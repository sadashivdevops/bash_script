#!/usr/bin/env python3
"""
Example usage script for image and PDF conversion utilities.

This script demonstrates how to use the ImageConverter and PDFConverter classes.
"""

import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw
from image_converter import ImageConverter, PDFConverter


def create_sample_images():
    """Create sample images for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Creating sample images in: {temp_dir}")
    
    # Create a sample PNG with transparency
    png_path = temp_dir / "sample.png"
    png_img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(png_img)
    draw.rectangle([50, 50, 150, 150], fill=(255, 0, 0, 200))  # Semi-transparent red square
    draw.ellipse([75, 75, 125, 125], fill=(0, 255, 0, 255))  # Green circle
    png_img.save(png_path, 'PNG')
    print(f"Created PNG: {png_path}")
    
    # Create a sample JPG
    jpg_path = temp_dir / "sample.jpg" 
    jpg_img = Image.new('RGB', (200, 200), (135, 206, 235))  # Sky blue background
    draw = ImageDraw.Draw(jpg_img)
    draw.polygon([(100, 50), (150, 150), (50, 150)], fill=(255, 255, 0))  # Yellow triangle
    draw.text((80, 170), "JPG Sample", fill=(0, 0, 0))
    jpg_img.save(jpg_path, 'JPEG', quality=95)
    print(f"Created JPG: {jpg_path}")
    
    return temp_dir, png_path, jpg_path


def demonstrate_image_conversion():
    """Demonstrate image format conversion."""
    print("\n" + "="*60)
    print("DEMONSTRATING IMAGE CONVERSION")
    print("="*60)
    
    # Create sample images
    temp_dir, png_path, jpg_path = create_sample_images()
    
    try:
        # Convert PNG to JPG
        print(f"\n1. Converting PNG to JPG...")
        jpg_converted = ImageConverter.png_to_jpg(png_path)
        print(f"   Original PNG: {png_path}")
        print(f"   Converted JPG: {jpg_converted}")
        print(f"   JPG file exists: {Path(jpg_converted).exists()}")
        
        # Convert JPG to PNG
        print(f"\n2. Converting JPG to PNG...")
        png_converted = ImageConverter.jpg_to_png(jpg_path)
        print(f"   Original JPG: {jpg_path}")
        print(f"   Converted PNG: {png_converted}")
        print(f"   PNG file exists: {Path(png_converted).exists()}")
        
        # Display file sizes
        print(f"\n3. File size comparison:")
        print(f"   Original PNG: {png_path.stat().st_size} bytes")
        print(f"   Converted JPG: {Path(jpg_converted).stat().st_size} bytes")
        print(f"   Original JPG: {jpg_path.stat().st_size} bytes") 
        print(f"   Converted PNG: {Path(png_converted).stat().st_size} bytes")
        
        return temp_dir
        
    except Exception as e:
        print(f"Error during image conversion: {e}")
        return temp_dir


def create_sample_pdf():
    """Create a sample PDF using reportlab (if available) or use mock data."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        temp_dir = Path(tempfile.mkdtemp())
        pdf_path = temp_dir / "sample.pdf"
        
        # Create a simple PDF with 3 pages
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        
        # Page 1
        c.drawString(100, 750, "This is Page 1")
        c.drawString(100, 700, "Sample PDF for conversion testing")
        c.rect(100, 600, 200, 100, fill=1)
        c.showPage()
        
        # Page 2
        c.drawString(100, 750, "This is Page 2")
        c.circle(200, 650, 50, fill=1)
        c.showPage()
        
        # Page 3
        c.drawString(100, 750, "This is Page 3")
        c.drawString(100, 700, "Final page of the sample PDF")
        c.showPage()
        
        c.save()
        print(f"Created sample PDF: {pdf_path}")
        return temp_dir, pdf_path
        
    except ImportError:
        print("reportlab not available, skipping PDF creation demo")
        print("In a real scenario, you would have actual PDF files to convert")
        return None, None


def demonstrate_pdf_conversion():
    """Demonstrate PDF to image conversion."""
    print("\n" + "="*60)
    print("DEMONSTRATING PDF CONVERSION")
    print("="*60)
    
    # Try to create a sample PDF
    temp_dir, pdf_path = create_sample_pdf()
    
    if pdf_path is None:
        print("Skipping PDF conversion demo (no sample PDF available)")
        return None
    
    try:
        # Convert PDF to PNG images
        print(f"\n1. Converting PDF to PNG images...")
        png_images = PDFConverter.pdf_to_images(pdf_path, temp_dir, output_format='PNG')
        print(f"   Source PDF: {pdf_path}")
        print(f"   Generated {len(png_images)} PNG images:")
        for i, img_path in enumerate(png_images, 1):
            print(f"     Page {i}: {img_path}")
        
        # Convert PDF to JPG images with higher DPI
        print(f"\n2. Converting PDF to JPG images (300 DPI)...")
        jpg_images = PDFConverter.pdf_to_images(
            pdf_path, temp_dir, output_format='JPEG', dpi=300
        )
        print(f"   Generated {len(jpg_images)} JPG images:")
        for i, img_path in enumerate(jpg_images, 1):
            print(f"     Page {i}: {img_path}")
        
        # Display file information
        print(f"\n3. Generated file information:")
        for img_path in png_images + jpg_images:
            path = Path(img_path)
            if path.exists():
                with Image.open(path) as img:
                    print(f"   {path.name}: {img.size[0]}x{img.size[1]}, {img.mode}, {path.stat().st_size} bytes")
        
        return temp_dir
        
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
        return temp_dir


def main():
    """Main demonstration function."""
    print("Image and PDF Conversion Utility Demo")
    print("="*60)
    
    # Demonstrate image conversion
    img_temp_dir = demonstrate_image_conversion()
    
    # Demonstrate PDF conversion
    pdf_temp_dir = demonstrate_pdf_conversion()
    
    print("\n" + "="*60)
    print("DEMO COMPLETED")
    print("="*60)
    
    if img_temp_dir:
        print(f"\nImage conversion files are in: {img_temp_dir}")
    if pdf_temp_dir:
        print(f"PDF conversion files are in: {pdf_temp_dir}")
    
    print("\nTo use the library in your own code:")
    print("from image_converter import ImageConverter, PDFConverter")
    print("")
    print("# Convert PNG to JPG")
    print("ImageConverter.png_to_jpg('input.png', 'output.jpg')")
    print("")
    print("# Convert JPG to PNG") 
    print("ImageConverter.jpg_to_png('input.jpg', 'output.png')")
    print("")
    print("# Convert PDF to images")
    print("PDFConverter.pdf_to_images('document.pdf', 'output_dir/', 'PNG', dpi=200)")


if __name__ == "__main__":
    main()