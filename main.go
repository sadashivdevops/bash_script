package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/gen2brain/go-fitz"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <pdf-file-path>")
		fmt.Println("This tool converts each page of a PDF to individual PNG images")
		os.Exit(1)
	}

	pdfPath := os.Args[1]

	// Check if file exists
	if _, err := os.Stat(pdfPath); os.IsNotExist(err) {
		log.Fatalf("PDF file does not exist: %s", pdfPath)
	}

	// Check if it's a PDF file
	if !strings.HasSuffix(strings.ToLower(pdfPath), ".pdf") {
		log.Fatalf("File must be a PDF: %s", pdfPath)
	}

	err := convertPDFToImages(pdfPath)
	if err != nil {
		log.Fatalf("Error converting PDF to images: %v", err)
	}

	fmt.Println("PDF conversion completed successfully!")
}

func convertPDFToImages(pdfPath string) error {
	// Open the PDF document
	doc, err := fitz.New(pdfPath)
	if err != nil {
		return fmt.Errorf("failed to open PDF: %w", err)
	}
	defer doc.Close()

	// Get the base name of the PDF file (without extension)
	baseName := strings.TrimSuffix(filepath.Base(pdfPath), filepath.Ext(pdfPath))

	// Create output directory
	outputDir := fmt.Sprintf("%s_images", baseName)
	err = os.MkdirAll(outputDir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create output directory: %w", err)
	}

	// Convert each page to an image
	for n := 0; n < doc.NumPage(); n++ {
		// Get PNG bytes directly from the document
		pngBytes, err := doc.ImagePNG(n, 150.0) // 150 DPI for good quality
		if err != nil {
			return fmt.Errorf("failed to extract image from page %d: %w", n+1, err)
		}

		// Save the image as PNG
		outputPath := filepath.Join(outputDir, fmt.Sprintf("page_%03d.png", n+1))
		err = os.WriteFile(outputPath, pngBytes, 0644)
		if err != nil {
			return fmt.Errorf("failed to save PNG image %s: %w", outputPath, err)
		}

		fmt.Printf("Converted page %d to %s\n", n+1, outputPath)
	}

	fmt.Printf("All %d pages converted and saved to directory: %s\n", doc.NumPage(), outputDir)
	return nil
}
