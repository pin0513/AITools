#!/bin/bash
#
# Gemini Image Generation Script
# 使用 Gemini API 生成圖片
#
# 使用方式:
#   ./gemini-image-gen.sh "prompt" output.png
#   GEMINI_API_KEY=xxx ./gemini-image-gen.sh "prompt" output.png
#
# 環境變數:
#   GEMINI_API_KEY - Gemini API 金鑰 (必須)
#   GEMINI_MODEL   - 模型名稱 (預設: gemini-2.0-flash-exp-image-generation)
#

set -e

# 檢查參數
if [ $# -lt 2 ]; then
    echo "Usage: $0 \"prompt\" output.png"
    echo ""
    echo "Environment variables:"
    echo "  GEMINI_API_KEY  - Required. Your Gemini API key"
    echo "  GEMINI_MODEL    - Optional. Model name (default: gemini-2.0-flash-exp-image-generation)"
    echo ""
    echo "Example:"
    echo "  GEMINI_API_KEY=your_key ./gemini-image-gen.sh \"A tech background\" hero.png"
    exit 1
fi

PROMPT="$1"
OUTPUT="$2"

# 檢查 API Key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set"
    exit 1
fi

# 設定模型 (可透過環境變數覆蓋)
MODEL="${GEMINI_MODEL:-gemini-2.0-flash-exp-image-generation}"

echo "Generating image with Gemini..."
echo "Model: $MODEL"
echo "Output: $OUTPUT"

# 呼叫 Gemini API
response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GEMINI_API_KEY}" \
    -H 'Content-Type: application/json' \
    -d "{
        \"contents\": [{
            \"parts\": [{\"text\": \"$PROMPT\"}]
        }],
        \"generationConfig\": {
            \"responseModalities\": [\"TEXT\", \"IMAGE\"]
        }
    }")

# 檢查錯誤
if echo "$response" | grep -q '"error"'; then
    echo "Error from API:"
    echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('error',d), indent=2))"
    exit 1
fi

# 提取 base64 圖片資料
image_data=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
        if 'inlineData' in part:
            print(part['inlineData']['data'])
            break
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
")

if [ -z "$image_data" ]; then
    echo "Error: No image data in response"
    echo "Response preview:"
    echo "$response" | head -500
    exit 1
fi

# 儲存圖片
echo "$image_data" | base64 -d > "$OUTPUT"
echo "✅ Saved: $OUTPUT"

# 顯示圖片資訊
if command -v file &> /dev/null; then
    file "$OUTPUT"
fi
