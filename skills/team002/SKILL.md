---
name: team002
description: |
  文章/文案撰寫團隊。包含企劃、研究、主筆、文案師、審稿主編、品質分析師，搭載七大寫作風格系統與去 AI 味機制。
  支援長文章、行銷文案、社群短文、EDM 等多種內容類型的完整製作流程。
  使用時機：(1) 撰寫文章 (2) 行銷文案 (3) 社群短文 (4) 內容企劃 (5) 主題研究 (6) 審稿潤稿
  觸發短語："team002", "寫文章", "寫文案", "內容企劃", "寫作團隊"
---

# Team002 - 文章/文案撰寫團隊

## 載入指示

請讀取完整團隊定義並依照指示執行：

**團隊主檔案**：讀取 `/Users/paul_huang/.claude/skills/teams/team002/SKILL.md`

依照該檔案中的「Article Consult（總編輯）」角色，接收用戶需求並調度團隊。

## Agent 檔案位置

需要切換角色時，讀取對應的 agent 檔案：

| 角色 | 檔案路徑 |
|------|---------|
| Article Planner (內容企劃) | `/Users/paul_huang/.claude/skills/teams/team002/agents/planning/article-planner.md` |
| Article Researcher (主題研究員) | `/Users/paul_huang/.claude/skills/teams/team002/agents/planning/article-researcher.md` |
| Article Writer (主筆) | `/Users/paul_huang/.claude/skills/teams/team002/agents/writing/article-writer.md` |
| Copywriter (文案師) | `/Users/paul_huang/.claude/skills/teams/team002/agents/writing/copywriter.md` |
| Article Editor (審稿主編) | `/Users/paul_huang/.claude/skills/teams/team002/agents/quality/article-editor.md` |
| Article Analytics (品質分析師) | `/Users/paul_huang/.claude/skills/teams/team002/agents/quality/article-analytics.md` |

## 共用技能檔案

| 技能 | 檔案路徑 |
|------|---------|
| 七大寫作風格系統 | `/Users/paul_huang/.claude/skills/teams/team002/skills/shared/writing-style-system.md` |
| 受眾適配 | `/Users/paul_huang/.claude/skills/teams/team002/skills/shared/audience-adaptation.md` |
| 敘事技巧 | `/Users/paul_huang/.claude/skills/teams/team002/skills/specialized/storytelling-craft.md` |
| 文案公式 | `/Users/paul_huang/.claude/skills/teams/team002/skills/specialized/copy-formulas.md` |
| 研究方法論 | `/Users/paul_huang/.claude/skills/teams/team002/skills/specialized/research-methodology.md` |
| 風格大師參考 | `/Users/paul_huang/Projects/writing-style.md` |

## 規則檔案（自動套用）

| 規則 | 檔案路徑 |
|------|---------|
| 去 AI 味 | `/Users/paul_huang/.claude/skills/teams/team002/rules/anti-ai-writing.md` |
| 品質門檻 | `/Users/paul_huang/.claude/skills/teams/team002/rules/quality-gate.md` |
| 內容誠信 | `/Users/paul_huang/.claude/skills/teams/team002/rules/content-integrity.md` |
