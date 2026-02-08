---
name: Gemini-GenImage
description: |
  使用 Google Gemini API 生成 AI 圖片的獨立技能。
  提供單張生成、批次生成兩種模式，支援環境變數或直接傳入 API Key。
  適用於：投影片配圖、UI 設計素材、網站視覺、概念示意圖等場景。
license: MIT
metadata:
  last_verified: "2026-01-30"
  version: "1.0.0"
---

# Gemini-GenImage Skill

使用 Google Gemini API 生成 AI 圖片的獨立技能。

## 🚀 快速開始

### 環境設定

```bash
# 設定 API Key (二擇一)
export GEMINI_API_KEY="your-api-key-here"
# 或在執行時直接傳入
```

### 單張生成

```bash
# 基本用法
~/.claude/skills/Gemini-GenImage/scripts/gemini-image-gen.sh "Your prompt here" output.png

# 指定 API Key
GEMINI_API_KEY=xxx ~/.claude/skills/Gemini-GenImage/scripts/gemini-image-gen.sh "prompt" output.png

# 使用不同模型
GEMINI_MODEL=gemini-2.5-flash-image ~/.claude/skills/Gemini-GenImage/scripts/gemini-image-gen.sh "prompt" output.png
```

### 批次生成

```bash
# 準備 config.json
cat > config.json << 'EOF'
{
  "images": [
    {"filename": "hero.png", "prompt": "Tech background with dark blue gradient"},
    {"filename": "icon.png", "prompt": "Minimalist app icon design"}
  ]
}
EOF

# 執行批次生成
~/.claude/skills/Gemini-GenImage/scripts/batch-generate.sh config.json output_dir/
```

---

## 腳本說明

### gemini-image-gen.sh

單張圖片生成腳本。

**參數：**
| 參數 | 說明 |
|------|------|
| `$1` | Prompt 描述 (必須) |
| `$2` | 輸出檔案路徑 (必須) |

**環境變數：**
| 變數 | 說明 | 預設值 |
|------|------|--------|
| `GEMINI_API_KEY` | Gemini API 金鑰 | (必須) |
| `GEMINI_MODEL` | 模型名稱 | `gemini-2.0-flash-exp-image-generation` |

**範例：**
```bash
# 生成科技背景圖
./gemini-image-gen.sh "Dark tech background with glowing nodes, deep blue (#1a237e) and red (#d32f2f) accents, modern minimal style, 16:9" hero-bg.png

# 生成架構圖
./gemini-image-gen.sh "Three-tier architecture diagram: Application -> Redis Cache -> Database, dark background, professional infographic style" architecture.png
```

### batch-generate.sh

批次生成多張圖片。

**參數：**
| 參數 | 說明 |
|------|------|
| `$1` | Config JSON 檔案路徑 (必須) |
| `$2` | 輸出目錄 (必須) |

**Config JSON 格式：**
```json
{
  "images": [
    {"filename": "output1.png", "prompt": "Prompt for image 1"},
    {"filename": "output2.png", "prompt": "Prompt for image 2"}
  ]
}
```

**特性：**
- 自動建立輸出目錄
- 每張圖片間隔 2 秒 (避免 rate limit)
- 顯示生成進度 `[1/5]`
- 統計成功/失敗數量

---

## 模型選擇

| 模型 ID | 狀態 | 適用場景 |
|---------|------|----------|
| `gemini-2.0-flash-exp-image-generation` | 穩定 | 快速生成、一般用途 |
| `gemini-2.5-flash-image` | GA | 更好品質、一般用途 |
| `gemini-3-pro-image-preview` | Preview | 4K、複雜 prompt、文字渲染 |

**建議：**
- 90% 場景使用預設模型即可
- 需要更高品質時切換 `gemini-2.5-flash-image`
- 需要 4K 或精準文字時使用 `gemini-3-pro-image-preview`

---

## Prompt 撰寫技巧

### 簡報背景圖

```
Dark tech background for presentation.
Gradient from #0d1117 to #1a237e.
Abstract data flow visualization with glowing nodes.
Subtle hexagonal grid pattern.
Modern, sleek, professional.
No text, no logos. Clean and minimal.
Suitable for overlaying white text.
16:9 aspect ratio.
```

### 架構圖

```
Three-tier cache architecture diagram.
Dark tech background.
Three glowing boxes: Application (blue) -> Redis Cache (red, center, larger) -> Database (blue).
Arrows showing data flow.
Modern minimalist tech style.
Colors: deep blue (#1a237e), Redis red (#d32f2f), white accents.
16:9 aspect ratio.
```

### 概念圖

