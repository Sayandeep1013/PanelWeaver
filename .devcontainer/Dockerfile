FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# The base image ships a Yarn apt source whose signing key no longer
# verifies, which fails every apt-get update (and the sshd feature with it).
# ffmpeg: rendering. espeak-ng: Kokoro TTS phonemes. Noto CJK: Japanese text
# in subtitles and contact sheets.
RUN grep -rl dl.yarnpkg.com /etc/apt/sources.list.d/ | xargs -r rm -f \
    && apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg espeak-ng fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
