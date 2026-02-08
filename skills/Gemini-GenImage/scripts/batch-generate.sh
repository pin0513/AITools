#!/bin/bash
#
# Batch Image Generation Script
# 批次生成多張圖片
#
# 使用方式:
#   ./batch-generate.sh config.json output_dir/
#
# config.json 格式:
# {
#   "images": [
#     {"filename": "hero.png", "prompt": "Tech background..."},
#     {"filename": "icon.png", "prompt": "Icon design..."}
#   ]
# }
#

set -e

SCRIPT_DIR="$(dirname "$0")"

# 檢查參數
if [ $# -lt 2 ]; then
    echo "Usage: $0 config.json output_dir/"
    echo ""
    echo "config.json format:"
    echo '{'
    echo '  "images": ['
    echo '    {"filename": "hero.png", "prompt": "Your prompt here"},'
    echo '    {"filename": "icon.png", "prompt": "Another prompt"}'
    echo '  ]'
    echo '}'
    exit 1
fi

CONFIG="$1"
OUTPUT_DIR="$2"

# 檢查 config 檔案
if [ ! -f "$CONFIG" ]; then
    echo "Error: Config file not found: $CONFIG"
    exit 1
fi

# 建立輸出目錄
mkdir -p "$OUTPUT_DIR"

# 檢查 API Key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set"
    exit 1
fi

echo "🎨 Starting batch image generation..."
echo ""

# 讀取 config 並逐一生成
python3 << EOF
import json
import subprocess
import os
import time

with open("$CONFIG") as f:
    config = json.load(f)

total = len(config.get("images", []))
success = 0
failed = 0

for i, img in enumerate(config.get("images", []), 1):
    filename = img.get("filename", f"image_{i}.png")
    prompt = img.get("prompt", "")
    output = os.path.join("$OUTPUT_DIR", filename)

    print(f"[{i}/{total}] Generating: {filename}")

    try:
        result = subprocess.run(
            ["$SCRIPT_DIR/gemini-image-gen.sh", prompt, output],
            capture_output=True,
            text=True,
            env={**os.environ}
        )
        if result.returncode == 0:
            success += 1
        else:
            failed += 1
            print(f"  ❌ Failed: {result.stderr}")
    except Exception as e:
        failed += 1
        print(f"  ❌ Error: {e}")

    # 避免 rate limit
    if i < total:
        time.sleep(2)

print(f"\n✅ Done! Success: {success}, Failed: {failed}")
EOF
