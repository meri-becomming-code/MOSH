import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def is_remote(url):
    return url.startswith('http://') or url.startswith('https://')

def check_link(url, base_path=None):
    """
    Checks if a link is valid (local or remote).
    Returns: (is_valid, status_message)
    """
    if not url or url.startswith('#') or url.startswith('mailto:'):
        return True, "Internal/Special"

    if is_remote(url):
        try:
            # Check URL with urllib
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return True, f"OK ({response.status})"
        except Exception as e:
            # Some servers block HEAD, try GET with small byte range or just try open
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    return True, f"OK ({response.status})"
            except Exception as e2:
                return False, f"Broken ({str(e2)})"
    else:
        # Local link
        if not base_path:
            return False, "No base path for local check"
        
        # Strip query params/hash
        clean_url = url.split('?')[0].split('#')[0]
        # Handle Canvas tokens
        clean_url = clean_url.replace('$IMS-CC-FILEBASE$/', '')
        
        full_path = os.path.normpath(os.path.join(os.path.dirname(base_path), clean_url))
        if os.path.exists(full_path):
            return True, "File exists"
        else:
            # Fuzzy check in web_resources
            target_name = os.path.basename(clean_url)
            # Find the root of the project (parent of web_resources usually)
            search_root = os.path.dirname(base_path)
            while not os.path.exists(os.path.join(search_root, 'web_resources')) and len(search_root) > 3:
                search_root = os.path.dirname(search_root)
            
            res_path = os.path.join(search_root, 'web_resources')
            if os.path.exists(res_path):
                for root, dirs, files in os.walk(res_path):
                    if target_name in files:
                        return True, "File exists in web_resources"
                        
            return False, f"Missing File: {target_name}"

def audit_directory(directory, io_handler=None):
    """Scans all HTML files in a directory for broken links."""
    report = []
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html'):
                html_files.append(os.path.join(root, file))

    total = len(html_files)
    for idx, fpath in enumerate(html_files):
        if io_handler and io_handler.is_stopped(): break
        
        fname = os.path.relpath(fpath, directory)
        if io_handler:
            io_handler.log(f"[{idx+1}/{total}] Auditing: {fname}")
        
        with open(fpath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                valid, msg = check_link(href, fpath)
                if not valid:
                    report.append({
                        'file': fname,
                        'link': href,
                        'text': link.get_text(strip=True)[:30],
                        'issue': msg
                    })
                    if io_handler:
                        io_handler.log(f"   [BROKEN] {href} -> {msg}")

    return report
