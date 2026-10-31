#!/bin/sh
# Renders og.png (link preview, 1200x630) and apple-touch-icon.png (180x180)
# from scripts/og.html with a headless Chrome. Set CHROME to its executable.
set -e
cd "$(dirname "$0")/.."
CHROME=${CHROME:-$(ls ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell | head -1)}
render() { # url size out
  "$CHROME" --no-sandbox --hide-scrollbars --virtual-time-budget=3000 \
    --window-size="$2" --screenshot="$3" "$1" >/dev/null 2>&1
}
render "file://$PWD/scripts/og.html" 1200,630 og.png
render "file://$PWD/scripts/og.html#icon" 180,180 apple-touch-icon.png
echo "og.png, apple-touch-icon.png"
