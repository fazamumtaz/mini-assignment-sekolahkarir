from pathlib import Path
import fitz


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from a PDF document."""

    pdf_path = Path(pdf_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with fitz.open(pdf_path) as document:
        pages = [
            page.get_text("text", sort=True)
            for page in document
        ]

    text = "\n".join(pages).strip()

    if not text:
        raise ValueError(f"No extractable text: {pdf_path}")

    return text
