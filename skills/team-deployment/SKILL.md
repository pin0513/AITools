---
name: Team Deployment
description: Manage and deploy Claude Code team structures across projects
---

# Team Deployment

## 描述

管理和部署 Claude Code 團隊結構的工具技能。提供團隊庫管理、部署、更新等功能。

## 使用時機

1. 需要將團隊部署到新專案
2. 查看可用的團隊列表
3. 更新現有專案的團隊定義
4. 管理全域團隊庫

## 核心功能

### 1. 列出可用團隊

列出 `~/DEV/claude-teams/` 中所有可用的團隊及其說明。

### 2. 部署團隊

將指定團隊部署到目標專案目錄，包含：
- 複製 `.claude/` 目錄（agents、skills、rules）
- 複製 `CLAUDE.md` 說明文件
- 覆蓋前的安全確認

### 3. 更新團隊

更新現有專案中的團隊定義，保持與團隊庫同步。

### 4. 驗證團隊結構

檢查團隊定義的完整性：
- 所有 agents 有 YAML frontmatter
- Skills 引用路徑正確
- Rules 檔案存在

## 團隊庫位置

**預設路徑**：`~/DEV/claude-teams/`

團隊庫結構：
```
~/DEV/claude-teams/
├── README.md
├── team-name-1/
│   ├── CLAUDE.md
│   └── .claude/
│       ├── agents/
│       ├── skills/
│       └── rules/
└── team-name-2/
    └── ...
```

## 使用指南

### 場景 1：查看可用團隊

**使用者說**：「列出可用的團隊」或「有哪些團隊可以用」

**執行步驟**：
1. 讀取 `~/DEV/claude-teams/` 目錄
2. 遍歷每個子目錄
3. 讀取 `CLAUDE.md` 第一行作為團隊描述
4. 統計 agents、skills、rules 數量
5. 以表格形式展示

**輸出範例**：
```markdown
## 可用團隊

| 團隊名稱 | 描述 | Agents | Skills | Rules |
|---------|------|--------|--------|-------|
| cross-platform-app-dev | Electron 應用開發團隊 | 9 | 15 | 6 |
| web-content-production | 網站內容製作團隊 | 7 | 12 | 5 |
```

---

### 場景 2：部署團隊到新專案

**使用者說**：「部署 cross-platform-app-dev 到 ~/DEV/my-project」

**執行步驟**：
1. 驗證團隊存在於 `~/DEV/claude-teams/{team-name}/`
2. 驗證目標專案目錄存在
3. 檢查目標目錄是否已有 `.claude/`
   - 如有，詢問是否覆蓋
   - 如無，直接部署
4. 複製 `.claude/` 目錄
5. 複製 `CLAUDE.md` 檔案
6. 確認部署成功

**安全檢查**：
```bash
# 檢查是否會覆蓋現有團隊
if [ -d "$TARGET/.claude" ]; then
  # 顯示現有團隊資訊
  # 詢問使用者確認
fi
```

**輸出範例**：
```markdown
✅ 團隊部署成功

**團隊**：cross-platform-app-dev
**位置**：~/DEV/my-project

**部署內容**：
- 9 個 Agents
- 15 個 Skills
- 6 個 Rules

**下一步**：
cd ~/DEV/my-project
claude

然後說：「請使用這個團隊開發 [你的需求]」
```

---

### 場景 3：部署到當前目錄

**使用者說**：「部署 cross-platform-app-dev 到當前目錄」

**執行步驟**：
1. 使用 `pwd` 取得當前目錄
2. 執行場景 2 的部署流程

---

### 場景 4：更新現有專案的團隊

**使用者說**：「更新當前專案的團隊」或「同步團隊定義」

**執行步驟**：
1. 檢查當前目錄的 `CLAUDE.md`
2. 從 `CLAUDE.md` 識別團隊名稱
3. 從團隊庫複製最新定義
4. 顯示更新的檔案清單

**輸出範例**：
```markdown
✅ 團隊已更新

**團隊**：cross-platform-app-dev
**更新檔案**：
- .claude/agents/engineering/electron-developer.md
- .claude/skills/electron-development-fundamentals/SKILL.md
- .claude/rules/code-quality-standards.md

**變更摘要**：
- 新增：CLI development best practices
- 更新：Security guidelines
```

---

### 場景 5：驗證團隊結構

**使用者說**：「驗證團隊結構」或「檢查團隊定義」

**執行步驟**：
1. 檢查所有 agents 的 YAML frontmatter
2. 檢查 skills 引用路徑
3. 檢查 rules 檔案存在性
4. 驗證目錄結構符合規範
5. 報告問題和建議

**輸出範例**：
```markdown
## 團隊結構驗證

✅ **通過**：所有 Agents 有正確的 YAML frontmatter
✅ **通過**：Skills 引用路徑正確
⚠️  **警告**：發現 2 個未使用的 skills
❌ **錯誤**：rule-1.md 被引用但檔案不存在

**建議**：
1. 刪除未使用的 skills：unused-skill-1, unused-skill-2
2. 建立缺失的 rule：rule-1.md
```

---

### 場景 6：建立新團隊（整合 team-maker）

**使用者說**：「建立新團隊」

