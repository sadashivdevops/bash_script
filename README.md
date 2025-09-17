# Bash Script Repository

This repository contains various scripts and utilities, including a new PDF to image conversion tool built with Go.

## Features

### PDF to Image Converter

A Go-based tool that converts PDF files to individual PNG images, with each page of the PDF exported as a separate image file.

#### Requirements

- Go 1.24.7 or later
- The tool uses the open-source `go-fitz` library (MuPDF Go bindings) for PDF operations

#### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sadashivdevops/bash_script.git
   cd bash_script
   ```

2. Install dependencies:
   ```bash
   go mod download
   ```

#### Usage

To convert a PDF file to images:

```bash
go run main.go <pdf-file-path>
```

**Example:**
```bash
go run main.go document.pdf
```

This will:
- Convert each page of `document.pdf` to individual PNG images
- Create a new directory called `document_images/`
- Save images as `page_001.png`, `page_002.png`, etc.

#### Features

- **Page-by-page conversion**: Each PDF page is converted to a separate PNG image
- **Automatic directory creation**: Creates an output directory named after the PDF file
- **Error handling**: Comprehensive error checking for file existence, permissions, and conversion issues
- **Progress tracking**: Shows conversion progress for each page
- **High-quality output**: Uses MuPDF for high-quality image rendering

#### Technical Details

- **PDF Library**: Uses `github.com/gen2brain/go-fitz` (MuPDF Go bindings)
- **Output Format**: PNG images
- **Naming Convention**: `page_XXX.png` where XXX is the zero-padded page number
- **Output Directory**: `{pdf_filename}_images/`

#### Example Output

```
$ go run main.go sample.pdf
Converted page 1 to sample_images/page_001.png
Converted page 2 to sample_images/page_002.png
Converted page 3 to sample_images/page_003.png
All 3 pages converted and saved to directory: sample_images
PDF conversion completed successfully!
```

### Other Scripts

- `new_git_script.sh`: Git branch management script for creating release branches

## License

This project is open source and available under the MIT License.