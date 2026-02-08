# Jira REST API Skill

直接透過 REST API 操作 Jira，不依賴 MCP，避免 session 斷線問題。

## 使用方式

```
/use-jira-rest-api <action> <參數>
```

## 支援的 Actions

| Action | 說明 | 範例 |
|--------|------|------|
| `get <issueKey>` | 取得 issue 詳情 | `/use-jira-rest-api get PROJ-1234` |
| `comment <issueKey> <text>` | 新增留言 | `/use-jira-rest-api comment PROJ-1234 "分析完成"` |
| `search <jql>` | JQL 搜尋 | `/use-jira-rest-api search "project=MYPROJECT"` |
| `transitions <issueKey>` | 查看可用狀態 | `/use-jira-rest-api transitions PROJ-1234` |
| `move <issueKey> <status>` | 變更狀態 | `/use-jira-rest-api move PROJ-1234 "In Progress"` |

---

## 設定檔

設定檔位置：`~/.claude/skills/use-jira-rest-api/`

- `config.json` - site 和 email
- `credentials.json` - API token（請勿提交到版控）

---

## 執行方式

當收到此 skill 的呼叫時，依照以下步驟執行：

### 1. 讀取設定

```bash
SKILL_DIR="$HOME/.claude/skills/use-jira-rest-api"
SITE=$(jq -r '.site' "$SKILL_DIR/config.json")
EMAIL=$(jq -r '.email' "$SKILL_DIR/config.json")
TOKEN=$(jq -r '.token' "$SKILL_DIR/credentials.json")
AUTH=$(echo -n "$EMAIL:$TOKEN" | base64)
BASE_URL="https://${SITE}.atlassian.net"
```

### 2. 執行對應 Action

#### Action: get

```bash
curl -s -H "Authorization: Basic $AUTH" \
  "$BASE_URL/rest/api/3/issue/{issueKey}?fields=summary,description,status,assignee,priority,issuetype" \
  | jq '{key: .key, summary: .fields.summary, status: .fields.status.name, type: .fields.issuetype.name, priority: .fields.priority.name, assignee: .fields.assignee.displayName}'
```

#### Action: comment

建立 ADF 格式 JSON 後發送：

```bash
# 建立 comment body
cat << 'EOF' > /tmp/jira_comment.json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [{"type": "text", "text": "{COMMENT_TEXT}"}]
      }
    ]
  }
}
EOF

# 替換文字並發送
sed -i '' "s/{COMMENT_TEXT}/實際留言內容/" /tmp/jira_comment.json

curl -s -X POST \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d @/tmp/jira_comment.json \
  "$BASE_URL/rest/api/3/issue/{issueKey}/comment"
```

#### Action: search

```bash
curl -s -H "Authorization: Basic $AUTH" \
  -G --data-urlencode "jql={JQL_QUERY}" \
  --data-urlencode "fields=summary,status,assignee,priority" \
  --data-urlencode "maxResults=20" \
  "$BASE_URL/rest/api/3/search" \
  | jq '.issues[] | {key, summary: .fields.summary, status: .fields.status.name}'
```

#### Action: transitions

```bash
curl -s -H "Authorization: Basic $AUTH" \
  "$BASE_URL/rest/api/3/issue/{issueKey}/transitions" \
  | jq '.transitions[] | {id, name}'
```

#### Action: move

```bash
# 1. 先取得 transition id
TRANSITION_ID=$(curl -s -H "Authorization: Basic $AUTH" \
  "$BASE_URL/rest/api/3/issue/{issueKey}/transitions" \
  | jq -r '.transitions[] | select(.name == "{STATUS_NAME}") | .id')

# 2. 執行 transition
curl -s -X POST \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"transition\": {\"id\": \"$TRANSITION_ID\"}}" \
  "$BASE_URL/rest/api/3/issue/{issueKey}/transitions"
```

---

## ADF 格式快速參考

### 帶格式的留言

```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "heading",
        "attrs": {"level": 2},
        "content": [{"type": "text", "text": "標題"}]
      },
      {
        "type": "paragraph",
        "content": [
          {"type": "text", "text": "普通 "},
          {"type": "text", "text": "粗體", "marks": [{"type": "strong"}]},
          {"type": "text", "text": " 文字"}
        ]
      },
      {
        "type": "bulletList",
        "content": [
          {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "項目1"}]}]},
          {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "項目2"}]}]}
        ]
      }
    ]
  }
}
```

---

## 常見 JQL 查詢

| 用途 | JQL |
|------|-----|
| 我的待辦 | `assignee = currentUser() AND status != Done` |
| 專案 Backlog | `project = MYPROJECT AND status = Backlog` |
| 近期更新 | `project = MYPROJECT AND updated >= -7d` |
| 高優先級 | `project = MYPROJECT AND priority in (P1, P2)` |

---

## 注意事項

1. **credentials.json 保密** - 已加入 .gitignore，請勿提交
2. **Rate Limit** - Jira Cloud API 限流，避免短時間大量請求
3. **ADF 格式** - Jira API v3 必須使用 ADF，不支援純 Markdown

---

*版本：v1.0 | 更新日期：2026-01-28*
