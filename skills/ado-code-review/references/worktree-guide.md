# Worktree Diff 使用指南

使用 Git Worktree 技術進行精確的 PR diff 比較，避免 merge 干擾。

---

## 為什麼需要 Worktree Diff?

### 傳統 Diff 的問題

```bash
# 問題：直接比較可能包含 merge commit 的變更
git diff main..feature/xxx

# 這會包含：
# 1. feature 分支的變更 (我們要的)
# 2. main 分支合併進來的變更 (不要的)
# 3. 解決 merge conflict 的變更 (可能混淆)
```

### Worktree Diff 的優勢

```bash
# 找到共同祖先
MERGE_BASE=$(git merge-base main feature/xxx)

# 從共同祖先比較
git diff $MERGE_BASE..feature/xxx

# 這只會包含 feature 分支真正的變更
```

---

## 標準流程

### Step 1: Fetch 最新遠端

```bash
git fetch origin
```

### Step 2: 計算 Merge Base

```bash
# 找到 source 和 target 的共同祖先
MERGE_BASE=$(git merge-base origin/main origin/feature/user-auth)
echo "Merge Base: $MERGE_BASE"
```

### Step 3: 取得 Diff 統計

```bash
git diff $MERGE_BASE..origin/feature/user-auth --stat
```

輸出範例：
```
 src/Services/UserService.cs | 45 +++++++++++++++++++++++
 src/Controllers/UserController.cs | 12 ++++---
 2 files changed, 52 insertions(+), 5 deletions(-)
```

### Step 4: 取得完整 Diff

```bash
git diff $MERGE_BASE..origin/feature/user-auth --no-color
```

### Step 5: 取得變更的檔案列表

```bash
git diff $MERGE_BASE..origin/feature/user-auth --name-only
```

### Step 6: 取得 Commit 歷史

```bash
git log $MERGE_BASE..origin/feature/user-auth --oneline
```

---

## Azure DevOps PR 審查流程

### 1. 從 PR 取得分支資訊

```bash
# PR 83397 的資訊
SOURCE_BRANCH="feature/user-auth"
TARGET_BRANCH="main"
```

### 2. Fetch 並比較

```bash
# Fetch 遠端
git fetch origin

# 計算 merge base
MERGE_BASE=$(git merge-base origin/$TARGET_BRANCH origin/$SOURCE_BRANCH)

# 取得精確 diff
git diff $MERGE_BASE..origin/$SOURCE_BRANCH
```

### 3. 完整腳本

```bash
#!/bin/bash
# worktree-diff.sh

REPO_PATH="$1"
SOURCE_BRANCH="$2"
TARGET_BRANCH="${3:-main}"

cd "$REPO_PATH" || exit 1

# Fetch latest
git fetch origin

# Calculate merge base
MERGE_BASE=$(git merge-base "origin/$TARGET_BRANCH" "origin/$SOURCE_BRANCH")

echo "=== Worktree Diff Report ==="
echo "Source: $SOURCE_BRANCH"
echo "Target: $TARGET_BRANCH"
echo "Merge Base: $MERGE_BASE"
echo ""

echo "=== Diff Stats ==="
git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --stat

echo ""
echo "=== Changed Files ==="
git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --name-only

echo ""
echo "=== Commits ==="
git log "$MERGE_BASE".."origin/$SOURCE_BRANCH" --oneline
```

---

## 本地分支審查

### 比較未提交變更

```bash
# 比較工作區與 HEAD
git diff HEAD

# 比較暫存區與 HEAD
git diff --cached
```

### 比較本地分支

```bash
# 本地分支 vs main
MERGE_BASE=$(git merge-base main feature/xxx)
git diff $MERGE_BASE..feature/xxx
```

---

## 處理特殊情況

### 分支已被刪除

```bash
# 使用 commit SHA 代替分支名
git diff abc123..def456
```

### 跨 Repository 比較

```bash
# 添加另一個遠端
git remote add other https://...
git fetch other

# 比較
git diff origin/main..other/feature
```

### 大型 Diff 處理

```bash
# 只看特定檔案類型
git diff $MERGE_BASE..HEAD -- "*.cs"

# 忽略空白變更
git diff $MERGE_BASE..HEAD -w

# 只看統計
git diff $MERGE_BASE..HEAD --stat
```

---

## 與 ADO MCP 整合

### 取得 PR 資訊

```
使用 mcp__azure-devops__repo_get_pull_request_by_id:
- repositoryId: "MyProject-Api"
- pullRequestId: 83397
- project: "MyProject"

回傳：
- sourceRefName: "refs/heads/feature/user-auth"
- targetRefName: "refs/heads/main"
```

### 轉換分支名稱

```bash
# 從 refs/heads/feature/user-auth 取得 feature/user-auth
SOURCE_BRANCH=$(echo "refs/heads/feature/user-auth" | sed 's|refs/heads/||')
```

---

## 常見問題

### Q: Merge base 為空?

```bash
# 確認分支存在
git branch -a | grep feature

# 嘗試 fetch
git fetch origin feature/xxx:feature/xxx
```

### Q: Diff 內容太大?

```bash
# 分批處理
git diff $MERGE_BASE..HEAD --name-only | head -20

# 只看特定目錄
git diff $MERGE_BASE..HEAD -- src/Services/
```

### Q: 如何排除特定檔案?

```bash
# 排除 .json 檔案
git diff $MERGE_BASE..HEAD -- . ':!*.json'

# 排除特定目錄
git diff $MERGE_BASE..HEAD -- . ':!tests/'
```

---

## 輸出格式

### 標準 Diff 格式

```diff
diff --git a/src/Services/UserService.cs b/src/Services/UserService.cs
index abc123..def456 100644
--- a/src/Services/UserService.cs
+++ b/src/Services/UserService.cs
@@ -10,6 +10,10 @@ public class UserService
     {
         private readonly ILogger _logger;
+
+        public async Task<User> GetUserAsync(int id)
+        {
+            return await _repository.GetByIdAsync(id);
+        }
     }
```

### 解讀 Diff

| 符號 | 意義 |
|-----|------|
| `---` | 原始檔案 |
| `+++` | 修改後檔案 |
| `@@` | 變更位置 (行號) |
| `-` | 刪除的行 |
| `+` | 新增的行 |
| ` ` (空格) | 未變更的行 (上下文) |

---

*版本：v1.0 | 更新日期：2026-01-29*
