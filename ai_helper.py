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
        
        # Use Gemini Pro Vision (or gemini-1.5-flash which is faster/cheaper)
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
