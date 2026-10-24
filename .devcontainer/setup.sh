#!/usr/bin/env bash
# Runs once when the codespace is created. Anything the pipeline needs at
# system level goes here, so every new codespace starts complete.
set -euo pipefail

sudo apt-get update
# ffmpeg: rendering. espeak-ng: Kokoro TTS phonemes. Noto CJK: Japanese text
# in subtitles and contact sheets.
sudo apt-get install -y --no-install-recommends ffmpeg espeak-ng fonts-noto-cjk
sudo rm -rf /var/lib/apt/lists/*

python -m pip install --upgrade pip

# Claude Code (native installer). Log in by running `claude` once.
curl -fsSL https://claude.ai/install.sh | bash

mkdir -p workspace renders
