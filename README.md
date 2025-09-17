# Image and PDF Conversion Utility

A Python utility for converting between image formats (PNG ↔ JPG) and converting PDF pages to images.

## Features

- **Image Format Conversion**: Convert between PNG and JPG formats
- **PDF to Image Conversion**: Convert each page of a PDF to individual image files
- **Multiple Output Formats**: Support for PNG and JPEG output from PDFs
- **Configurable Quality**: Adjustable DPI and quality settings
- **Comprehensive Error Handling**: Detailed error messages and validation
- **Full Test Coverage**: Extensive unit tests for all functionality

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `Pillow>=10.0.0` - For image processing
- `pdf2image>=1.16.3` - For PDF to image conversion
- `pytest>=7.4.0` - For running tests
- `pytest-cov>=4.1.0` - For test coverage

## Usage

### Image Conversion

```python
from image_converter import ImageConverter

# Convert PNG to JPG
ImageConverter.png_to_jpg('input.png', 'output.jpg')

# Convert JPG to PNG
ImageConverter.jpg_to_png('input.jpg', 'output.png')

# Auto-generate output filename
ImageConverter.png_to_jpg('image.png')  # Creates image.jpg
ImageConverter.jpg_to_png('photo.jpg')  # Creates photo.png
```

### PDF to Image Conversion

```python
from image_converter import PDFConverter

# Convert PDF to PNG images (default)
image_paths = PDFConverter.pdf_to_images('document.pdf')

# Convert to JPEG with custom settings
image_paths = PDFConverter.pdf_to_images(
    'document.pdf',
    output_dir='output_folder/',
    output_format='JPEG',
    dpi=300
)

# Each page becomes a separate image file:
# document_page_001.png, document_page_002.png, etc.
```

### Command Line Usage

Run the example script to see the functionality in action:

```bash
python3 example_usage.py
```

## API Reference

### ImageConverter Class

#### `png_to_jpg(input_path, output_path=None)`
Convert PNG image to JPG format.

**Parameters:**
- `input_path` (str|Path): Path to input PNG file
- `output_path` (str|Path, optional): Output JPG file path. If None, uses input filename with .jpg extension

**Returns:** `str` - Path to converted JPG file

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If input file is not a valid PNG or conversion fails

#### `jpg_to_png(input_path, output_path=None)`
Convert JPG image to PNG format.

**Parameters:**
- `input_path` (str|Path): Path to input JPG file  
- `output_path` (str|Path, optional): Output PNG file path. If None, uses input filename with .png extension

**Returns:** `str` - Path to converted PNG file

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If input file is not a valid JPG or conversion fails

### PDFConverter Class

#### `pdf_to_images(input_path, output_dir=None, output_format='PNG', dpi=200)`
Convert each page of a PDF to individual images.

**Parameters:**
- `input_path` (str|Path): Path to input PDF file
- `output_dir` (str|Path, optional): Output directory. If None, uses input file directory
- `output_format` (str): Output format ('PNG', 'JPEG', or 'JPG'). Default: 'PNG'
- `dpi` (int): Resolution for output images. Default: 200

**Returns:** `List[str]` - List of paths to generated image files

**Raises:**
- `FileNotFoundError`: If input PDF file doesn't exist
- `ValueError`: If PDF cannot be processed or invalid format specified

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest test_image_converter.py -v

# Run with coverage
python -m pytest test_image_converter.py --cov=image_converter --cov-report=html
```

The test suite includes:
- Image format conversion tests
- PDF to image conversion tests  
- Error handling and edge case tests
- File validation tests
- Format compatibility tests

## Requirements

### System Dependencies

For PDF conversion functionality, you may need to install poppler-utils:

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download and install poppler from: https://poppler.freedesktop.org/

### Python Dependencies

See `requirements.txt` for the complete list of Python dependencies.

## Examples

### Basic Image Conversion
```python
from image_converter import ImageConverter

# Convert a PNG with transparency to JPG
# (transparency will be replaced with white background)
ImageConverter.png_to_jpg('logo.png', 'logo.jpg')

# Convert JPG to PNG (preserves quality)
ImageConverter.jpg_to_png('photo.jpg', 'photo.png')
```

### PDF Processing
```python
from image_converter import PDFConverter

# Convert a multi-page PDF to high-quality PNG images
pages = PDFConverter.pdf_to_images(
    'presentation.pdf',
    output_dir='slides/',
    output_format='PNG',
    dpi=300
)

print(f"Converted {len(pages)} pages:")
for page in pages:
    print(f"  {page}")
```

### Error Handling
```python
from image_converter import ImageConverter, PDFConverter

try:
    ImageConverter.png_to_jpg('nonexistent.png')
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Conversion error: {e}")

try:
    PDFConverter.pdf_to_images('document.pdf', output_format='INVALID')
except ValueError as e:
    print(f"Invalid format: {e}")
```

## License

This project is provided as-is for educational and utility purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **"poppler not found" error**: Install poppler-utils system package
2. **"Permission denied" error**: Check file permissions and output directory access
3. **"Invalid image format" error**: Verify input file is actually in the expected format
4. **Memory issues with large PDFs**: Use lower DPI or process pages individually

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify input files are valid and accessible
3. Run the test suite to ensure functionality works
4. Check the example script for usage patterns