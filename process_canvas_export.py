#!/usr/bin/env python3
"""
Canvas IMSCC Math Converter - Gemini-Powered
Created by Meri Kasprak with Gemini assistance
Released under GNU GPL v3

Processes a Canvas Common Cartridge (IMSCC) export and uses Gemini to convert
handwritten math PDFs to accessible LaTeX format.

Usage:
    python process_canvas_export.py "path/to/new-math-export_extracted"
"""

import os
import sys
from pathlib import Path
import json

try:
    from google import genai
    from PIL import Image
    from pdf2image import convert_from_path
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip install google-genai pillow pdf2image beautifulsoup4")
    sys.exit(1)

# Gemini conversion prompt
MATH_CONVERSION_PROMPT = """Convert ALL mathematical content in this image to Canvas-compatible LaTeX format.

RULES:
1. Use \\(...\\) for inline equations
2. Use $$...$$ for display equations
3. Preserve problem numbers and structure
4. Add <details><summary>Solution</summary>...</details> for solutions
5. Be 100% accurate

Return ready-to-paste HTML/LaTeX for Canvas."""

def setup_gemini():
    """Configure Gemini API."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("\n🔑 Gemini API Key Required")
        print("Get from: https://aistudio.google.com/app/apikey")
        api_key = input("Enter API key: ").strip()
        if not api_key:
            sys.exit(1)
    
    client = genai.Client(api_key=api_key)
    return client

def find_math_pdfs(export_dir: str):
    """Find all PDF note packets in web_resources."""
    web_resources = Path(export_dir) / 'web_resources'
    if not web_resources.exists():
        print(f"❌ No web_resources folder found in {export_dir}")
        return []
    
    pdfs = list(web_resources.glob('**/*.pdf'))
    print(f"📚 Found {len(pdfs)} PDF files")
    return pdfs

def convert_pdf_with_gemini(client, pdf_path: str, output_dir: str):
    """Convert a PDF to Canvas LaTeX using Gemini."""
    print(f"\n📄 Processing: {pdf_path.name}")
    
    # Convert PDF to images
    temp_dir = output_dir / f"{pdf_path.stem}_temp"
    temp_dir.mkdir(exist_ok=True)
    
    print("   Converting PDF to images...")
    try:
        images = convert_from_path(str(pdf_path), dpi=300, output_folder=str(temp_dir))
    except Exception as e:
        print(f"   ❌ Error converting PDF: {e}")
        return None
    
    print(f"   ✅ Created {len(images)} page images")
    
    # Process each page with Gemini
    all_content = []
    for i, img_path in enumerate(temp_dir.glob('*.png'), 1):
        print(f"   [{i}/{len(images)}] Converting page {i}...", end=' ', flush=True)
        
        try:
            img = Image.open(img_path)
            response = client.models.generate_content(
                model='gemini-1.5-pro',
                contents=[MATH_CONVERSION_PROMPT, img]
            )
            
            if response.text:
                all_content.append(f"\n<!-- Page {i} -->\n{response.text}\n")
                print("✅")
            else:
                print("⚠️ No response")
                
        except Exception as e:
            print(f"❌ {e}")
            all_content.append(f"\n<!-- Error on page {i}: {e} -->\n")
    
    # Clean up temp images
    for img in temp_dir.glob('*.png'):
        img.unlink()
    temp_dir.rmdir()
    
    return "\n".join(all_content)

def create_canvas_html_page(title: str, content: str):
    """Wrap content in Canvas-friendly HTML template."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #4b3190;
            border-bottom: 2px solid #4b3190;
            padding-bottom: 10px;
        }}
        details {{
            background: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #4b3190;
            border-radius: 4px;
        }}
        summary {{
            cursor: pointer;
            font-weight: bold;
            color: #4b3190;
        }}
        summary:hover {{
            color: #6b4fc0;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
"""
    return html

def process_canvas_export(export_dir: str):
    """Main processing function."""
    export_path = Path(export_dir)
    
    if not export_path.exists():
        print(f"❌ Directory not found: {export_dir}")
        sys.exit(1)
    
    print("🚀 Canvas Export Math Converter (Gemini-Powered)")
    print("="*60)
    print(f"📂 Processing: {export_path.name}\n")
    
    # Setup Gemini
    client = setup_gemini()
    print("✅ Gemini API configured\n")
    
    # Find PDFs
    pdfs = find_math_pdfs(export_dir)
    if not pdfs:
        print("❌ No PDF files found to convert")
        sys.exit(1)
    
    # Create output directory
    output_dir = export_path / "converted_pages"
    output_dir.mkdir(exist_ok=True)
    
    # Process each PDF
    stats = {'success': 0, 'failed': 0}
    
    for pdf in pdfs:
        latex_content = convert_pdf_with_gemini(client, pdf, output_dir)
        
        if latex_content:
            # Create HTML page
            title = pdf.stem.replace('_', ' ').title()
            html_content = create_canvas_html_page(title, latex_content)
            
            # Save HTML file
            html_filename = f"{pdf.stem}.html"
            html_path = output_dir / html_filename
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"   ✅ Saved: {html_filename}")
            stats['success'] += 1
        else:
            stats['failed'] += 1
    
    # Generate summary
    print("\n" + "="*60)
    print("✅ CONVERSION COMPLETE!")
    print(f"   Success: {stats['success']} files")
    if stats['failed'] > 0:
        print(f"   Failed: {stats['failed']} files")
    print(f"\n📁 Output location: {output_dir}")
    print("\n🎯 Next Steps:")
    print("   1. Review HTML files in converted_pages/")
    print("   2. Copy content into Canvas pages")
    print("   3. Verify LaTeX renders correctly")
    print("   4. Publish to students!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python process_canvas_export.py <path-to-extracted-imscc>")
        print("\nExample:")
        print('   python process_canvas_export.py "c:/Users/meri/Desktop/new-math-export_extracted"')
        sys.exit(1)
    
    process_canvas_export(sys.argv[1])
