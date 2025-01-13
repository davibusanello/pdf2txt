import argparse
from pdf2image import convert_from_path
import pytesseract

def pdf_to_text(pdf_file, output_file):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_file)

    # Extract text from each page
    text = ''
    for page in pages:
        text += pytesseract.image_to_string(page)

    # Write the extracted text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Text")
    parser.add_argument('pdf_file', type=str, help='Path to the input PDF file')
    parser.add_argument('output_file', type=str, help='Path to the output text file')

    args = parser.parse_args()
    pdf_to_text(args.pdf_file, args.output_file)
    print(f'Text extracted and saved to {args.output_file}')

if __name__ == '__main__':
    main()
