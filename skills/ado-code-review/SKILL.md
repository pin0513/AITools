---
name: ado-code-review
description: |
  Azure DevOps 專業程式碼審查技能。整合 Worktree-based diff、C# 專家審查、資安弱點掃描、ADO PR 評論發佈、Teams 通知。
  使用時機：(1) 審查 Azure DevOps PR (2) 本地分支 code review (3) 提交前程式碼審查 (4) 資安弱點掃描
  觸發短語："review PR", "code review", "審查 PR", "檢查程式碼", "資安審查"
---

# Azure DevOps Code Review Skill

專為 Azure DevOps 設計的企業級程式碼審查技能，整合多個審查維度與自動化通知。

## 核心功能

| 功能 | 說明 |
|------|------|
| **Worktree Diff** | 使用 Git Worktree 精確比較，避免 merge 干擾 |
| **C# 專家審查** | .NET/C# 最佳實踐、效能、架構審查 |
| **資安弱點掃描** | OWASP Top 10、硬編碼憑證、注入攻擊檢測 |
| **ADO PR 評論** | 自動發佈審查結果到 PR Thread |
| **Teams 通知** | 發送審查摘要到 Teams Channel |

---

## 使用方式

### 基本用法

```bash
# 審查 Azure DevOps PR
/ado-code-review 83397

# 審查多個 PR
/ado-code-review 83397 83449

# 審查本地分支
/ado-code-review main..feature/my-feature

# 審查未提交變更
/ado-code-review
```

### 參數選項

| 參數 | 說明 | 範例 |
|------|------|------|
| `<PR_ID>` | Azure DevOps PR 編號 | `83397` |
| `<branch_range>` | Git 分支範圍 | `main..feature/xxx` |
| `--no-comment` | 不發佈 PR 評論 | `--no-comment` |
| `--no-teams` | 不發送 Teams 通知 | `--no-teams` |
| `--security-only` | 僅執行資安審查 | `--security-only` |

---

## 審查流程

### 1. 取得變更內容

使用 Worktree-based diff 取得精確變更：

```bash
# 取得 merge-base
MERGE_BASE=$(git merge-base origin/main origin/$SOURCE_BRANCH)

# 精確 diff
git diff $MERGE_BASE..$SOURCE_BRANCH
```

### 2. 執行多維度審查

啟動 **5 個並行 Agent** 進行獨立審查：

| Agent | 審查焦點 | Model |
|-------|---------|-------|
| **C# 品質審查** | 程式碼品質、命名、架構 | Sonnet |
| **資安弱點掃描** | OWASP、憑證、注入 | Sonnet |
| **.NET 效能審查** | async/await、EF Core、記憶體 | Haiku |
| **測試覆蓋審查** | 測試案例、覆蓋率 | Haiku |
| **CLAUDE.md 合規** | 專案規範遵循 | Haiku |

### 3. 信心分數過濾

每個 issue 評分 0-100：

| 分數 | 等級 | 說明 |
|-----|------|------|
| 0-25 | 假陽性 | 不報告 |
| 26-50 | 小問題 | 不報告 |
| 51-75 | 中等問題 | 不報告 |
| **76-89** | **重要問題** | 報告為 HIGH |
| **90-100** | **嚴重問題** | 報告為 CRITICAL |

**只報告 ≥ 80 分的 issues**

### 4. 發佈結果

- **ADO PR**: 使用 `mcp__azure-devops__repo_create_pull_request_thread` 發佈
- **Teams**: 使用 Teams Webhook 發送 Adaptive Card

---

## 審查規則

### CRITICAL (必須修復)

參考 `references/security-checks.md` 完整清單：

- 硬編碼憑證 (API keys, passwords, connection strings)
- SQL 注入風險 (字串串接查詢)
- 缺少輸入驗證
- 不安全的反序列化
- 路徑遍歷風險
- 認證繞過

### HIGH (強烈建議修復)

參考 `references/dotnet-checks.md` 完整清單：

- 方法超過 50 行
- 檔案超過 800 行
- 巢狀深度 > 4 層
- 缺少錯誤處理
- Console.WriteLine 殘留
- 阻塞式 async 呼叫 (.Result, .Wait())
- 缺少 CancellationToken

### MEDIUM (建議修復)

- 可變性模式 (建議使用 immutable)
- Magic numbers
- 缺少測試
- 命名不一致

---

## 輸出格式

```markdown
## Code Review Report

### 審查資訊
- **PR:** #83397
- **標題:** feat: xxx
- **分支:** feature/xxx → main
- **模式:** Worktree-based Diff
- **Merge Base:** abc123

### 變更統計
- 檔案數：X 個
- 新增：+XXX 行
- 刪除：-XXX 行

### 問題清單

#### 🔴 CRITICAL (必須修復)
**[CRITICAL-1] 硬編碼 API Key**
- **File:** src/Services/PaymentService.cs:45
- **Issue:** 發現硬編碼的 API key
- **Fix:** 使用 Configuration 或 Key Vault

#### 🟠 HIGH (強烈建議修復)
...

### 審查決定
| 決定 | 條件 |
|-----|-----|
| ✅ APPROVE | 無 CRITICAL 或 HIGH |
| ⚠️ WARNING | 僅 MEDIUM issues |
| 🚫 BLOCK | 有 CRITICAL 或 HIGH |

**最終決定:** {APPROVE/WARNING/BLOCK}
```

---

## SubAgent 使用

此 skill 包含專用 SubAgent，可獨立執行完整審查流程：

```
使用 Task tool 呼叫 ado-code-reviewer agent
```

Agent 位置: `agents/ado-code-reviewer.md`

---

## 與其他工具整合

### Azure DevOps MCP

需要以下 MCP 工具：
- `mcp__azure-devops__repo_get_pull_request_by_id`
- `mcp__azure-devops__repo_create_pull_request_thread`
- `mcp__azure-devops__repo_list_pull_requests_by_repo_or_project`

### Teams Webhook

參考 `~/.claude/skills/teams-notify/SKILL.md` 設定 Webhook。

---

## 參考資源

### Reference Files

詳細審查規則請參考：
- **`references/dotnet-checks.md`** - .NET/C# 審查規則
- **`references/security-checks.md`** - 資安弱點審查規則
- **`references/worktree-guide.md`** - Worktree 使用指南
- **`~/.claude/rules/azure-devops.md`** - Azure DevOps 操作規則 (PR URL 組裝)

### Scripts

- **`scripts/worktree-diff.sh`** - Worktree diff 輔助腳本

---

## 錯誤處理

| 錯誤 | 原因 | 解決方式 |
|-----|------|---------|
| PR not found | PR ID 錯誤或無權限 | 確認 PR ID 和權限 |
| Branch not found | 分支不存在或未 fetch | 執行 `git fetch origin` |
| MCP error | Azure DevOps MCP 連線問題 | 確認 MCP 設定 |
| Teams webhook failed | Webhook URL 無效 | 更新 webhooks.json |

---

*版本：v1.0 | 更新日期：2026-01-29*
