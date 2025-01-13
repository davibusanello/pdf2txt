import argparse
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ThreadPoolExecutor
from typing import List
from PIL import Image
import os
import glob
import argcomplete

def process_page_chunk(pages: List[Image.Image]) -> str:
    """Process a chunk of pages and return combined text."""
    chunk_text = ''
    for page in pages:
        chunk_text += pytesseract.image_to_string(page)
    return chunk_text

def chunk_list(lst: list, chunk_size: int) -> List[list]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def pdf_to_text(pdf_file: str, output_file: str, max_threads: int = 4, chunk_size: int = 3):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_file)

    # Split pages into chunks
    page_chunks = chunk_list(pages, chunk_size)

    # Process chunks in parallel
    text_chunks = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit all chunks for processing
        future_to_chunk = {executor.submit(process_page_chunk, chunk): i
                         for i, chunk in enumerate(page_chunks)}

        # Collect results in order
        text_chunks = [''] * len(page_chunks)
        for future in future_to_chunk:
            chunk_idx = future_to_chunk[future]
            text_chunks[chunk_idx] = future.result()

    # Combine all text chunks
    final_text = ''.join(text_chunks)

    # Write the extracted text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)

def pdf_completer(prefix, parsed_args, **kwargs):
    """Complete PDF files in current directory"""
    return (f for f in glob.glob(prefix + '*') if f.lower().endswith('.pdf'))

def dir_completer(prefix, parsed_args, **kwargs):
    """Complete directories and text files"""
    return (f for f in glob.glob(prefix + '*') if os.path.isdir(f) or f.lower().endswith('.txt'))

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Text")
    parser.add_argument('pdf_file', type=str, help='Path to the input PDF file (supports wildcards)').completer = pdf_completer
    parser.add_argument('output_file', type=str, help='Path to the output text file').completer = dir_completer
    parser.add_argument('--max-threads', type=int, default=4,
                      help='Maximum number of threads to use (default: 4)')
    parser.add_argument('--chunk-size', type=int, default=3,
                      help='Number of pages to process per thread (default: 3)')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # Expand file path
    pdf_files = glob.glob(os.path.expanduser(args.pdf_file))
    if not pdf_files:
        print(f"No files found matching: {args.pdf_file}")
        return

    # If multiple files are selected, adjust output filename
    for pdf_file in pdf_files:
        if len(pdf_files) > 1:
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            output_file = f"{os.path.splitext(args.output_file)[0]}_{base_name}.txt"
        else:
            output_file = args.output_file

        pdf_to_text(pdf_file, output_file,
                    max_threads=args.max_threads,
                    chunk_size=args.chunk_size)
        print(f'Text extracted and saved to {output_file}')

if __name__ == '__main__':
    main()
