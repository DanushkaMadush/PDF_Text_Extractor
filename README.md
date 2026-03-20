# PDF Text Extractor API

A **FastAPI** microservice for uploading PDF files and extracting **text-only** content (no OCR).

- Upload a PDF (`multipart/form-data`)
- Extract readable text from all pages
- Return extracted text as JSON

> Note: This repository currently contains a folder structure for the service, but core Python files such as `main.py` and `requirements.txt` are placeholders. This README documents the intended FastAPI implementation.

## Tech Stack

- **FastAPI** (API + OpenAPI docs)
- **Uvicorn** (ASGI server)
- PDF text extraction library (recommended): **PyMuPDF (fitz)**
  - Alternative: `pdfplumber` (better for layout-heavy PDFs)

## API Endpoints (planned)

### Health check

`GET /health`

Response:
```json
{"status":"ok"}
```

### Extract PDF text

`POST /api/v1/extract`

Consumes: `multipart/form-data`

Form fields:
- `file` (required): PDF file

Response example:
```json
{
  "filename": "example.pdf",
  "pages": 3,
  "text": "...all extracted text..."
}
```

## Local Development

### Prerequisites

- Python 3.10+

### Setup

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Run (FastAPI)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./sample.pdf"
```

## Notes / Limitations

- **No OCR**: scanned/image-only PDFs will likely return empty text.
- Consider adding:
  - file type validation (`application/pdf`)
  - file size limits
  - timeouts for very large PDFs

## Roadmap

- [ ] Implement FastAPI app in `main.py`
- [ ] Add dependencies to `requirements.txt`
- [ ] Implement extraction logic in `app/services/extractor.py`
- [ ] Define response schema in `app/models/extract_response.py`
- [ ] Add tests under `tests/`

## License

See [LICENSE](./LICENSE).