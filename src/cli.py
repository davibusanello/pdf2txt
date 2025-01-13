#!/usr/bin/env python3
"""PDF to Text converter CLI.

This module provides the command-line interface for converting PDF files to text
using OCR technology.
"""

import argparse
import glob
import os

import argcomplete

from src.pdf2txt import pdf_to_text


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
