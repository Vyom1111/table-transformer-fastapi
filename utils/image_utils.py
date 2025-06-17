from pdf2image import convert_from_bytes
from PIL import Image, ImageDraw
import pytesseract

def pdf_to_images(pdf_bytes):
    return convert_from_bytes(pdf_bytes)

def draw_boxes(image, boxes):
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle(box, outline="red", width=2)
    return image

def crop_tables(image, boxes):
    tables = []
    for box in boxes:
        xmin, ymin, xmax, ymax = map(int, box)
        cropped = image.crop((xmin, ymin, xmax, ymax))
        tables.append(cropped)
    return tables

def extract_text_from_table(image):
    # Use Tesseract to extract text from image
    text = pytesseract.image_to_string(image)
    # Naive row-wise split
    rows = [r.strip() for r in text.strip().split("\n") if r.strip()]
    table = []
    for row in rows:
        table.append([cell.strip() for cell in row.split()])  # whitespace split
    return table
