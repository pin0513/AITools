---
name: teams-notify
description: |
  發送 Microsoft Teams 訊息通知技能。透過 Incoming Webhook 發送訊息到指定的 Teams channel。
  使用時機：(1) PR 建立後通知團隊 (2) 部署完成通知 (3) 重要事件通知
---

# Teams Notify Skill

透過 Microsoft Teams Incoming Webhook 發送訊息通知。

## 使用方式

```
/teams-notify <訊息類型> [參數] [--to 群組ID]
```

### 支援的訊息類型

| 類型 | 說明 | 範例 |
|------|------|------|
| `pr` | PR 建立/更新通知 | `/teams-notify pr 83059` |
| `pr` | PR 通知到指定群組 | `/teams-notify pr 83059 --to qa` |
| `deploy` | 部署完成通知 | `/teams-notify deploy TST --to release` |
| `custom` | 自訂訊息 | `/teams-notify custom "訊息內容" --to dev` |

### 群組參數

- `--to <群組ID>`: 指定發送到哪個 Teams 群組
- 若未指定，使用 `webhooks.json` 中的 `default` 群組

---

## 前置設定

### 1. 取得 Teams Incoming Webhook URL

1. 進入 Teams Channel → 點擊 `...` → `Connectors`
2. 搜尋 `Incoming Webhook` → 點擊 `Configure`
3. 設定名稱（如 `Claude Code Bot`）→ 複製 Webhook URL

### 2. 設定 Webhook 配置檔

在 `~/.claude/skills/teams-notify/webhooks.json` 建立配置：

```json
{
  "webhooks": {
    "dev": {
      "name": "開發團隊",
      "url": "https://outlook.office.com/webhook/xxx-dev"
    },
    "qa": {
      "name": "QA 團隊",
      "url": "https://outlook.office.com/webhook/xxx-qa"
    },
    "release": {
      "name": "Release 通知",
      "url": "https://outlook.office.com/webhook/xxx-release"
    }
  },
  "default": "dev"
}
```

### Webhook 群組說明

| 群組 ID | 用途 | 通知類型 |
|--------|------|---------|
| `dev` | 開發團隊日常通知 | PR、Code Review |
| `qa` | QA 團隊通知 | 測試完成、Bug 修復 |
| `release` | 發布通知 | 部署、版本更新 |

---

## 工作流程

### PR 通知 (`/teams-notify pr <PR_ID>`)

1. **取得 PR 資訊**
   ```
   使用 mcp__azure-devops__repo_get_pull_request_by_id 取得 PR 詳情
   ```

   > ⚠️ **重要：PR URL 組裝規則**
   >
   > **永遠不要自己猜測或組裝 PR URL！** 必須從 API 回應中取得：
   >
   > ```
   > PR_URL = {repository.webUrl}/pullrequest/{pullRequestId}
   > ```
   >
   > 例如 API 回應：
   > ```json
   > {
   >   "pullRequestId": 83468,
   >   "repository": {
   >     "webUrl": "https://{org}.visualstudio.com/{project}/_git/{repo}"
   >   }
   > }
   > ```
   >
   > 正確 URL: `https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/83468`
   >
   > **常見錯誤（請勿使用）：**
   > - ❌ `dev.azure.com/ApolloHRP/...` (錯誤的組織)
   > - ❌ `dev.azure.com/{org}/{project}/_git/...` (自行猜測格式)
   > - ✅ 使用 `repository.webUrl` + `/pullrequest/{id}`

2. **組裝 Adaptive Card**
   ```json
   {
     "type": "message",
     "attachments": [
       {
         "contentType": "application/vnd.microsoft.card.adaptive",
         "content": {
           "type": "AdaptiveCard",
           "body": [...],
           "actions": [...]
         }
       }
     ]
   }
   ```

3. **發送到 Teams**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"type":"message","attachments":[...]}' \
     "$TEAMS_WEBHOOK_URL"
   ```

---

## Adaptive Card 模板 (Power Automate 格式)

> **重要**: Power Automate webhook 需要直接發送 Adaptive Card JSON，不需要外層的 `message` 和 `attachments` 包裝。

### PR 通知模板

```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "size": "Large",
      "weight": "Bolder",
      "text": "🔀 Pull Request #{PR_ID}"
    },
    {
      "type": "TextBlock",
      "text": "{PR_TITLE}",
      "weight": "Bolder",
      "wrap": true
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "建立者", "value": "{CREATED_BY}" },
        { "title": "分支", "value": "{SOURCE_BRANCH} → {TARGET_BRANCH}" },
        { "title": "Repo", "value": "{REPO_NAME}" }
      ]
    },
    {
      "type": "TextBlock",
      "text": "{SUMMARY}",
      "wrap": true,
      "isSubtle": true
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "查看 PR",
      "url": "{PR_URL}"
    },
    {
      "type": "Action.OpenUrl",
      "title": "查看 Jira",
      "url": "{JIRA_URL}"
    }
  ]
}
```

### 自訂訊息模板

```json
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
          {
            "type": "TextBlock",
            "text": "{MESSAGE}",
            "wrap": true
          }
        ]
      }
    }
  ]
}
```

---

## 完整範例

### 發送 PR 通知

```bash
# 1. 先使用 MCP 取得 PR 詳情
# mcp__azure-devops__repo_get_pull_request_by_id
# 回應會包含 repository.webUrl，用它來組裝 PR_URL

# 2. 從 API 回應取得 URL (重要！)
# PR_URL = ${repository.webUrl}/pullrequest/${pullRequestId}
# 例如: https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/{id}

# 3. 發送到 Teams (使用從 API 取得的 URL)
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.4",
    "body": [
      {"type": "TextBlock", "size": "Large", "weight": "Bolder", "text": "🔀 Pull Request #1234"},
      {"type": "TextBlock", "text": "feat: add user authentication feature", "weight": "Bolder", "wrap": true},
      {"type": "FactSet", "facts": [
        {"title": "建立者", "value": "Developer Name"},
        {"title": "分支", "value": "feature/user-auth → main"}
      ]}
    ],
    "actions": [
      {"type": "Action.OpenUrl", "title": "查看 PR", "url": "${PR_URL_FROM_API}"}
    ]
  }' \
  "$TEAMS_WEBHOOK_URL"
```

> ⚠️ **注意**: `PR_URL_FROM_API` 必須從 `mcp__azure-devops__repo_get_pull_request_by_id` 回應中的 `repository.webUrl` 組裝，**絕對不要自己猜測 URL 格式**！

---

## 錯誤處理

| 錯誤 | 原因 | 解決方式 |
|-----|------|---------|
| `TEAMS_WEBHOOK_URL not set` | 未設定環境變數 | 設定 Webhook URL |
| `400 Bad Request` | Payload 格式錯誤 | 檢查 JSON 格式 |
| `403 Forbidden` | Webhook 已失效 | 重新建立 Webhook |
| `404 Not Found` | URL 錯誤 | 確認 Webhook URL |

---

## 注意事項

1. **Webhook URL 保密** - 不要將 URL 提交到版控
2. **訊息長度限制** - Adaptive Card 有大小限制 (約 28KB)
3. **頻率限制** - 避免短時間內發送過多訊息

---

*版本：v1.0 | 更新日期：2026-01-16*
