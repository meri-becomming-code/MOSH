"""
Quick fix script to update all .pptx links to .html in an extracted Canvas course.
Run this on your already-extracted course folder to fix broken PowerPoint links.
"""

import os
import re
import sys

def fix_pptx_links(root_dir):
    """Update all .pptx links to .html throughout the course."""
    
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory")
        return
    
    print(f"Scanning for broken PowerPoint links in: {root_dir}\n")
    
    files_updated = 0
    links_fixed = 0
    
    # Walk through all HTML files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith('.html'):
                continue
            
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Pattern 1: Fix href links from .pptx to .html
                # Matches: href="...something.pptx?params" or href="...something.pptx"
                pattern1 = r'(href="[^"]*/)([^/"]+)\.pptx(\?[^"]*")'
                matches = re.findall(pattern1, content)
                if matches:
                    content = re.sub(pattern1, r'\1\2.html\3', content)
                    links_fixed += len(matches)
                
                # Pattern 2: Fix href without query params
                pattern2 = r'(href="[^"]*/)([^/"]+)\.pptx(")'
                matches2 = re.findall(pattern2, content)
                if matches2:
                    content = re.sub(pattern2, r'\1\2.html\3', content)
                    links_fixed += len(matches2)
                
                # Pattern 3: Fix link text (PPTX) -> (HTML) with readable names
                pattern3 = r'>([^<]*?)([A-Za-z0-9_-]+)\s*\(PPTX\)</a>'
                def make_readable(match):
                    prefix = match.group(1)
                    filename = match.group(2)
                    # Replace underscores with spaces for readability
                    readable = filename.replace('_', ' ')
                    return f'>{prefix}{readable} (HTML)</a>'
                
                content = re.sub(pattern3, make_readable, content)
                
                # Save if changed
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_updated += 1
                    print(f"  ✓ Updated: {os.path.relpath(filepath, root_dir)}")
                    
            except Exception as e:
                print(f"  ✗ Error processing {file}: {e}")
    
    print(f"\n{'='*60}")
    print(f"COMPLETE!")
    print(f"  Files updated: {files_updated}")
    print(f"  Links fixed: {links_fixed}")
    print(f"{'='*60}\n")
    print("Next steps:")
    print("  1. Repackage your course using the toolkit")
    print("  2. Import the fixed .imscc file into Canvas")
    print("  3. Verify links work!\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        course_dir = sys.argv[1]
    else:
        # Default to current directory
        course_dir = input("Enter path to extracted Canvas course folder: ").strip()
    
    fix_pptx_links(course_dir)
