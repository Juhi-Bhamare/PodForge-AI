import pymupdf

from services.text_processor import clean_text


def extract_text_from_pdf(file_path: str) -> dict:
    """
    Extract and clean text from a PDF.
    """

    document = pymupdf.open(file_path)

    pages = []
    full_text = ""

    for page in document:
        text = page.get_text()

        cleaned_page = clean_text(text)

        pages.append(cleaned_page)

        if cleaned_page:
            full_text += cleaned_page + "\n\n"

    document.close()

    words = full_text.split()

    return {
        "pages": len(pages),
        "words": len(words),
        "characters": len(full_text),
        "text": full_text.strip()
    }