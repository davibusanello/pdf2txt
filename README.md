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

## Shell Completion

To enable shell completion (for bash/zsh), add this to your shell's rc file (~/.bashrc, ~/.zshrc):

```bash
eval "$(register-python-argcomplete $(which pdf-to-text))"
# or with explicit path
eval "$(register-python-argcomplete /path/to/your/virtual/env/bin/pdf-to-text)"
```

After setting up completion, you can use TAB to:

- Auto-complete PDF files when entering the input file
- Auto-complete directories and .txt files when entering the output file

## Dependencies

- `pdf2image`: For converting PDF pages to images
- `Pillow`: For image processing
- `pytesseract`: Python wrapper for Google's Tesseract OCR engine

## Usage

```bash
# Basic usage (default 4 threads and 3 pages per thread)
uv run pdf-to-text input.pdf output.txt

# With wildcards
uv run pdf-to-text "documents/*.pdf" outputs.txt

# Changing threads and chunk size
uv run pdf-to-text input.pdf output.txt --max-threads 8 --chunk-size 5

# Help
uv run pdf-to-text --help
```

When using wildcards with multiple input files, each output will be named as `output_filename.txt` where filename is the name of the input PDF.

## License

[MIT](./LICENSE) Copyright (c) 2025 Davi Busanello <itsme@davibusanello.me>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
