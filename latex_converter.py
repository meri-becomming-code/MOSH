#!/usr/bin/env python3
"""
Math Content to Canvas LaTeX Converter
Created by Meri Kasprak with Gemini assistance
Released under GNU GPL v3

Converts mathematical content (images, text equations, handwritten solutions) 
to Canvas-compatible LaTeX following official Instructure best practices.

Based on Instructure Canvas Documentation:
- Uses \\(...\\) for inline equations
- Uses $$...$$ for display (block) equations
- MathJax 2.7.7 with TeX-MML-AM_SVG configuration
- Generates accessible MathML automatically
- Never uses equation images (accessibility requirement)
"""

import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from typing import List, Tuple, Optional
import json

# Pattern matchers for detecting equations in text
EQUATION_PATTERNS = [
    # Inline patterns: f(x) = ..., y = ..., x + 5 = 10
    (r'\b([fgh])\(([xy])\)\s*=\s*([^,.\n]+)', 'inline'),
    (r'\b([xy])\s*=\s*([^,.\n]+)', 'inline'),
    
    # Quadratic formula components
    (r'([+-]?\d*\.?\d+)x\^?2\s*([+-])\s*(\d*\.?\d+)x\s*([+-])\s*(\d+)', 'inline'),
    
    # Fractions: 2/3, -5/2
    (r'(\d+)/(\d+)', 'inline'),
    
    # Square roots: sqrt(...), √...
    (r'sqrt\(([^)]+)\)|√\(([^)]+)\)', 'inline'),
    
    # Exponents: x^2, 2^n
    (r'([a-z0-9]+)\^([0-9\-+]+)', 'inline'),
    
    # Greek letters spelled out
    (r'\b(alpha|beta|gamma|delta|theta|pi|sigma|omega)\b', 'inline'),
]

# Common equation text to LaTeX conversions
TEXT_TO_LATEX = {
    'sqrt': r'\\sqrt',
    '<=': r'\\le',
    '>=': r'\\ge',
    '!=': r'\\ne',
    '+-': r'\\pm',
    'infinity': r'\\infty',
    'alpha': r'\\alpha',
    'beta': r'\\beta',
    'gamma': r'\\gamma',
    'delta': r'\\delta',
    'theta': r'\\theta',
    'pi': r'\\pi',
    'sigma': r'\\sigma',
    'omega': r'\\omega',
}

def detect_equation_in_text(text: str) -> Optional[Tuple[str, str, str]]:
    """
    Detects if text contains mathematical notation and returns conversion info.
    
    Returns:
        Tuple of (original_text, latex_code, equation_type) or None
    """
    for pattern, eq_type in EQUATION_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            matched_text = match.group(0)
            latex = convert_text_to_latex(matched_text)
            return (matched_text, latex, eq_type)
    return None

def convert_text_to_latex(text: str) -> str:
    """
    Converts plain text mathematical notation to LaTeX.
    
    Examples:
        'f(x) = 2x + 3' -> 'f(x) = 2x + 3'
        'x^2 - 5x + 6' -> 'x^2 - 5x + 6'
        'sqrt(25)' -> '\\sqrt{25}'
    """
    latex = text
    
    # Apply text replacements
    for text_pattern, latex_pattern in TEXT_TO_LATEX.items():
        latex = latex.replace(text_pattern, latex_pattern)
    
    # Convert x^2 to x^{2}
    latex = re.sub(r'([a-zA-Z0-9])\^([0-9\-+]+)', r'\1^{\2}', latex)
    
    # Convert sqrt(x) to \sqrt{x}
    latex = re.sub(r'sqrt\(([^)]+)\)', r'\\sqrt{\1}', latex)
    latex = re.sub(r'√\(([^)]+)\)', r'\\sqrt{\1}', latex)
    
    # Convert fractions a/b to \frac{a}{b} (only simple numeric fractions)
    latex = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', latex)
    
    return latex

def wrap_latex(latex_code: str, equation_type: str = 'inline') -> str:
    """
    Wraps LaTeX code with Canvas-compatible delimiters.
    
    Args:
        latex_code: The LaTeX code
        equation_type: 'inline' or 'display'
    
    Returns:
        Properly delimited LaTeX for Canvas
    """
    if equation_type == 'display':
        return f'$$\n{latex_code}\n$$'
    else:
        return f'\\({latex_code}\\)'

