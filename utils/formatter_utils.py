from io import BytesIO
import pandas as pd

def json_to_csv(pages):
    buffer = BytesIO()
    for page in pages:
        for table in page["tables"]:
            df = pd.DataFrame(table["data"])
            df.to_csv(buffer, index=False, header=False)
            buffer.write(b"\n\n")
    buffer.seek(0)
    return buffer

def json_to_excel(pages):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for page in pages:
            for table in page["tables"]:
                df = pd.DataFrame(table["data"])
                sheet = f"Page{page['page']}_T{table['table_index']}"
                df.to_excel(writer, index=False, header=False, sheet_name=sheet)
    buffer.seek(0)
    return buffer

def json_to_markdown(pages):
    md = ""
    for page in pages:
        for table in page["tables"]:
            md += f"\n### Page {page['page']} - Table {table['table_index']}\n\n"
            for row in table["data"]:
                md += "| " + " | ".join(row) + " |\n"
            md += "\n"
    return BytesIO(md.encode())
