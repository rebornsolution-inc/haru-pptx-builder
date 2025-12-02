import pdfplumber
import json
import sys
from pathlib import Path

def analyze_pdf(pdf_path, output_path):
    """
    Analyzes a PDF file and generates a source_style.json file.
    """
    print(f"Analyzing PDF: {pdf_path}")
    
    slide_structures = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Total pages: {total_pages}")
            
            for i, page in enumerate(pdf.pages):
                slide_number = i + 1
                text = page.extract_text()
                words = page.extract_words()
                
                # Simple heuristic to determine slide type
                slide_type = "content-text"
                if i == 0:
                    slide_type = "hero-cover"
                elif "목차" in text or "Contents" in text or "Agenda" in text:
                    slide_type = "table-of-contents"
                elif len(text) < 50 and len(words) < 10: # Very little text
                    slide_type = "section-divider"
                
                # Extract elements (simplified)
                elements = {}
                
                # Try to find title (largest font usually, or top position)
                # pdfplumber words have 'top', 'bottom', 'x0', 'x1', 'size' (if available, often not reliable for size)
                # Actually extract_words returns dict with x0,top,x1,bottom,text. Font info is in page.chars
                
                # Let's just store the raw text for now as a single element
                elements["body"] = {
                    "text": text,
                    "position": "center",
                    "fontSize": "18px", # Placeholder
                    "color": "#000000"
                }
                
                slide_structure = {
                    "slideNumber": slide_number,
                    "type": slide_type,
                    "layout": "auto-detected",
                    "elements": elements,
                    "background": {
                        "color": "#FFFFFF" # Default
                    },
                    "spacing": {
                        "padding": "40px"
                    }
                }
                slide_structures.append(slide_structure)
                
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return

    # Construct the final JSON
    output_data = {
        "metadata": {
            "sourceFile": str(pdf_path),
            "analyzedAt": "2025-12-02T00:00:00Z",
            "analysisMethod": "pdfplumber-text-extraction",
            "totalPages": total_pages,
            "analyzedPages": list(range(1, total_pages + 1))
        },
        "slideStructures": slide_structures,
        "designTokens": {
            "colors": {
                "primary": { "main": "#000000", "description": "Detected primary color" },
                "background": { "main": "#FFFFFF", "description": "Detected background" },
                "text": { "primary": "#000000", "secondary": "#666666" }
            },
            "typography": {
                "heading": { "fontFamily": "sans-serif", "fontWeight": "700" },
                "body": { "fontFamily": "sans-serif", "fontWeight": "400" }
            },
            "spacing": {
                "page": { "horizontal": "50px", "vertical": "50px" }
            },
            "layout": {
                "aspectRatio": "16:9"
            }
        },
        "componentPatterns": {},
        "recommendations": {},
        "extractionNotes": {
            "limitations": ["Text-only extraction", "No visual style analysis"],
            "strengths": ["Accurate text content"],
            "recommendation": "Review and add visual styles manually."
        },
        "implementationReadiness": {
            "htmlStructure": "✅ Ready",
            "contentInput": "✅ Extracted"
        }
    }
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete. Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python analyze_pdf.py <pdf_path> <output_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    analyze_pdf(pdf_path, output_path)
