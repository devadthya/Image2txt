# Image2txt (✿◡‿◡)

A lightweight, zero-flash one-shot OCR tool for Linux (Wayland & X11) and Windows 11. Copy or screenshot an image, and it will immediately parse the text right into your clipboard! >///<

## :P Requirements

### Linux
Make sure your package manager has Tesseract and wl-clipboard installed:
- **Fedora / Nobara:** `sudo dnf install tesseract tesseract-osd wl-clipboard`
- **Arch Linux:** `sudo pacman -S tesseract tesseract-data-eng wl-clipboard`
- **Ubuntu / Debian:** `sudo apt install tesseract-ocr wl-clipboard xclip`

### Windows
- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (default path: `C:\Program Files\Tesseract-OCR`)
- Install [AutoHotkey v2](https://www.autohotkey.com/)
- Python dependencies: `pip install pytesseract pillow pyperclip win11toast`

---

## Quick Install

### Linux
```bash
git clone [https://github.com/devadthya/image2txt.git](https://github.com/devadthya/image2txt.git)
cd image2txt/linux
chmod +x install.sh
./install.sh













