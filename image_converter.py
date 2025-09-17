#!/usr/bin/env python3
"""
Image and PDF Conversion Tool

This module provides functionality to:
1. Convert between PNG and JPG image formats
2. Convert PDF files to individual image files (one per page)
"""

import os
import sys
import io
from pathlib import Path
from typing import List, Optional
import logging

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library not found. Install it using: pip install Pillow")
    sys.exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF library not found. Install it using: pip install PyMuPDF")
    sys.exit(1)


class ImageConverter:
    """Handles image format conversions and PDF to image conversions."""
    
    def __init__(self, quality: int = 95):
        """
        Initialize the ImageConverter.
        
        Args:
            quality (int): JPEG quality for conversions (1-100)
        """
        self.quality = max(1, min(100, quality))
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def convert_image_format(self, input_path: str, output_path: str, 
                           target_format: str = None) -> bool:
        """
        Convert image between PNG and JPG formats.
        
        Args:
            input_path (str): Path to input image file
            output_path (str): Path for output image file
            target_format (str): Target format ('PNG' or 'JPEG'). 
                               If None, inferred from output_path extension
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Validate input file exists
            if not os.path.exists(input_path):
                self.logger.error(f"Input file not found: {input_path}")
                return False
            
            # Open the image
            with Image.open(input_path) as img:
                # Determine target format
                if target_format is None:
                    ext = Path(output_path).suffix.lower()
                    if ext == '.png':
                        target_format = 'PNG'
                    elif ext in ['.jpg', '.jpeg']:
                        target_format = 'JPEG'
                    else:
                        self.logger.error(f"Unsupported output format: {ext}")
                        return False
                
                # Convert RGBA to RGB if saving as JPEG
                if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save the image
                save_kwargs = {}
                if target_format == 'JPEG':
                    save_kwargs['quality'] = self.quality
                    save_kwargs['optimize'] = True
                
                img.save(output_path, format=target_format, **save_kwargs)
                
                self.logger.info(f"Successfully converted {input_path} to {output_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False
    
    def png_to_jpg(self, input_path: str, output_path: str) -> bool:
        """
        Convert PNG to JPG format.
        
        Args:
            input_path (str): Path to PNG file
            output_path (str): Path for output JPG file
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        return self.convert_image_format(input_path, output_path, 'JPEG')
    
    def jpg_to_png(self, input_path: str, output_path: str) -> bool:
        """
        Convert JPG to PNG format.
        
        Args:
            input_path (str): Path to JPG file
            output_path (str): Path for output PNG file
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        return self.convert_image_format(input_path, output_path, 'PNG')
    
    def pdf_to_images(self, pdf_path: str, output_dir: str, 
                     image_format: str = 'PNG', dpi: int = 150) -> List[str]:
        """
        Convert PDF pages to individual image files.
        
        Args:
            pdf_path (str): Path to PDF file
            output_dir (str): Directory to save image files
            image_format (str): Output image format ('PNG' or 'JPEG')
            dpi (int): Resolution for image conversion
        
        Returns:
            List[str]: List of created image file paths
        """
        output_files = []
        
        try:
            # Validate input file exists
            if not os.path.exists(pdf_path):
                self.logger.error(f"PDF file not found: {pdf_path}")
                return output_files
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Open PDF
            pdf_document = fitz.open(pdf_path)
            
            # Get base filename without extension
            base_name = Path(pdf_path).stem
            
            # Convert each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Render page to image
                matrix = fitz.Matrix(dpi/72, dpi/72)  # Convert DPI to scale
                pix = page.get_pixmap(matrix=matrix)
                
                # Determine file extension
                ext = '.png' if image_format.upper() == 'PNG' else '.jpg'
                
                # Create output filename
                output_filename = f"{base_name}_page_{page_num + 1:03d}{ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save image
                if image_format.upper() == 'PNG':
                    pix.save(output_path)
                else:
                    # For JPEG, we need to convert through PIL to handle quality
                    img_data = pix.tobytes("ppm")
                    img = Image.open(io.BytesIO(img_data))
                    img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                
                output_files.append(output_path)
                self.logger.info(f"Created: {output_path}")
            
            pdf_document.close()
            self.logger.info(f"Successfully converted {len(output_files)} pages from {pdf_path}")
            
        except Exception as e:
            self.logger.error(f"Error converting PDF {pdf_path}: {str(e)}")
        
        return output_files


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Image and PDF Conversion Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # PNG to JPG conversion
    png_to_jpg_parser = subparsers.add_parser('png-to-jpg', help='Convert PNG to JPG')
    png_to_jpg_parser.add_argument('input', help='Input PNG file path')
    png_to_jpg_parser.add_argument('output', help='Output JPG file path')
    png_to_jpg_parser.add_argument('--quality', type=int, default=95, 
                                  help='JPEG quality (1-100, default: 95)')
    
    # JPG to PNG conversion
    jpg_to_png_parser = subparsers.add_parser('jpg-to-png', help='Convert JPG to PNG')
    jpg_to_png_parser.add_argument('input', help='Input JPG file path')
    jpg_to_png_parser.add_argument('output', help='Output PNG file path')
    
    # PDF to images conversion
    pdf_to_images_parser = subparsers.add_parser('pdf-to-images', 
                                               help='Convert PDF to image files')
    pdf_to_images_parser.add_argument('input', help='Input PDF file path')
    pdf_to_images_parser.add_argument('output_dir', help='Output directory for images')
    pdf_to_images_parser.add_argument('--format', choices=['PNG', 'JPEG'], 
                                    default='PNG', help='Output image format')
    pdf_to_images_parser.add_argument('--dpi', type=int, default=150, 
                                    help='DPI for image conversion (default: 150)')
    pdf_to_images_parser.add_argument('--quality', type=int, default=95, 
                                    help='JPEG quality (1-100, default: 95)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create converter instance
    quality = getattr(args, 'quality', 95)
    converter = ImageConverter(quality=quality)
    
    # Execute command
    if args.command == 'png-to-jpg':
        success = converter.png_to_jpg(args.input, args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'jpg-to-png':
        success = converter.jpg_to_png(args.input, args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'pdf-to-images':
        dpi = getattr(args, 'dpi', 150)
        output_files = converter.pdf_to_images(
            args.input, args.output_dir, args.format, dpi
        )
        if output_files:
            print(f"Successfully created {len(output_files)} image files:")
            for file_path in output_files:
                print(f"  {file_path}")
            sys.exit(0)
        else:
            print("Failed to convert PDF to images")
            sys.exit(1)


if __name__ == '__main__':
    main()