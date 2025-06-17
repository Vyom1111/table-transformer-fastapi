from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse, StreamingResponse
from transformers import AutoImageProcessor, TableTransformerForObjectDetection
from utils.image_utils import pdf_to_images, crop_tables, extract_text_from_table
from utils.formatter_utils import json_to_csv, json_to_excel, json_to_markdown
import torch
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust as needed

app = FastAPI()

image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

@app.post("/extract-tables/")
async def extract_tables(
    file: UploadFile = File(...),
    format: str = Query("json", enum=["json", "csv", "excel", "md"])
):
    try:
        pdf_bytes = await file.read()
        images = pdf_to_images(pdf_bytes)

        all_tables = []

        for page_index, image in enumerate(images):
            inputs = image_processor(images=image, return_tensors="pt")
            outputs = model(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            results = image_processor.post_process_object_detection(
                outputs, threshold=0.9, target_sizes=target_sizes
            )[0]

            boxes = [box.tolist() for box in results["boxes"]]
            cropped_tables = crop_tables(image, boxes)

            page_tables = []

            for table_index, table_img in enumerate(cropped_tables):
                table_data = extract_text_from_table(table_img)
                page_tables.append({
                    "table_index": table_index + 1,
                    "data": table_data
                })

            all_tables.append({
                "page": page_index + 1,
                "tables": page_tables
            })

        if format == "json":
            return JSONResponse(content={"pages": all_tables})
        elif format == "csv":
            csv_buffer = json_to_csv(all_tables)
            return StreamingResponse(csv_buffer, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tables.csv"})
        elif format == "excel":
            excel_buffer = json_to_excel(all_tables)
            return StreamingResponse(excel_buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=tables.xlsx"})
        elif format == "md":
            md_buffer = json_to_markdown(all_tables)
            return StreamingResponse(md_buffer, media_type="text/markdown", headers={"Content-Disposition": "attachment; filename=tables.md"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
