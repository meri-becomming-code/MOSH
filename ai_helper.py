# Created by Meri Kasprak with the assistance of Gemini.
# Released freely under the GNU General Public License version 3. USE AT YOUR OWN RISK.

import os
import google.generativeai as genai
from PIL import Image

def generate_alt_text(image_path, api_key):
    """
    Generates alt text for an image using Google Gemini API.
    Returns: (text, error_message)
    """
    if not api_key:
        return None, "No API Key provided. Please set it in Settings."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        img = Image.open(image_path)
        
        prompt = (
            "Describe this image for a blind user (Alt Text). "
            "Be concise, neutral, and descriptive. "
            "Do not start with 'Image of' or 'Picture of'. "
            "If it contains text, transcribe it. "
            "Max 1-2 sentences."
        )
        
        response = model.generate_content([prompt, img])
        return response.text.strip(), None
        
    except Exception as e:
        return None, str(e)

def batch_generate_alt_text(image_paths, api_key, progress_callback=None):
    """
    Generates alt text for multiple images.
    progress_callback: function(current, total, filename, result)
    """
    results = {}
    total = len(image_paths)
    for i, path in enumerate(image_paths):
        fname = os.path.basename(path)
        text, err = generate_alt_text(path, api_key)
        results[fname] = text if not err else f"[Error: {err}]"
        if progress_callback:
            progress_callback(i + 1, total, fname, results[fname])
    return results