```
Speed comparison visualization.
Split image: Left = snail (slow, 200ms), Right = rocket (fast, <1ms).
Dark background with red (#d32f2f) and blue (#1a237e) color scheme.
Modern flat design, clean vector-like aesthetic.
Subtle speed lines and motion effects.
No text labels. 16:9 aspect ratio.
```

### 流程圖

```
Distributed lock concept illustration.
Dark tech background.
Central glowing padlock in gold (#ffc107).
Multiple server nodes (3-4) arranged around it.
ONE server has solid connection (acquired), others faded/denied.
Modern minimalist tech style.
16:9 aspect ratio.
```

### 🎭 角色圖（分層素材用）

> **重點**：生成便於去背的角色圖，用於分層動畫

**角色生成 Prompt 模板：**
```
[角色描述], [動作/表情],
simple solid [顏色] background,
full body visible, clear edges, clean silhouette,
[風格] style, flat colors,
high quality illustration, centered composition
```

**範例 - 日系可愛風角色：**
```
Cute young boy with brown hair in medieval peasant clothes,
standing pose with curious expression,
simple solid pastel pink background,
full body visible, clear edges, clean silhouette,
kawaii anime style, soft pastel colors,
high quality illustration, centered composition
```

**範例 - 騎士角色：**
```
Big muscular knight in shiny silver armor,
confident standing pose with hands on hips,
simple solid light blue background,
full body visible, clear edges, clean silhouette,
anime style, vibrant colors,
high quality illustration, centered composition
```

**角色生成的關鍵要點：**

| 要點 | 正確做法 | 錯誤做法 |
|------|----------|----------|
| 背景 | `simple solid [color] background` | 複雜場景背景 |
| 邊緣 | `clear edges, clean silhouette` | 模糊邊緣、漸層融合 |
| 構圖 | `full body visible, centered` | 截斷、偏移 |
| 風格 | `flat colors` | 複雜光影 |

**角色去背流程（必要後處理）：**
```bash
# 1. 移除浮水印
~/ai-tools/GeminiWatermarkTool char_raw.png

# 2. 使用 rembg 去背
rembg i -m isnet-anime char_raw.png char_transparent.png

# 3. 檢查結果
identify -verbose char_transparent.png | grep -i "alpha"
```

**角色表情變體生成：**
```bash
# 生成同一角色的不同表情
GEMINI_API_KEY=xxx ./gemini-image-gen.sh \
  "Cute young boy... happy smiling expression, ..." \
  char_art_happy.png

GEMINI_API_KEY=xxx ./gemini-image-gen.sh \
  "Cute young boy... sad disappointed expression, ..." \
  char_art_sad.png
```

---

## 整合到其他 Skills

### 投影片相關

此 skill 可被以下投影片相關 skills 呼叫：

- **slide-consult** - 投影片製作顧問
- **slide-maker** - 投影片生成器
- **slide-image** - 投影片圖片處理
- **slide-theme** - 投影片主題樣式

### UI/設計相關

此 skill 可被以下設計相關 skills 呼叫：

- **web-produce-artist** - 網站素材繪圖師
- **web-produce-designer** - 網頁設計師
- **dev-team-ui** - UI/UX 設計總監
- **dev-team-ui-pro** - UI/UX 進階設計

### 整合範例

在其他 skill 中呼叫：

```bash
# 在簡報製作流程中生成圖片
GEMINI_API_KEY="$API_KEY" ~/.claude/skills/Gemini-GenImage/scripts/gemini-image-gen.sh "$PROMPT" "$OUTPUT_PATH"

# 批次生成簡報所需圖片
~/.claude/skills/Gemini-GenImage/scripts/batch-generate.sh images-config.json ./assets/images/
```

---

## 錯誤處理

| 錯誤訊息 | 原因 | 解決方式 |
|----------|------|----------|
| `GEMINI_API_KEY not set` | 未設定 API Key | 設定環境變數或直接傳入 |
| `Error from API` | API 回傳錯誤 | 檢查 API Key 是否有效、模型是否存在 |
| `No image data in response` | 回應中無圖片 | 檢查 prompt 是否觸發安全過濾 |

---

## API 定價參考

| 模型 | 每張圖片約 |
|------|-----------|
| gemini-2.0-flash-exp | ~$0.005 |
| gemini-2.5-flash-image | ~$0.008 |
| gemini-3-pro-image | ~$0.02 |

---

## 後處理：浮水印移除

生成的圖片可能包含 Gemini 浮水印，可使用以下工具移除：

```bash
# 單張處理
~/ai-tools/GeminiWatermarkTool image.png

# 批次處理
~/ai-tools/GeminiWatermarkTool -i ./generated/ -o ./cleaned/
```

**注意：** SynthID (不可見浮水印) 無法移除，這是設計如此。

---

**Last verified**: 2026-01-30 | **Skill version**: 1.0.0
