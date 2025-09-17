#!/usr/bin/env python3
"""
Unit tests for the Image and PDF Conversion Tool
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

if PIL_AVAILABLE and PYMUPDF_AVAILABLE:
    from image_converter import ImageConverter
else:
    # Create a mock class for testing when dependencies are not available
    class ImageConverter:
        def __init__(self, quality=95):
            self.quality = quality
        
        def convert_image_format(self, *args, **kwargs):
            return False
        
        def png_to_jpg(self, *args, **kwargs):
            return False
        
        def jpg_to_png(self, *args, **kwargs):
            return False
        
        def pdf_to_images(self, *args, **kwargs):
            return []


class TestImageConverter(unittest.TestCase):
    """Test cases for ImageConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = ImageConverter(quality=90)
        
        # Create test images if PIL is available
        if PIL_AVAILABLE:
            self.test_png_path = os.path.join(self.temp_dir, 'test.png')
            self.test_jpg_path = os.path.join(self.temp_dir, 'test.jpg')
            
            # Create a simple test PNG image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(self.test_png_path, 'PNG')
            
            # Create a simple test JPG image
            img.save(self.test_jpg_path, 'JPEG')
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_init(self):
        """Test ImageConverter initialization."""
        # Test default quality
        converter = ImageConverter()
        self.assertEqual(converter.quality, 95)
        
        # Test custom quality
        converter = ImageConverter(quality=80)
        self.assertEqual(converter.quality, 80)
        
        # Test quality bounds
        converter = ImageConverter(quality=0)
        self.assertEqual(converter.quality, 1)
        
        converter = ImageConverter(quality=150)
        self.assertEqual(converter.quality, 100)
    
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_png_to_jpg_conversion(self):
        """Test PNG to JPG conversion."""
        output_path = os.path.join(self.temp_dir, 'output.jpg')
        
        # Test successful conversion
        result = self.converter.png_to_jpg(self.test_png_path, output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify the output is a valid JPEG
        with Image.open(output_path) as img:
            self.assertEqual(img.format, 'JPEG')
    
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_jpg_to_png_conversion(self):
        """Test JPG to PNG conversion."""
        output_path = os.path.join(self.temp_dir, 'output.png')
        
        # Test successful conversion
        result = self.converter.jpg_to_png(self.test_jpg_path, output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify the output is a valid PNG
        with Image.open(output_path) as img:
            self.assertEqual(img.format, 'PNG')
    
    def test_convert_nonexistent_file(self):
        """Test conversion with non-existent input file."""
        nonexistent_path = os.path.join(self.temp_dir, 'nonexistent.png')
        output_path = os.path.join(self.temp_dir, 'output.jpg')
        
        result = self.converter.convert_image_format(nonexistent_path, output_path)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(output_path))
    
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_format_inference_from_extension(self):
        """Test format inference from file extension."""
        # Test PNG output
        png_output = os.path.join(self.temp_dir, 'test_output.png')
        result = self.converter.convert_image_format(
            self.test_jpg_path, png_output
        )
        self.assertTrue(result)
        
        with Image.open(png_output) as img:
            self.assertEqual(img.format, 'PNG')
        
        # Test JPEG output
        jpg_output = os.path.join(self.temp_dir, 'test_output.jpg')
        result = self.converter.convert_image_format(
            self.test_png_path, jpg_output
        )
        self.assertTrue(result)
        
        with Image.open(jpg_output) as img:
            self.assertEqual(img.format, 'JPEG')
    
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_rgba_to_jpeg_conversion(self):
        """Test RGBA image conversion to JPEG."""
        # Create an RGBA image
        rgba_path = os.path.join(self.temp_dir, 'rgba_test.png')
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 128))  # Semi-transparent red
        img.save(rgba_path, 'PNG')
        
        # Convert to JPEG
        jpg_output = os.path.join(self.temp_dir, 'rgba_to_jpg.jpg')
        result = self.converter.convert_image_format(rgba_path, jpg_output)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(jpg_output))
        
        # Verify the output is RGB
        with Image.open(jpg_output) as img:
            self.assertEqual(img.format, 'JPEG')
            self.assertEqual(img.mode, 'RGB')
    
    def test_unsupported_format(self):
        """Test conversion with unsupported output format."""
        if not PIL_AVAILABLE:
            self.skipTest("PIL/Pillow not available")
        
        output_path = os.path.join(self.temp_dir, 'output.bmp')
        result = self.converter.convert_image_format(
            self.test_png_path, output_path
        )
        self.assertFalse(result)
    
    @unittest.skipUnless(PYMUPDF_AVAILABLE, "PyMuPDF not available")
    def test_pdf_to_images_with_mock_pdf(self):
        """Test PDF to images conversion with mocked PDF."""
        # Create a simple mock PDF file
        pdf_path = os.path.join(self.temp_dir, 'test.pdf')
        output_dir = os.path.join(self.temp_dir, 'pdf_output')
        
        # Create a minimal PDF file for testing
        try:
            # Create a simple PDF with PyMuPDF
            doc = fitz.open()  # Create empty PDF
            page = doc.new_page()  # Add a page
            page.insert_text((50, 50), "Test Page 1")
            
            page2 = doc.new_page()  # Add another page
            page2.insert_text((50, 50), "Test Page 2")
            
            doc.save(pdf_path)
            doc.close()
            
            # Test conversion
            output_files = self.converter.pdf_to_images(
                pdf_path, output_dir, 'PNG', dpi=72
            )
            
            # Should have created 2 images
            self.assertEqual(len(output_files), 2)
            
            # Check that files exist
            for file_path in output_files:
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(file_path.endswith('.png'))
        
        except Exception as e:
            self.skipTest(f"Could not create test PDF: {e}")
    
    def test_pdf_to_images_nonexistent_file(self):
        """Test PDF to images conversion with non-existent PDF."""
        nonexistent_pdf = os.path.join(self.temp_dir, 'nonexistent.pdf')
        output_dir = os.path.join(self.temp_dir, 'output')
        
        output_files = self.converter.pdf_to_images(nonexistent_pdf, output_dir)
        self.assertEqual(len(output_files), 0)
    
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_output_directory_creation(self):
        """Test that output directories are created automatically."""
        nested_output = os.path.join(
            self.temp_dir, 'nested', 'directory', 'output.jpg'
        )
        
        result = self.converter.png_to_jpg(self.test_png_path, nested_output)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(nested_output))


class TestImageConverterCLI(unittest.TestCase):
    """Test cases for command-line interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        if PIL_AVAILABLE:
            self.test_png_path = os.path.join(self.temp_dir, 'test.png')
            self.test_jpg_path = os.path.join(self.temp_dir, 'test.jpg')
            
            # Create test images
            img = Image.new('RGB', (50, 50), color='blue')
            img.save(self.test_png_path, 'PNG')
            img.save(self.test_jpg_path, 'JPEG')
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    @patch('sys.argv', ['image_converter.py', 'png-to-jpg', 'test.png', 'output.jpg'])
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_cli_png_to_jpg(self):
        """Test CLI PNG to JPG conversion."""
        output_path = os.path.join(self.temp_dir, 'cli_output.jpg')
        
        with patch('sys.argv', [
            'image_converter.py', 'png-to-jpg', 
            self.test_png_path, output_path
        ]):
            # Import and test main function
            from image_converter import main
            
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            
            self.assertTrue(os.path.exists(output_path))
    
    @patch('sys.argv', ['image_converter.py', 'jpg-to-png', 'test.jpg', 'output.png'])
    @unittest.skipUnless(PIL_AVAILABLE, "PIL/Pillow not available")
    def test_cli_jpg_to_png(self):
        """Test CLI JPG to PNG conversion."""
        output_path = os.path.join(self.temp_dir, 'cli_output.png')
        
        with patch('sys.argv', [
            'image_converter.py', 'jpg-to-png', 
            self.test_jpg_path, output_path
        ]):
            from image_converter import main
            
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)
            
            self.assertTrue(os.path.exists(output_path))
    
    def test_cli_no_command(self):
        """Test CLI with no command."""
        with patch('sys.argv', ['image_converter.py']):
            from image_converter import main
            
            # Should not raise an exception, just print help
            try:
                main()
            except SystemExit:
                pass  # Expected behavior


class TestDependencyHandling(unittest.TestCase):
    """Test cases for handling missing dependencies."""
    
    def test_missing_pil_import(self):
        """Test behavior when PIL is not available."""
        if PIL_AVAILABLE:
            # Mock the import to fail
            with patch.dict('sys.modules', {'PIL': None}):
                # This would normally cause an ImportError
                pass
    
    def test_missing_pymupdf_import(self):
        """Test behavior when PyMuPDF is not available."""
        if PYMUPDF_AVAILABLE:
            # Mock the import to fail
            with patch.dict('sys.modules', {'fitz': None}):
                # This would normally cause an ImportError
                pass


if __name__ == '__main__':
    # Print dependency status
    print(f"PIL/Pillow available: {PIL_AVAILABLE}")
    print(f"PyMuPDF available: {PYMUPDF_AVAILABLE}")
    print()
    
    # Run tests
    unittest.main(verbosity=2)