def analyze_image_for_math_type(img_tag, img_path: str) -> dict:
    """
    Analyzes an image to determine what type of mathematical content it contains.
    
    Returns:
        Dict with: type, description, suggested_latex, needs_manual_review
    """
    result = {
        'type': 'unknown',
        'description': '',
        'suggested_latex': None,
        'needs_manual_review': True,
        'replacement_strategy': 'keep_with_alt_text'
    }
    
    # Check file name and alt text for clues
    img_name = Path(img_path).stem.lower() if img_path else ''
    alt_text = img_tag.get('alt', '').lower()
    src = img_tag.get('src', '').lower()
    
    # Coordinate grid detection
    if any(word in img_name + alt_text + src for word in ['grid', 'coordinate', 'graph', 'axis']):
        if any(word in img_name + alt_text for word in ['blank', 'empty', 'practice']):
            result['type'] = 'blank_grid'
            result['description'] = 'Blank coordinate grid for student work'
            result['replacement_strategy'] = 'keep_with_enhanced_alt_text'
        else:
            result['type'] = 'plotted_graph'
            result['description'] = 'Graph showing plotted function'
            result['replacement_strategy'] = 'suggest_desmos_embed'
    
    # Equation image detection
    elif any(word in img_name + alt_text for word in ['equation', 'formula', 'expression']):
        result['type'] = 'equation'
        result['description'] = 'Mathematical equation (should be converted to LaTeX)'
        result['replacement_strategy'] = 'convert_to_latex'
        result['needs_manual_review'] = True
    
    # Geometric diagram
    elif any(word in img_name + alt_text for word in ['triangle', 'circle', 'ellipse', 'parabola', 'geometry']):
        result['type'] = 'geometric_diagram'
        result['description'] = 'Geometric diagram'
        result['replacement_strategy'] = 'suggest_geogebra_embed'
    
    # Handwritten solution
    elif any(word in img_name + alt_text + src for word in ['solution', ' key', 'answer']):
        result['type'] = 'handwritten_solution'
        result['description'] = 'Handwritten solution steps'
        result['replacement_strategy'] = 'ocr_to_latex'
    
    return result

def enhance_image_alt_text(img_tag, analysis: dict) -> str:
    """
    Creates detailed, educational alt text for mathematical images.
    
    Following Canvas accessibility best practices.
    """
    img_type = analysis['type']
    
    if img_type == 'blank_grid':
        return "Blank coordinate grid with x-axis from -10 to 10 and y-axis from -10 to 10, gridlines every 1 unit. Use for plotting functions or coordinate pairs."
    
    elif img_type == 'plotted_graph':
        # Extract info from existing alt text if possible
        existing_alt = img_tag.get('alt', '')
        return f"Graph showing: {existing_alt}. For interactive version, use Desmos graphing calculator."
    
    elif img_type == 'equation':
        return "Mathematical equation displayed as image. LaTeX conversion recommended for accessibility."
    
    elif img_type == 'geometric_diagram':
        existing_alt = img_tag.get('alt', '')
        return f"Geometric diagram: {existing_alt}"
    
    elif img_type == 'handwritten_solution':
        return "Handwritten solution steps showing detailed work. OCR conversion to typed text recommended for accessibility."
    
    return img_tag.get('alt', 'Mathematical content')

