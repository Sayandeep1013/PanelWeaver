#!/usr/bin/env bash
# Runs once when the codespace is created, as the codespace user. System
# packages belong in the Dockerfile; user-level tools go here.
set -euo pipefail

python -m pip install --upgrade pip

# Claude Code (native installer). Log in by running `claude` once.
curl -fsSL https://claude.ai/install.sh | bash

mkdir -p workspace renders
