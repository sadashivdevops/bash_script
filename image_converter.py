"""
Image and PDF conversion utilities.

This module provides functionality to:
1. Convert between image formats (PNG, JPG)
2. Convert PDF pages to individual images
"""

import os
from pathlib import Path
from typing import List, Optional, Union
from PIL import Image
from pdf2image import convert_from_path


class ImageConverter:
    """Handles image format conversions between PNG and JPG."""
    
    @staticmethod
    def png_to_jpg(input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> str:
        """
        Convert PNG image to JPG format.
        
        Args:
            input_path: Path to the input PNG file
            output_path: Path for the output JPG file. If None, uses input filename with .jpg extension
            
        Returns:
            str: Path to the converted JPG file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file is not a valid PNG image
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if output_path is None:
            output_path = input_path.with_suffix('.jpg')
        else:
            output_path = Path(output_path)
        
        try:
            # Open PNG image and convert to RGB (JPG doesn't support transparency)
            with Image.open(input_path) as img:
                if img.format != 'PNG':
                    raise ValueError(f"Input file is not a PNG image: {input_path}")
                
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save as JPG
                img.save(output_path, 'JPEG', quality=95)
                
        except Exception as e:
            raise ValueError(f"Error converting PNG to JPG: {str(e)}")
        
        return str(output_path)
    
    @staticmethod
    def jpg_to_png(input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> str:
        """
        Convert JPG image to PNG format.
        
        Args:
            input_path: Path to the input JPG file
            output_path: Path for the output PNG file. If None, uses input filename with .png extension
            
        Returns:
            str: Path to the converted PNG file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file is not a valid JPG image
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if output_path is None:
            output_path = input_path.with_suffix('.png')
        else:
            output_path = Path(output_path)
        
        try:
            with Image.open(input_path) as img:
                if img.format not in ('JPEG', 'JPG'):
                    raise ValueError(f"Input file is not a JPG image: {input_path}")
                
                # Save as PNG
                img.save(output_path, 'PNG')
                
        except Exception as e:
            raise ValueError(f"Error converting JPG to PNG: {str(e)}")
        
        return str(output_path)


class PDFConverter:
    """Handles PDF to image conversions."""
    
    @staticmethod
    def pdf_to_images(input_path: Union[str, Path], 
                     output_dir: Optional[Union[str, Path]] = None,
                     output_format: str = 'PNG',
                     dpi: int = 200) -> List[str]:
        """
        Convert each page of a PDF to individual images.
        
        Args:
            input_path: Path to the input PDF file
            output_dir: Directory for output images. If None, uses input file directory
            output_format: Output image format ('PNG' or 'JPEG')
            dpi: Resolution for the output images
            
        Returns:
            List[str]: List of paths to the generated image files
            
        Raises:
            FileNotFoundError: If input PDF file doesn't exist
            ValueError: If PDF cannot be processed or invalid format specified
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input PDF file not found: {input_path}")
        
        if output_format.upper() not in ('PNG', 'JPEG', 'JPG'):
            raise ValueError(f"Unsupported output format: {output_format}")
        
        if output_dir is None:
            output_dir = input_path.parent
        else:
            output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(input_path, dpi=dpi)
            
            if not images:
                raise ValueError(f"No pages found in PDF: {input_path}")
            
            output_paths = []
            base_name = input_path.stem
            
            for i, image in enumerate(images, 1):
                # Generate output filename
                if output_format.upper() == 'JPEG' or output_format.upper() == 'JPG':
                    ext = 'jpg'
                    format_name = 'JPEG'
                else:
                    ext = 'png'
                    format_name = 'PNG'
                
                output_path = output_dir / f"{base_name}_page_{i:03d}.{ext}"
                
                # Convert and save image
                if format_name == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
                    # Convert to RGB for JPEG
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                    image = background
                
                image.save(output_path, format_name, quality=95 if format_name == 'JPEG' else None)
                output_paths.append(str(output_path))
            
            return output_paths
            
        except Exception as e:
            raise ValueError(f"Error converting PDF to images: {str(e)}")


def main():
    """Example usage of the conversion functions."""
    print("Image and PDF Converter")
    print("=" * 50)
    
    # Example usage would go here
    print("Available functions:")
    print("- ImageConverter.png_to_jpg(input_path, output_path)")
    print("- ImageConverter.jpg_to_png(input_path, output_path)")
    print("- PDFConverter.pdf_to_images(input_path, output_dir, output_format, dpi)")


if __name__ == "__main__":
    main()