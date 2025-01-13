# PDF to Text Converter

A Python-based tool that converts PDF files to text using OCR (Optical Character Recognition) technology.

## Requirements

- Python 3.13 or higher
- Tesseract OCR engine installed on your system
- UV package manager

## Installation

1. Install Tesseract OCR on your system:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download and install from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

2. Install UV if you haven't already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Clone the repository:

   ```bash
   git clone https://github.com/davibusanello/pdf-to-text.git
   cd pdf-to-text
   ```

4. Create and activate a virtual environment with UV:

   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

5. Install dependencies:

   ```bash
   uv sync
   ```

## Dependencies

- `pdf2image`: For converting PDF pages to images
- `Pillow`: For image processing
- `pytesseract`: Python wrapper for Google's Tesseract OCR engine

## Usage

```bash
uv run pdf-to-text.py <input_pdf_file> <output_text_file>
```

## License

[MIT](./LICENSE) Copyright (c) 2025 Davi Busanello <itsme@davibusanello.me>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
