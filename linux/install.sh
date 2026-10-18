#!/usr/bin/env bash
set -e

INSTALL_BIN="$HOME/.local/bin"
APPLICATIONS_DIR="$HOME/.local/share/applications"

echo "==> Installing Python dependencies..."
pip install -r requirements.txt --quiet

echo "==> Setting up directories..."
mkdir -p "$INSTALL_BIN"
mkdir -p "$APPLICATIONS_DIR"

echo "==> Installing executable..."
cp image2txt.py "$INSTALL_BIN/image2txt"
chmod +x "$INSTALL_BIN/image2txt"

echo "==> Creating desktop entry..."
cat <<DESKTOP > "$APPLICATIONS_DIR/image2txt.desktop"
[Desktop Entry]
Type=Application
Name=Image2txt
Comment=One-shot clipboard text extractor >~<
Exec=$INSTALL_BIN/image2txt
Icon=accessories-character-map
Terminal=false
Categories=Utility;
DESKTOP

chmod +x "$APPLICATIONS_DIR/image2txt.desktop"
update-desktop-database "$APPLICATIONS_DIR" 2>/dev/null || true

echo "✓ (｡•̀ᴗ-)✧ All done! Run 'image2txt' or bind it to a custom hotkey."