**執行步驟**：
1. 呼叫 `team-maker` skill
2. team-maker 完成後，詢問是否加入團隊庫
3. 如果是，移動到 `~/DEV/claude-teams/`
4. 提示部署方式

**輸出範例**：
```markdown
✅ 新團隊已建立並加入團隊庫

**團隊名稱**：mobile-app-ios
**位置**：~/DEV/claude-teams/mobile-app-ios

**如何使用**：
部署到專案：「部署 mobile-app-ios 到 ~/DEV/my-ios-app」
```

---

## 命令對照表

| 使用者說法 | 執行功能 |
|-----------|---------|
| 「列出可用團隊」「有哪些團隊」 | 列出團隊庫中的所有團隊 |
| 「部署 {team} 到 {path}」 | 部署指定團隊到目標路徑 |
| 「部署 {team} 到當前目錄」 | 部署到當前工作目錄 |
| 「更新團隊」「同步團隊」 | 更新當前專案的團隊定義 |
| 「驗證團隊」「檢查團隊結構」 | 驗證團隊定義完整性 |
| 「建立新團隊」 | 呼叫 team-maker 並加入團隊庫 |

---

## 實作細節

### Bash 命令範例

**列出團隊**：
```bash
for team in ~/DEV/claude-teams/*; do
  if [ -d "$team/.claude" ]; then
    team_name=$(basename "$team")
    description=$(head -1 "$team/CLAUDE.md" 2>/dev/null | sed 's/^# //')
    agent_count=$(find "$team/.claude/agents" -name "*.md" | wc -l)
    skill_count=$(find "$team/.claude/skills" -name "SKILL.md" | wc -l)
    rule_count=$(find "$team/.claude/rules" -name "*.md" | wc -l)
    
    echo "$team_name | $description | $agent_count | $skill_count | $rule_count"
  fi
done
```

**部署團隊**：
```bash
TEAM_NAME="cross-platform-app-dev"
TARGET_DIR="~/DEV/my-project"
TEAMS_DIR="~/DEV/claude-teams"

# 檢查團隊存在
if [ ! -d "$TEAMS_DIR/$TEAM_NAME" ]; then
  echo "錯誤：團隊不存在"
  exit 1
fi

# 檢查目標目錄
if [ -d "$TARGET_DIR/.claude" ]; then
  # 詢問是否覆蓋
  # ...
fi

# 執行複製
cp -r "$TEAMS_DIR/$TEAM_NAME/.claude" "$TARGET_DIR/"
cp "$TEAMS_DIR/$TEAM_NAME/CLAUDE.md" "$TARGET_DIR/"
```

---

## 錯誤處理

### 錯誤 1：團隊不存在

```
❌ 錯誤：團隊 'unknown-team' 不存在

可用團隊：
• cross-platform-app-dev
• web-content-production
```

### 錯誤 2：目標目錄不存在

```
❌ 錯誤：目標目錄 '~/DEV/nonexistent' 不存在

建議：
mkdir ~/DEV/nonexistent
```

### 錯誤 3：團隊庫未初始化

```
❌ 錯誤：團隊庫 '~/DEV/claude-teams' 不存在

是否初始化團隊庫？(y/N)
```

---

## 最佳實踐

1. **部署前確認**：總是顯示將要覆蓋的內容
2. **清楚的輸出**：使用表格和符號（✅ ❌ ⚠️）提升可讀性
3. **安全操作**：覆蓋前備份現有 `.claude/`
4. **版本追蹤**：記錄部署的團隊版本和時間
5. **驗證完整性**：部署後自動驗證團隊結構

---

## 擴展功能（未來）

- [ ] 團隊版本管理（git integration）
- [ ] 團隊差異比較
- [ ] 從遠端倉庫安裝團隊
- [ ] 團隊使用統計
- [ ] 自動更新檢查

---

## 範例對話

**使用者**：「列出可用的團隊」

**Claude**：
```markdown
## 可用團隊

| 團隊名稱 | 描述 | Agents | Skills | Rules |
|---------|------|--------|--------|-------|
| cross-platform-app-dev | Electron 應用開發團隊 | 9 | 15 | 6 |

詳細資訊：
• **cross-platform-app-dev**
  - 技術棧：Electron, React Native
  - 適用：跨平台桌面/移動應用開發
  - 位置：~/DEV/claude-teams/cross-platform-app-dev
```

---

**使用者**：「部署 cross-platform-app-dev 到 ~/DEV/my-app」

**Claude**：
```markdown
⚠️ 目標目錄已存在 .claude/ 目錄

**現有團隊**：
- Agents: 5 個
- Skills: 8 個  
- Rules: 3 個

是否覆蓋？覆蓋前會備份到 .claude.backup/

回覆「是」以繼續，或「否」取消部署。
```

**使用者**：「是」

**Claude**：
```markdown
✅ 團隊部署成功

**備份位置**：~/DEV/my-app/.claude.backup/
**團隊**：cross-platform-app-dev
**部署內容**：
- 9 個 Agents
- 15 個 Skills
- 6 個 Rules

**下一步**：
cd ~/DEV/my-app
claude

然後說：「請使用這個團隊開發檔案管理工具」
```
