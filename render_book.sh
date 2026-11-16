#!/bin/bash

# Script to render Quarto book with custom Chrome environment settings
# Fixes M1/Chromium crash issues by using system Chrome and specific flags.

export QUARTO_CHROMIUM="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
export QUARTO_CHROMIUM_HEADLESS_MODE=new
export QUARTO_NO_SANDBOX=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

echo "Starting render..."
quarto render
echo "Render complete."
