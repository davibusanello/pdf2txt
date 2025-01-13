#!/usr/bin/env python3
"""PDF to Text converter with multi-threading support.

This module provides functionality to convert PDF files to text using OCR technology
with support for multi-threading to improve performance.
"""

import argparse
import glob
import os
from concurrent.futures import ThreadPoolExecutor

import argcomplete
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


def pdf_completer(prefix: str, parsed_args: argparse.Namespace, **kwargs) -> list[str]:
    """Complete PDF files in current directory.

    Args:
        prefix: Current input prefix to complete.
        parsed_args: Parsed command line arguments.
        **kwargs: Additional arguments passed by argcomplete.

    Returns:
        List of matching PDF files.
    """
    return [f for f in glob.glob(prefix + "*") if f.lower().endswith(".pdf")]


def dir_completer(prefix: str, parsed_args: argparse.Namespace, **kwargs) -> list[str]:
    """Complete directories and text files.

    Args:
        prefix: Current input prefix to complete.
        parsed_args: Parsed command line arguments.
        **kwargs: Additional arguments passed by argcomplete.

    Returns:
        List of matching directories and text files.
    """
    return [
        f
        for f in glob.glob(prefix + "*")
        if os.path.isdir(f) or f.lower().endswith(".txt")
    ]


def main() -> None:
    """Execute the main program."""
    parser = argparse.ArgumentParser(description="Convert PDF to Text")
    parser.add_argument(
        "pdf_file", type=str, help="Path to the input PDF file (supports wildcards)"
    ).completer = pdf_completer
    parser.add_argument(
        "output_file", type=str, help="Path to the output text file"
    ).completer = dir_completer
    parser.add_argument(
        "--max-threads",
        type=int,
        default=4,
        help="Maximum number of threads to use (default: 4)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=3,
        help="Number of pages to process per thread (default: 3)",
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    pdf_files = glob.glob(os.path.expanduser(args.pdf_file))
    if not pdf_files:
        print(f"No files found matching: {args.pdf_file}")  # noqa: T201
        return

    for pdf_file in pdf_files:
        if len(pdf_files) > 1:
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            output_file = f"{os.path.splitext(args.output_file)[0]}_{base_name}.txt"
        else:
            output_file = args.output_file

        pdf_to_text(
            pdf_file,
            output_file,
            max_threads=args.max_threads,
            chunk_size=args.chunk_size,
        )
        print(f"Text extracted and saved to {output_file}")  # noqa: T201


if __name__ == "__main__":
    main()
