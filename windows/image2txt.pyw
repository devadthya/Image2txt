import os
import sys
from PIL import Image, ImageGrab, ImageOps
import pytesseract
import pyperclip
from win11toast import toast

# Explicit fallback path for Tesseract OCR on Windows
TESS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESS_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESS_PATH

def notify(title, message):
    try:
        toast(title, message, duration='short')
    except Exception:
        pass

def preprocess_image(img):
    # 1. Convert to grayscale to remove subpixel/ClearType color fringing
    gray = img.convert('L')

    # 2. Upscale small snips so letter heights meet Tesseract's 30px target
    w, h = gray.size
    scale = 1
    if h < 60 or w < 150:
        scale = 3
    elif h < 120 or w < 300:
        scale = 2

    if scale > 1:
        gray = gray.resize((w * scale, h * scale), Image.Resampling.LANCZOS)

    # 3. Add a clean margin border around the text (helps boundary detection)
    padded = ImageOps.expand(gray, border=15, fill='black' if is_dark(gray) else 'white')
    return padded

def is_dark(img):
    # Quick sample to check if the image has a dark background
    sample = img.resize((10, 10))
    avg_brightness = sum(sample.getdata()) / 100
    return avg_brightness < 128

def extract_text(img):
    processed = preprocess_image(img)

    # First attempt: assume single uniform block of text (--psm 6)
    text = pytesseract.image_to_string(processed, config='--psm 6').strip()
    if text:
        return text

    # Second attempt: sparse text / single word / line fallback (--psm 11)
    text = pytesseract.image_to_string(processed, config='--psm 11').strip()
    if text:
        return text

    # Third attempt: default mode on original image as last resort
    return pytesseract.image_to_string(img).strip()

def main():
    content = ImageGrab.grabclipboard()

    img = None
    if isinstance(content, Image.Image):
        img = content
    elif isinstance(content, list) and content:
        try:
            img = Image.open(content[0])
        except Exception:
            notify("Image2Txt", "Copied file is not a supported image.")
            return
    else:
        notify("Image2Txt", "No image found in clipboard.")
        return

    try:
        extracted = extract_text(img)
        if not extracted:
            notify("Image2Txt", "No text detected in image.")
            return

        pyperclip.copy(extracted)
        
        snippet = extracted.replace("\n", " ")[:45]
        notify("Text Ready!", f"Copied: {snippet}...")
    except Exception as e:
        notify("OCR Error", str(e))

if __name__ == "__main__":
    main()
