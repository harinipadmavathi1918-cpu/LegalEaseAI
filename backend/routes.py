"""FastAPI routes for LegalEase."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from .schemas import DocumentRequest, DocumentResponse, ExportRequest
from .ai_core.gemini_generator import GeminiDocumentGenerator
from . import export_utils

router = APIRouter()

# Single shared generator (stateless)
_generator = GeminiDocumentGenerator()


@router.get("/health")
def health():
    return {"status": "ok", "service": "LegalEase Backend"}


@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest):
    """Generate a legal document from structured inputs using Gemini."""
    try:
        content = _generator.generate_document(
            document_type=payload.document_type,
            party_a=payload.party_a,
            party_b=payload.party_b,
            effective_date=payload.effective_date,
            jurisdiction=payload.jurisdiction,
            key_terms=payload.key_terms,
            additional_notes=payload.additional_notes or "",
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")

    return DocumentResponse(
        document_type=payload.document_type,
        content=content,
        model=_generator.model_name,
    )


@router.post("/export")
def export_document(payload: ExportRequest):
    """Export a previously generated document to txt/docx/pdf."""
    fmt = payload.format
    title = payload.filename.replace("_", " ").title()

    if fmt == "txt":
        data = export_utils.to_txt(payload.content)
        media = "text/plain"
        ext = "txt"
    elif fmt == "docx":
        data = export_utils.to_docx(payload.content, title=title)
        media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ext = "docx"
    elif fmt == "pdf":
        data = export_utils.to_pdf(payload.content, title=title)
        media = "application/pdf"
        ext = "pdf"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

    filename = f"{payload.filename}.{ext}"
    return Response(
        content=data,
        media_type=media,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )