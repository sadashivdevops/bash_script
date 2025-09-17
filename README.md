# Image and PDF Conversion Tool

A Python-based tool for converting between image formats (PNG ↔ JPG) and converting PDF documents to individual image files.

## Features

- **Image Format Conversion**: Convert between PNG and JPG formats with quality control
- **PDF to Images**: Convert each page of a PDF document to separate image files
- **High Quality Output**: Configurable DPI and JPEG quality settings
- **Automatic RGBA Handling**: Proper handling of transparency when converting to JPEG
- **Command-Line Interface**: Easy-to-use CLI for batch processing
- **Comprehensive Testing**: Full unit test coverage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sadashivdevops/bash_script.git
cd bash_script
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies

- **Pillow (PIL)**: For image format conversion
- **PyMuPDF**: For PDF to image conversion

## Usage

### Command Line Interface

The tool provides three main commands:

#### 1. Convert PNG to JPG
```bash
python image_converter.py png-to-jpg input.png output.jpg [--quality 95]
```

#### 2. Convert JPG to PNG
```bash
python image_converter.py jpg-to-png input.jpg output.png
```

#### 3. Convert PDF to Images
```bash
python image_converter.py pdf-to-images input.pdf output_directory [--format PNG] [--dpi 150] [--quality 95]
```

### Python API

You can also use the tool programmatically:

```python
from image_converter import ImageConverter

# Create converter instance
converter = ImageConverter(quality=90)

# Convert PNG to JPG
success = converter.png_to_jpg('input.png', 'output.jpg')

# Convert JPG to PNG
success = converter.jpg_to_png('input.jpg', 'output.png')

# Convert PDF to images
output_files = converter.pdf_to_images(
    'document.pdf', 
    'output_directory',
    image_format='PNG',
    dpi=300
)
```

## Command Line Options

### PNG to JPG Conversion
- `input`: Path to input PNG file
- `output`: Path for output JPG file
- `--quality`: JPEG quality (1-100, default: 95)

### JPG to PNG Conversion
- `input`: Path to input JPG file
- `output`: Path for output PNG file

### PDF to Images Conversion
- `input`: Path to input PDF file
- `output_dir`: Directory to save image files
- `--format`: Output image format (PNG or JPEG, default: PNG)
- `--dpi`: Resolution for conversion (default: 150)
- `--quality`: JPEG quality when using JPEG format (1-100, default: 95)

## Examples

### Basic Image Conversion
```bash
# Convert PNG to JPG with default quality
python image_converter.py png-to-jpg photo.png photo.jpg

# Convert PNG to JPG with custom quality
python image_converter.py png-to-jpg photo.png photo.jpg --quality 85

# Convert JPG to PNG
python image_converter.py jpg-to-png photo.jpg photo.png
```

### PDF Conversion
```bash
# Convert PDF to PNG images at 150 DPI
python image_converter.py pdf-to-images document.pdf ./images/

# Convert PDF to JPEG images at 300 DPI
python image_converter.py pdf-to-images document.pdf ./images/ --format JPEG --dpi 300 --quality 90
```

### Output File Naming

When converting PDF to images, files are automatically named as:
```
{original_filename}_page_{page_number}.{extension}
```

For example, converting `report.pdf` will create:
- `report_page_001.png`
- `report_page_002.png`
- `report_page_003.png`
- etc.

## Features in Detail

### Image Quality Control
- JPEG quality can be set from 1 (lowest) to 100 (highest)
- PNG conversion preserves full quality
- Automatic optimization for JPEG files

### Transparency Handling
- RGBA images are properly converted to RGB when saving as JPEG
- Transparent areas are filled with white background
- PNG format preserves transparency

### Error Handling
- Comprehensive error checking and logging
- Graceful handling of invalid files
- Automatic directory creation for output files

## Testing

Run the comprehensive test suite:

```bash
python -m unittest test_image_converter.py -v
```

The test suite includes:
- Image format conversion tests
- PDF conversion tests
- Error handling tests
- CLI interface tests
- Edge case handling

### Test Coverage

The tests cover:
- ✅ PNG to JPG conversion
- ✅ JPG to PNG conversion
- ✅ PDF to images conversion
- ✅ RGBA transparency handling
- ✅ Error handling for missing files
- ✅ Command-line interface
- ✅ Quality settings
- ✅ DPI settings
- ✅ Output directory creation

## Requirements

- Python 3.7+
- Pillow (PIL) >= 10.0.0
- PyMuPDF >= 1.23.0

## Performance Notes

- **Memory Usage**: Large PDFs are processed page by page to minimize memory usage
- **DPI Settings**: Higher DPI values produce larger, higher-quality images but require more processing time
- **Quality Settings**: JPEG quality affects both file size and image quality

## Error Handling

The tool provides detailed error messages for common issues:
- File not found errors
- Invalid format errors
- Permission errors
- Corrupted file errors

All errors are logged with timestamps for debugging purposes.

## License

This project is part of the bash_script repository and follows the same licensing terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues and questions, please create an issue in the GitHub repository.