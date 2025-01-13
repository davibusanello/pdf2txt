"""Core functionality for PDF to text conversion with multi-threading support.

This module provides the core functionality to convert PDF files to text using OCR
technology with support for multi-threading to improve performance.
"""

import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def process_page_chunk(pages: list[Image.Image]) -> str:
    """Process a chunk of pages and return combined text.

    Args:
        pages: List of PIL Image objects representing PDF pages.

    Returns:
        str: Combined text extracted from all pages in the chunk.
    """
    chunk_text = ""
    for page in pages:
        chunk_text += pytesseract.image_to_string(page)
    return chunk_text


def chunk_list(lst: list, chunk_size: int) -> list[list]:
    """Split a list into chunks of specified size.

    Args:
        lst: Input list to be chunked.
        chunk_size: Size of each chunk.

    Returns:
        List[list]: List of chunks.
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def pdf_to_text(
    pdf_file: str, output_file: str, max_threads: int = 4, chunk_size: int = 3
) -> None:
    """Convert PDF file to text using OCR with multi-threading.

    Args:
        pdf_file: Path to the input PDF file.
        output_file: Path where the output text will be saved.
        max_threads: Maximum number of threads to use for processing.
        chunk_size: Number of pages to process per thread.
    """
    from concurrent.futures import ThreadPoolExecutor

    pages = convert_from_path(pdf_file)
    page_chunks = chunk_list(pages, chunk_size)

    text_chunks = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_chunk = {
            executor.submit(process_page_chunk, chunk): i
            for i, chunk in enumerate(page_chunks)
        }

        text_chunks = [""] * len(page_chunks)
        for future in future_to_chunk:
            chunk_idx = future_to_chunk[future]
            text_chunks[chunk_idx] = future.result()

    final_text = "".join(text_chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)
