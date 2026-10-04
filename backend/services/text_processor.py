import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text while preserving meaningful content.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 6000,
    overlap: int = 500
) -> list[str]:
    """
    Split text into overlapping chunks.

    Keeping a small overlap helps preserve context
    between neighboring chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks