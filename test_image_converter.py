"""
Unit tests for image and PDF conversion functionality.
"""

import os
import tempfile
import pytest
from pathlib import Path
from PIL import Image, ImageDraw
from unittest.mock import patch, MagicMock
import shutil

from image_converter import ImageConverter, PDFConverter


class TestImageConverter:
    """Test cases for ImageConverter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_png(self, filename: str = "test.png", size: tuple = (100, 100), 
                       mode: str = "RGBA") -> Path:
        """Create a test PNG image."""
        filepath = self.temp_path / filename
        img = Image.new(mode, size, (255, 0, 0, 128))  # Red with transparency
        
        # Add some content
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 90, 90], fill=(0, 255, 0, 255))  # Green rectangle
        
        img.save(filepath, "PNG")
        return filepath
    
    def create_test_jpg(self, filename: str = "test.jpg", size: tuple = (100, 100)) -> Path:
        """Create a test JPG image."""
        filepath = self.temp_path / filename
        img = Image.new("RGB", size, (0, 0, 255))  # Blue
        
        # Add some content
        draw = ImageDraw.Draw(img)
        draw.ellipse([20, 20, 80, 80], fill=(255, 255, 0))  # Yellow circle
        
        img.save(filepath, "JPEG")
        return filepath
    
    def test_png_to_jpg_success(self):
        """Test successful PNG to JPG conversion."""
        # Create test PNG
        png_path = self.create_test_png()
        jpg_path = self.temp_path / "converted.jpg"
        
        # Convert
        result_path = ImageConverter.png_to_jpg(png_path, jpg_path)
        
        # Verify
        assert result_path == str(jpg_path)
        assert jpg_path.exists()
        
        # Check the converted image
        with Image.open(jpg_path) as img:
            assert img.format == "JPEG"
            assert img.mode == "RGB"
            assert img.size == (100, 100)
    
    def test_png_to_jpg_auto_output_path(self):
        """Test PNG to JPG conversion with automatic output path."""
        # Create test PNG
        png_path = self.create_test_png("input.png")
        
        # Convert without specifying output path
        result_path = ImageConverter.png_to_jpg(png_path)
        
        # Verify
        expected_path = self.temp_path / "input.jpg"
        assert result_path == str(expected_path)
        assert expected_path.exists()
    
    def test_png_to_jpg_rgba_handling(self):
        """Test PNG with transparency is properly converted to JPG."""
        # Create RGBA PNG
        png_path = self.create_test_png("rgba.png", mode="RGBA")
        
        # Convert
        result_path = ImageConverter.png_to_jpg(png_path)
        
        # Verify JPG has no transparency
        with Image.open(result_path) as img:
            assert img.mode == "RGB"
            # Should have white background where transparency was
    
    def test_png_to_jpg_file_not_found(self):
        """Test PNG to JPG conversion with non-existent file."""
        non_existent = self.temp_path / "does_not_exist.png"
        
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            ImageConverter.png_to_jpg(non_existent)
    
    def test_png_to_jpg_invalid_format(self):
        """Test PNG to JPG conversion with non-PNG file."""
        # Create a JPG file but try to convert as PNG
        jpg_path = self.create_test_jpg("fake.png")
        
        with pytest.raises(ValueError, match="Input file is not a PNG image"):
            ImageConverter.png_to_jpg(jpg_path)
    
    def test_jpg_to_png_success(self):
        """Test successful JPG to PNG conversion."""
        # Create test JPG
        jpg_path = self.create_test_jpg()
        png_path = self.temp_path / "converted.png"
        
        # Convert
        result_path = ImageConverter.jpg_to_png(jpg_path, png_path)
        
        # Verify
        assert result_path == str(png_path)
        assert png_path.exists()
        
        # Check the converted image
        with Image.open(png_path) as img:
            assert img.format == "PNG"
            assert img.size == (100, 100)
    
    def test_jpg_to_png_auto_output_path(self):
        """Test JPG to PNG conversion with automatic output path."""
        # Create test JPG
        jpg_path = self.create_test_jpg("input.jpg")
        
        # Convert without specifying output path
        result_path = ImageConverter.jpg_to_png(jpg_path)
        
        # Verify
        expected_path = self.temp_path / "input.png"
        assert result_path == str(expected_path)
        assert expected_path.exists()
    
    def test_jpg_to_png_file_not_found(self):
        """Test JPG to PNG conversion with non-existent file."""
        non_existent = self.temp_path / "does_not_exist.jpg"
        
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            ImageConverter.jpg_to_png(non_existent)
    
    def test_jpg_to_png_invalid_format(self):
        """Test JPG to PNG conversion with non-JPG file."""
        # Create a PNG file but try to convert as JPG
        png_path = self.create_test_png("fake.jpg")
        
        with pytest.raises(ValueError, match="Input file is not a JPG image"):
            ImageConverter.jpg_to_png(png_path)


class TestPDFConverter:
    """Test cases for PDFConverter class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_success(self, mock_convert):
        """Test successful PDF to images conversion."""
        # Mock PDF conversion
        mock_images = [
            Image.new('RGB', (100, 100), (255, 0, 0)),  # Red page
            Image.new('RGB', (100, 100), (0, 255, 0)),  # Green page
        ]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Convert
        result_paths = PDFConverter.pdf_to_images(pdf_path, self.temp_path)
        
        # Verify
        assert len(result_paths) == 2
        assert all(Path(path).exists() for path in result_paths)
        assert "test_page_001.png" in result_paths[0]
        assert "test_page_002.png" in result_paths[1]
        
        # Verify mock was called correctly
        mock_convert.assert_called_once_with(pdf_path, dpi=200)
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_jpeg_format(self, mock_convert):
        """Test PDF to images conversion with JPEG output."""
        # Mock PDF conversion
        mock_images = [Image.new('RGB', (100, 100), (255, 0, 0))]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Convert to JPEG
        result_paths = PDFConverter.pdf_to_images(
            pdf_path, self.temp_path, output_format='JPEG'
        )
        
        # Verify
        assert len(result_paths) == 1
        assert result_paths[0].endswith('.jpg')
        assert Path(result_paths[0]).exists()
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_auto_output_dir(self, mock_convert):
        """Test PDF to images conversion with automatic output directory."""
        # Mock PDF conversion
        mock_images = [Image.new('RGB', (100, 100), (255, 0, 0))]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Convert without specifying output directory
        result_paths = PDFConverter.pdf_to_images(pdf_path)
        
        # Verify output is in same directory as PDF
        assert len(result_paths) == 1
        result_path = Path(result_paths[0])
        assert result_path.parent == self.temp_path
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_custom_dpi(self, mock_convert):
        """Test PDF to images conversion with custom DPI."""
        # Mock PDF conversion
        mock_images = [Image.new('RGB', (100, 100), (255, 0, 0))]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Convert with custom DPI
        PDFConverter.pdf_to_images(pdf_path, self.temp_path, dpi=300)
        
        # Verify mock was called with correct DPI
        mock_convert.assert_called_once_with(pdf_path, dpi=300)
    
    def test_pdf_to_images_file_not_found(self):
        """Test PDF to images conversion with non-existent file."""
        non_existent = self.temp_path / "does_not_exist.pdf"
        
        with pytest.raises(FileNotFoundError, match="Input PDF file not found"):
            PDFConverter.pdf_to_images(non_existent)
    
    def test_pdf_to_images_invalid_format(self):
        """Test PDF to images conversion with invalid output format."""
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            PDFConverter.pdf_to_images(pdf_path, output_format="BMP")
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_no_pages(self, mock_convert):
        """Test PDF to images conversion with empty PDF."""
        # Mock empty PDF
        mock_convert.return_value = []
        
        # Create fake PDF file
        pdf_path = self.temp_path / "empty.pdf"
        pdf_path.touch()
        
        with pytest.raises(ValueError, match="No pages found in PDF"):
            PDFConverter.pdf_to_images(pdf_path)
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_rgba_to_jpeg(self, mock_convert):
        """Test PDF to images conversion with RGBA to JPEG conversion."""
        # Mock PDF with RGBA image
        mock_images = [Image.new('RGBA', (100, 100), (255, 0, 0, 128))]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Convert to JPEG (should handle RGBA properly)
        result_paths = PDFConverter.pdf_to_images(
            pdf_path, self.temp_path, output_format='JPEG'
        )
        
        # Verify file was created and is RGB
        assert len(result_paths) == 1
        with Image.open(result_paths[0]) as img:
            assert img.mode == 'RGB'
    
    @patch('image_converter.convert_from_path')
    def test_pdf_to_images_creates_output_directory(self, mock_convert):
        """Test PDF to images conversion creates output directory if it doesn't exist."""
        # Mock PDF conversion
        mock_images = [Image.new('RGB', (100, 100), (255, 0, 0))]
        mock_convert.return_value = mock_images
        
        # Create fake PDF file
        pdf_path = self.temp_path / "test.pdf"
        pdf_path.touch()
        
        # Use non-existent output directory
        output_dir = self.temp_path / "new_directory"
        
        # Convert
        result_paths = PDFConverter.pdf_to_images(pdf_path, output_dir)
        
        # Verify directory was created and file exists
        assert output_dir.exists()
        assert output_dir.is_dir()
        assert len(result_paths) == 1
        assert Path(result_paths[0]).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])