import argparse
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ThreadPoolExecutor
from typing import List
from PIL import Image

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

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Text")
    parser.add_argument('pdf_file', type=str, help='Path to the input PDF file')
    parser.add_argument('output_file', type=str, help='Path to the output text file')
    parser.add_argument('--max-threads', type=int, default=4,
                      help='Maximum number of threads to use (default: 4)')
    parser.add_argument('--chunk-size', type=int, default=3,
                      help='Number of pages to process per thread (default: 3)')

    args = parser.parse_args()
    pdf_to_text(args.pdf_file, args.output_file,
                max_threads=args.max_threads,
                chunk_size=args.chunk_size)
    print(f'Text extracted and saved to {args.output_file}')

if __name__ == '__main__':
    main()