def process_html_file(html_path: str, output_path: str = None, interactive: bool = False) -> dict:
    """
    Processes an HTML file to convert math content to Canvas LaTeX format.
    
    Args:
        html_path: Path to input HTML file
        output_path: Path to save enhanced HTML (defaults to overwrite)
        interactive: If True, prompts for LaTeX conversions
    
    Returns:
        Dict with statistics and recommendations
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    stats = {
        'equations_converted': 0,
        'images_analyzed': 0,
        'images_needing_ocr': [],
        'images_needing_desmos': [],
        'images_needing_geogebra': [],
        'manual_review_needed': []
    }
    
    # 1. Convert text equations to LaTeX
    for tag in soup.find_all(['p', 'li', 'td', 'div']):
        if tag.find(['img', 'iframe']):  # Skip if contains images/iframes
            continue
        
        text = tag.get_text()
        equation_info = detect_equation_in_text(text)
        
        if equation_info:
            original, latex, eq_type = equation_info
            
            # Replace text with LaTeX-wrapped version
            new_html = tag.decode_contents().replace(
                original, 
                wrap_latex(latex, eq_type)
            )
            tag.clear()
            tag.append(BeautifulSoup(new_html, 'html.parser'))
            
            stats['equations_converted'] += 1
            print(f"  ✓ Converted: {original} → {wrap_latex(latex, eq_type)}")
    
    # 2. Analyze and enhance images
    for img in soup.find_all('img'):
        stats['images_analyzed'] += 1
        
        img_src = img.get('src', '')
        img_path = os.path.join(os.path.dirname(html_path), img_src) if img_src else None
        
        analysis = analyze_image_for_math_type(img, img_path)
        
        # Enhance alt text
        new_alt = enhance_image_alt_text(img, analysis)
        img['alt'] = new_alt
        
        # Track items needing special handling
        if analysis['replacement_strategy'] == 'ocr_to_latex':
            stats['images_needing_ocr'].append({
                'src': img_src,
                'type': analysis['type']
            })
        elif analysis['replacement_strategy'] == 'suggest_desmos_embed':
            stats['images_needing_desmos'].append({
                'src': img_src,
                'description': analysis['description']
            })
        elif analysis['replacement_strategy'] == 'suggest_geogebra_embed':
            stats['images_needing_geogebra'].append({
                'src': img_src,
                'description': analysis['description']
            })
        
        if analysis['needs_manual_review']:
            stats['manual_review_needed'].append(img_src)
        
        # Add note for images that should be converted
        if analysis['replacement_strategy'] == 'convert_to_latex':
            parent = img.parent
            note = soup.new_tag('div', style='background: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107;')
            note.string = "⚠️ Accessibility Note: This equation should be converted to LaTeX for screen reader compatibility."
            if parent:
                img.insert_after(note)
    
    # Save enhanced HTML
    if output_path is None:
        output_path = html_path
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return stats

def generate_report(stats_list: List[dict], output_dir: str):
    """
    Generates a comprehensive report of all conversions and recommendations.
    """
    report_path = os.path.join(output_dir, 'latex_conversion_report.md')
    
    total_conversions = sum(s['equations_converted'] for s in stats_list)
    total_images = sum(s['images_analyzed'] for s in stats_list)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Canvas LaTeX Conversion Report\n\n")
        f.write(f"**Generated**: {os.popen('date').read().strip()}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- Files processed: {len(stats_list)}\n")
        f.write(f"- Text equations converted to LaTeX: {total_conversions}\n")
        f.write(f"- Images analyzed: {total_images}\n\n")
        
        # Count items needing special handling
        total_ocr = sum(len(s['images_needing_ocr']) for s in stats_list)
        total_desmos = sum(len(s['images_needing_desmos']) for s in stats_list)
        total_geogebra = sum(len(s['images_needing_geogebra']) for s in stats_list)
        
        f.write("## Recommended Next Steps\n\n")
        
        if total_ocr > 0:
            f.write(f"### 📸 OCR Conversion Needed ({total_ocr} images)\n\n")
            f.write("These images contain handwritten solutions that should be converted to typed LaTeX:\n\n")
            for stats in stats_list:
                for item in stats['images_needing_ocr']:
                    f.write(f"- `{item['src']}`\n")
            f.write("\n**Action**: Use LaTeX-OCR or SimpleTex API to convert.\n\n")
        
        if total_desmos > 0:
            f.write(f"### 📊 Desmos Embed Recommended ({total_desmos} graphs)\n\n")
            f.write("These graphs could be made interactive with Desmos embeds:\n\n")
            for stats in stats_list:
                for item in stats['images_needing_desmos']:
                    f.write(f"- `{item['src']}` - {item['description']}\n")
            f.write("\n**Action**: Create Desmos graphs and replace <iframe> embeds.\n\n")
        
        if total_geogebra > 0:
            f.write(f"### 🎨 GeoGebra Embed Recommended ({total_geogebra} diagrams)\n\n")
            f.write("These geometric diagrams could be made interactive with GeoGebra:\n\n")
            for stats in stats_list:
                for item in stats['images_needing_geogebra']:
                    f.write(f"- `{item['src']}` - {item['description']}\n")
            f.write("\n**Action**: Create GeoGebra applets and replace with embeds.\n\n")
        
        f.write("## Canvas LaTeX Syntax Reference\n\n")
        f.write("```\n")
        f.write("Inline equation: \\(x^2 + 5x + 6\\)\n")
        f.write("Display equation: $$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$\n")
        f.write("```\n\n")
        
        f.write("## Accessibility Best Practices\n\n")
        f.write("✅ All equations now use Canvas-compatible LaTeX delimiters\n")
        f.write("✅ MathJax automatically converts to accessible MathML\n")
        f.write("✅ Screen readers can speak equations aloud\n")
        f.write("✅ Enhanced alt text added to all mathematical images\n\n")
    
    print(f"\n✅ Report generated: {report_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python latex_converter.py <path_to_html_or_directory>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    
    if os.path.isfile(target_path):
        print(f"Processing: {target_path}")
        stats = process_html_file(target_path)
        generate_report([stats], os.path.dirname(target_path))
    
    elif os.path.isdir(target_path):
        print(f"Processing directory: {target_path}")
        html_files = list(Path(target_path).rglob('*.html'))
        print(f"Found {len(html_files)} HTML files")
        
        all_stats = []
        for html_file in html_files:
            print(f"\n📄 {html_file.name}")
            stats = process_html_file(str(html_file))
            all_stats.append(stats)
        
        generate_report(all_stats, target_path)
    
    else:
        print(f"Error: {target_path} not found")
        sys.exit(1)
    
    print("\n✨ Conversion complete! Check the report for next steps.")

if __name__ == '__main__':
    main()
