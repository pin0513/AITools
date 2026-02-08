# Continuous Learning v2

Instinct-based 持續學習系統。以背景任務方式運作，自動從使用模式中萃取可重用的知識。

## 概述

此系統透過觀察工具使用模式，自動學習並萃取出可重複利用的「本能」(Instincts)，進而演化為 skills、commands 或 agents。

## 架構

```
~/.claude/homunculus/
├── observations.jsonl      # 工具使用觀察記錄
├── instincts/
│   ├── personal/          # 個人學習到的 instincts
│   └── inherited/         # 匯入的 instincts
├── evolved/               # 演化出的 skills/commands/agents
│   ├── skills/
│   ├── commands/
│   └── agents/
└── config.json            # 系統配置
```

## 使用方式

### 檢視 Instinct 狀態

```bash
python3 ~/.claude/scripts/instinct-cli.py status
```

顯示所有已學習的 instincts 及其信心分數。

### 匯入 Instincts

```bash
python3 ~/.claude/scripts/instinct-cli.py import ~/shared-instincts
```

從其他來源匯入 instincts。

### 匯出 Instincts

```bash
python3 ~/.claude/scripts/instinct-cli.py export ~/my-instincts
python3 ~/.claude/scripts/instinct-cli.py export ~/my-instincts --min-confidence 0.7
```

匯出 instincts 供分享。

### 分析演化機會

```bash
python3 ~/.claude/scripts/instinct-cli.py evolve
python3 ~/.claude/scripts/instinct-cli.py evolve --auto
```

分析現有 instincts，建議可演化為 skill 的模式。

### 核准/拒絕 Instinct

```bash
python3 ~/.claude/scripts/instinct-cli.py approve <instinct-id>
python3 ~/.claude/scripts/instinct-cli.py reject <instinct-id>
python3 ~/.claude/scripts/instinct-cli.py reject <instinct-id> --delete
```

## 運作原理

### 1. 觀察階段 (Observation)

透過 PostToolUse hook，系統記錄以下工具的使用情況：
- Edit, Write, Bash, Read, Grep, Glob

每次工具使用都會記錄：
- 時間戳記
- Session ID
- 工具名稱
- 輸入參數
- 輸出結果
- 成功/失敗狀態

### 2. 分析階段 (Analysis)

Session 結束時，背景腳本會分析觀察記錄，偵測：

**重複工作流程 (Repeated Workflows)**
- 偵測經常出現的工具使用序列
- 例如：`Read -> Grep -> Edit` 重複出現 5 次以上

**使用者修正 (User Corrections)**
- 偵測同一檔案多次編輯失敗的情況
- 可能代表需要額外的驗證步驟

### 3. Instinct 產生

當偵測到模式時，系統會產生 Instinct 建議：

- **信心分數 < 0.3**: 忽略
- **信心分數 0.3-0.7**: 標記為 `pending`，等待使用者核准
- **信心分數 >= 0.7**: 自動核准 (`auto_approved`)

### 4. 演化階段 (Evolution)

高信心度的 Instincts 可以演化為：
- **Skill**: 可重複呼叫的技能
- **Command**: CLI 指令
- **Agent**: 自動化代理

## 配置

編輯 `~/.claude/homunculus/config.json`:

```json
{
  "observation": {
    "enabled": true,
    "rotation": {
      "maxSizeMB": 10,
      "maxAgeDays": 7
    }
  },
  "instinct": {
    "confidenceThreshold": {
      "minimum": 0.3,
      "autoApprove": 0.7
    }
  },
  "analyzer": {
    "triggers": {
      "minObservations": 10,
      "patternThreshold": 3
    }
  },
  "evolution": {
    "clusteringThreshold": 3,
    "autoEvolveConfidence": 0.8
  }
}
```

## 驗證

### 檢查觀察記錄

```bash
tail -f ~/.claude/homunculus/observations.jsonl
```

### 檢查背景分析器

```bash
ps aux | grep analyze-session
```

### 檢查分析日誌

```bash
tail -f ~/.claude/homunculus/analyzer.log
```

## 故障排除

### 觀察記錄未產生

1. 確認 hook 已配置在 `~/.claude/settings.json`
2. 確認 `observe-tool.sh` 有執行權限
3. 檢查 homunculus 目錄是否存在

### 背景分析器未執行

1. 確認 `analyze-session.sh` 有執行權限
2. 檢查 `analyzer.log` 是否有錯誤訊息
3. 手動執行腳本測試

## 相關檔案

| 檔案 | 用途 |
|------|------|
| `~/.claude/homunculus/config.json` | 系統配置 |
| `~/.claude/homunculus/observations.jsonl` | 觀察記錄 |
| `~/.claude/scripts/observe-tool.sh` | 記錄工具使用 |
| `~/.claude/scripts/analyze-session.sh` | 背景分析腳本 |
| `~/.claude/scripts/instinct-cli.py` | CLI 管理工具 |
| `~/.claude/settings.json` | Hooks 配置 |
