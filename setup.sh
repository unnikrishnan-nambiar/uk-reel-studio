#!/bin/bash
# One-time setup on macOS (Intel or Apple Silicon). Run from the project folder:  ./setup.sh
set -e
cd "$(dirname "$0")"
if ! command -v brew >/dev/null; then
  echo "Installing Homebrew (asks for your Mac password)…"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/usr/local/bin/brew shellenv 2>/dev/null || /opt/homebrew/bin/brew shellenv)"
fi
brew install ffmpeg python@3.11 node git
PY=$(brew --prefix python@3.11)/bin/python3.11
[ -d .venv ] || $PY -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q numpy opencv-python soundfile playwright sherpa-onnx
.venv/bin/pip install -q onnxruntime || .venv/bin/pip install -q "onnxruntime==1.19.2"
.venv/bin/python -m playwright install chromium
mkdir -p models input output
B=https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models
if [ ! -f models/omni/tokens.txt ]; then
  echo "Downloading the speech model (about 1 GB, Malayalam + English + 1600 languages)…"
  curl -fL $B/sherpa-onnx-omnilingual-asr-1600-languages-1B-ctc-int8-2025-11-12.tar.bz2 | tar xj -C models
  mv models/sherpa-onnx-omnilingual-asr-1600-languages-1B-ctc-int8-2025-11-12 models/omni
fi
[ -s models/isnet-general-use.onnx ] || curl -fL -o models/isnet-general-use.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx
# Optional phone inbox in iCloud Drive: save videos from the iPhone Files app into "Reel Inbox"
IC="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
if [ -d "$IC" ]; then mkdir -p "$IC/Reel Inbox"; echo "iCloud inbox ready: iCloud Drive > Reel Inbox"; fi
chmod +x reel
echo; echo "Setup done. Now run:  claude   and say: edit the new video"
