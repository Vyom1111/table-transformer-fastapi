# Table Transformer FastAPI 🧾🚀

This is a FastAPI-based backend that extracts tables from multi-page PDFs using Microsoft's `table-transformer-detection` and OCR (Tesseract). It supports outputs in:

- ✅ JSON
- ✅ CSV
- ✅ Excel (.xlsx)
- ✅ Markdown

## 🔧 Setup

### 1. Clone the Repo

```bash
git clone https://github.com/Vyom1111/table-transformer-fastapi.git
cd table-transformer-fastapi
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Also install **Tesseract OCR**:

- [Windows Download (UB Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)
- macOS: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr`

### 3. Run the App

```bash
uvicorn app:app --reload
```

Then visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📤 Example API Call

**Endpoint:**

```
POST /extract-tables/?format=json
```

**Formats:**

- `format=json` → structured table output
- `format=csv` → download as .csv
- `format=excel` → Excel download
- `format=md` → Markdown tables

---

## 📂 Project Structure

```
├── app.py                  # FastAPI app
├── requirements.txt        # Dependencies
├── utils/
│   ├── image_utils.py      # OCR + PDF utilities
│   └── formatter_utils.py  # Format converters (CSV/Excel/Markdown)
```

---

## 📄 License

MIT

---

