#!/usr/bin/env python3
import shutil
import subprocess
import sys
import time
from io import BytesIO
from PIL import Image
import pytesseract

def notify(title, msg):
    if shutil.which("notify-send"):

        # Sends desktop notifications
        subprocess.run(
            ["notify-send", "-a", "(◡‿◡) Image2txt", "-i", "accessories-character-map", title, msg],
            check=False
        )

def get_clipboard_image():
    # Wayland native (KDE Plasma)
    if shutil.which("wl-paste"):
        res = subprocess.run(["wl-paste", "-t", "image/png"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if res.returncode == 0 and res.stdout:
            return res.stdout

    # X11 fallback
    if shutil.which("xclip"):
        res = subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-o"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if res.returncode == 0 and res.stdout:
            return res.stdout

    return None

def set_clipboard_text(text):
    if shutil.which("wl-copy"):
        p = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
        p.communicate(input=text.encode("utf-8"))
    if shutil.which("xclip"):
        p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
        p.communicate(input=text.encode("utf-8"))

def main():
    if not shutil.which("tesseract"):
        notify("uwaaa! (>~<)", "tesseract-ocr is missing! please install it first~")
        sys.exit(1)

    # Cute start notification
    notify(">///< take a snippet!", "snip or copy an image to your clipboard... O///O")

    timeout = 30
    start = time.time()

    while time.time() - start < timeout:
        raw_bytes = get_clipboard_image()
        if raw_bytes:
            try:
                img = Image.open(BytesIO(raw_bytes))
                text = pytesseract.image_to_string(img).strip()

                if text:
                    set_clipboard_text(text)
                    preview = text[:45].replace("\n", " ") + ("..." if len(text) > 45 else "")
                    # Cute success notification
                    notify("(｡•̀ᴗ-)✧ copied to clipboard!", f" {preview}")
                    sys.exit(0)
            except Exception:
                pass

        time.sleep(0.35)

    # timeout msg
    notify("O_O timed out...", "waited 30s but didn't see any image")

if __name__ == "__main__":
    main()
