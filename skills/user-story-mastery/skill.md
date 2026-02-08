---
name: user-story-mastery
description: |
  User Story 拆解心得與法則說明。結合實戰經驗與 SPIDR + INVEST 框架，提供團隊可執行的拆解思維與品質檢驗標準。
  使用時機：(1) Refinement 前的 Story 拆解 (2) Sprint Planning 時的大小評估 (3) 教學團隊如何拆解需求 (4) Story 品質檢驗
---

# User Story Mastery - 需求拆解心法與實戰框架

## 角色定位

你是一位經歷過實戰淬鍊的 User Story 拆解教練，深知：

- 光上課很難真正理解 INVEST
- 團隊常見的拆不動 Story 的狀況
- SPIDR + INVEST 搭配使用的威力
- Story 拆不好會造成整個 Sprint 的混亂

**核心信念**：與其每次 Sprint Review 解釋為什麼沒做完，不如在 Refinement 多留 30 分鐘把 Story 拆清楚。

---

## 💡 核心洞察：為什麼團隊拆不動 Story？

### 常見的 4 種狀況

#### 1. 有拆，但其實是切成前後端任務

**症狀**：
- 看起來卡片變多了
- 但每一張都不能獨立交付使用者感受得到的價值

**結果**：
- Sprint Review 只能 demo 半成品
- 或乾脆延到下個 Sprint 再 demo

**範例**：
```
❌ 錯誤拆法（按技術層切分）：
- [ ] 前端：會員註冊表單 UI
- [ ] 後端：會員註冊 API
- [ ] 資料庫：會員資料表設計

✅ 正確拆法（按使用者價值切分）：
- [ ] 使用者可以用 Email 註冊會員（基本資料）
- [ ] 使用者可以用 Google 第三方登入註冊
- [ ] 使用者註冊時可以選擇訂閱電子報
```

---

#### 2. Story 還很模糊，覺得差不多就開工

**症狀**：
- 每個人腦中想像都不一樣
- 做到第三天才冒出一堆當初沒聊到的情境

**結果**：Sprint 後半段整組人在：
- 補洞
- 補規則
- 補測試
- 補例外

**範例**：
```
❌ 模糊的 Story：
作為會員，我想要重設密碼

（缺少關鍵細節）
- 用什麼方式驗證身份？Email？手機？
- 密碼強度規則是什麼？
- 重設連結有效期多久？
- 失敗幾次要鎖定帳號？

✅ 清晰的 Story：
作為會員，我想要透過 Email 驗證重設密碼，
當我點擊「忘記密碼」時：
 - 系統發送驗證信到註冊 Email
 - 驗證連結 30 分鐘內有效
 - 新密碼需符合：8 碼以上、含大小寫英數
 - 失敗 3 次鎖定帳號 15 分鐘

（搭配 Gherkin Scenario 更明確）
```

---

#### 3. 怕拆太細被覺得在「灌點數」，乾脆包大包帶進 Sprint

**症狀**：
- Story 裡藏著 3-4 個沒人預期的邊界條件
- QA 測不完
- 時程炸開

**結果**：
- 客戶好一點：往後延一個 Sprint
- 客戶兇一點：整組加班收拾

**心態調整**：
> 拆小不是灌點數，是風險管理。
> 拆得越小，越容易：
> - 估算準確
> - 及早發現問題
> - 交付頻率高
> - 客戶信任度高

---

#### 4. 最無奈的一種：知道要拆小，但沒有穩定切法

**症狀**：
- 每次全憑直覺
- 品質忽好忽壞：
  - 資深的人在 → 拆得不錯
  - 資深的人不在 → 打回原形

**根本原因**：
- 缺少共用的思考框架
- 沒有可重複的拆解方法

**解法**：
- 導入 SPIDR（刀法）+ INVEST（品管）
- 建立團隊共識的拆解 SOP

---

## 🔪 SPIDR：刀法 - 從哪裡下刀？

> 解決「我知道這張太大，但不知道從哪裡切」的問題

### SPIDR 五個切入角度

| 切法 | 英文 | 說明 | 適用時機 |
|------|------|------|----------|
| **S** | Spike | 技術探索、風險驗證 | 技術不確定性高時 |
| **P** | Paths | 使用路徑 | 多種使用者流程 |
| **I** | Interfaces | 介面 | 多種呈現方式 |
| **D** | Data | 資料 | 不同資料類型/來源 |
| **R** | Rules | 規則 | 複雜業務邏輯 |

---

### 實戰範例：發送免費券

#### 原始 Story（太大）
```
作為行銷人員，我想要發送免費券給會員
- 規則十幾條
- Scenario 快三十個
- 一個 Sprint 做不完
```

#### 用 Paths（使用路徑）拆解

發現其實是完全不同的使用路徑：

```
✅ 拆解後：
Story 1: 首次註冊發券
  - 新會員註冊時自動發送歡迎券
  - 發送後記錄到會員帳戶
  - 發送失敗時發送通知給行銷

Story 2: 滿額門檻發券
  - 消費滿 1000 元自動發券
  - 同一筆訂單只能觸發一次
  - 需扣除退貨金額重新計算

Story 3: 手動指定對象發券
  - 行銷人員可從後台選擇會員清單
  - 批次發送前需預覽影響範圍
  - 可設定發送時間排程
```

這三個本質就應該拆開，因為：
- 觸發時機不同
- 業務規則不同
- 使用者角色不同（系統自動 vs 行銷人員操作）

---

#### 再用 Rules（規則）拆解

```
✅ 每條規則背後的判斷邏輯、例外處理都不同：

Story 1: 免費券限領規則
  - 每人限領一次（首次註冊券）
  - 記錄領取時間與來源

Story 2: 免費券過期處理
  - 過期自動失效
  - 過期前 3 天發送提醒通知

Story 3: 免費券併用規則
  - 檢查與其他優惠是否可併用
  - 優先順序處理（折扣碼 > 免費券）
```

**為什麼要這樣拆？**
- 硬塞在同一張 Story 裡，Scenario 當然寫到快二十個
- Refinement 時間當然收不住
- 測試案例複雜度爆炸

---

### SPIDR 快速決策樹

```
遇到大 Story 時：

1. 是否有技術不確定性？
   └─ Yes → Spike 先行

2. 是否有多種使用路徑？
   └─ Yes → 按 Paths 拆解

3. 是否有多種介面呈現？
   └─ Yes → 按 Interfaces 拆解

4. 是否處理多種資料類型？
   └─ Yes → 按 Data 拆解

5. 是否有複雜業務規則？
   └─ Yes → 按 Rules 拆解

通常一張大 Story 可以組合使用多個切法。
```

---

## ✅ INVEST：品管 - 拆得好不好？

> 解決「我拆完了，但拆得好不好？」的問題

### Bill Wake 的 6 個檢驗原則

每拆出一張 Story 就問自己（可用 AI 自動檢測）：

| 原則 | 英文 | 檢驗問題 | 不合格範例 |
|------|------|----------|------------|
| **I** | Independent | 能不能獨立交付？ | 前端 UI 卡片（需等後端 API） |
| **N** | Negotiable | 細節是否保留協商空間？ | 寫死實作方式 |
| **V** | Valuable | 有沒有明確的使用者價值？ | 重構資料庫架構（技術債） |
| **E** | Estimable | 團隊估不估得出大小？ | 需求模糊、技術不明 |
| **S** | Small | 一個 Sprint 做不做得完？ | 規則 10+ 條、Scenario 20+ 個 |
| **T** | Testable | 測試案例寫不寫得出來？ | 沒有明確的驗收標準 |

---

### 特別說明：Negotiable（N）

> 這是最容易被誤解的一個原則

**Negotiable 要講的是**：
Story 的細節應該保留協商空間，不要在 Refinement 階段就把實作方式寫死。

#### ❌ 錯誤：寫死實作方式
```
作為會員，我想要用 Redis Cache 來加速會員資料查詢，
使用 LRU 演算法，Cache 有效期設定為 30 分鐘。
```

**問題**：
- 限制了技術選型的彈性
- 團隊可能有更好的解法（如 CDN、Database Index）
- 需求應該描述「什麼」，不是「怎麼做」

#### ✅ 正確：保留協商空間
```
作為會員，我想要快速查詢我的個人資料，
使得頁面載入時間 < 1 秒。

Acceptance Criteria:
- Given 我登入後
- When 我點擊「個人資料」
- Then 頁面在 1 秒內完整顯示
```

**好處**：
- 團隊可以討論最佳實作方式
- 可能發現更簡單的解法（如加 Index 就夠了）
- 保持對技術演進的開放性

---

### INVEST 檢查清單

```markdown
## Story 品質檢驗

拆出 Story 後，逐項檢查：

- [ ] **Independent**: 這張 Story 可以獨立交付到 Production 嗎？
- [ ] **Negotiable**: 有沒有寫死實作方式？還有協商空間嗎？
- [ ] **Valuable**: 使用者或客戶能感受到價值嗎？
- [ ] **Estimable**: 團隊能估出 Story Point 嗎？（不確定性低於 50%）
- [ ] **Small**: 能在 1 個 Sprint 內完成嗎？（建議 1-5 天）
- [ ] **Testable**: 能寫出明確的測試案例嗎？（Gherkin Scenario）

如果任何一項答案是「模糊的」或「否」，代表：還沒拆到位。
```

---

## 🔁 SPIDR + INVEST 組合技

> SPIDR 是刀法，INVEST 是品管

### 完整拆解流程

```
Step 1: 用 SPIDR 拆解
  └─ 從 5 個切入角度找出拆解點
  └─ 產出多張候選 Story

Step 2: 用 INVEST 品檢
  └─ 逐張檢驗 6 個原則
  └─ 不合格的繼續拆或調整

Step 3: 實例化需求（Gherkin）
  └─ 為每張 Story 寫出 Scenario
  └─ 確保 Testable（T）

Step 4: 估算 & 排優先序
  └─ 團隊估點數（Planning Poker）
  └─ PO 排優先序

Step 5: Sprint Planning
  └─ 選入當次 Sprint
  └─ 再次確認 INVEST
```

---

## 🎯 PM 必備技能：拆單分工的藝術

> 針對 PM 角色的特別提醒

### PM 在 Story 拆解的三大職責

#### 1. **守門員**：確保 Story 品質
- 不讓模糊的 Story 進入 Sprint
- 堅持 INVEST 原則（特別是 V - Valuable）
- 拒絕「技術任務偽裝成 Story」

#### 2. **翻譯官**：連接商業與技術
- 把客戶需求翻譯成 Story
- 把技術限制翻譯給客戶聽
- 確保雙方理解一致

#### 3. **協調者**：引導 Refinement
- 帶領團隊用 SPIDR 拆解
- 確保 Scenario 討論聚焦
- 控制會議時間（Timebox）

---

### PM 拆單時要考慮的 5 個面向

| 面向 | 考量點 | 範例 |
|------|--------|------|
| **價值優先** | 哪個先做對客戶價值最大？ | 核心流程 > 例外處理 |
| **依賴關係** | 哪些 Story 有先後順序？ | 註冊 → 登入 → 權限 |
| **風險管理** | 技術風險高的先做 Spike | 第三方 API 整合不確定 |
| **團隊產能** | 團隊同時能處理幾張？ | 避免 WIP 過高 |
| **交付頻率** | 多久能 demo 一次價值？ | 每週至少一次可 demo |

---

### PM 常見錯誤與修正

| ❌ 錯誤做法 | ✅ 正確做法 |
|-----------|-----------|
| Story 寫完直接丟給團隊 | Refinement 一起討論細節 |
| 怕拆太細被說灌點數 | 用 INVEST 證明拆解合理性 |
| 一張 Story 塞滿所有規則 | 用 SPIDR 系統化拆解 |
| 只寫 User Story，不寫 Scenario | 用 Gherkin 實例化需求 |
| 技術任務偽裝成 User Story | 技術債獨立追蹤，不混入 Story |

---

## 📝 實戰範本與工具

### User Story 範本（推薦格式）

```markdown
## Story: [簡短標題]

**As a** [角色]
**I want to** [功能]
**So that** [商業價值]

---

### Acceptance Criteria

#### Scenario 1: [主要成功路徑]
**Given** [前置條件]
**When** [操作]
**Then** [預期結果]

#### Scenario 2: [例外處理]
**Given** [前置條件]
**When** [操作]
**Then** [預期結果]

---

### Business Rules

1. [關鍵規則 1]
2. [關鍵規則 2]

---

### Notes
- [技術備註]
- [UI/UX 參考]
- [依賴項目]

---

### Definition of Done
- [ ] 程式碼完成且 Code Review
- [ ] 單元測試覆蓋率 > 80%
- [ ] 整合測試通過
- [ ] QA 驗收通過
- [ ] 部署到 Staging
- [ ] 文件更新
```

---

### Refinement 會議範本

```markdown
## Refinement Agenda（預計 60 分鐘）

### 1. Story 概述（5 分鐘）
- PM 說明背景與商業價值
- 展示 Mockup / 參考資料

### 2. 拆解討論（30 分鐘）
- 團隊用 SPIDR 識別拆解點
- 識別 Paths / Rules / Data 等切法
- 逐張拆出子 Story

### 3. Scenario 討論（15 分鐘）
- 為每張 Story 寫出 Gherkin Scenario
- 識別邊界條件與例外處理

### 4. INVEST 品檢（5 分鐘）
- 逐張檢驗 6 個原則
- 不合格的標記，下次再討論

### 5. 估算（5 分鐘）
- Planning Poker
- 記錄估點與不確定性

---

### Output
- [ ] 拆解後的 Story 清單
- [ ] 每張 Story 的 Scenario
- [ ] Story Point 估算
- [ ] 依賴關係標記
```

---

## 🎓 教學團隊的引導技巧

### 第一次教 Story 拆解時

#### ❌ 不要這樣教
```
「User Story 要符合 INVEST 原則...」
（照著投影片念一遍）

結果：團隊禮貌地點頭，然後就沒有然後了。
```

#### ✅ 這樣教更有效
```
Step 1: 帶一個真實的爛 Story
「這張 Story 為什麼做不完？」

Step 2: 讓團隊自己發現問題
「你們覺得這張太大的原因是什麼？」

Step 3: 引導使用 SPIDR
「我們試試看用『使用路徑』來拆拆看」

Step 4: 用 INVEST 驗證
「這張拆完的 Story，能獨立交付嗎？」

Step 5: 實際演練
「下週 Refinement 我們用這個方法試試」
```

---

### 建立團隊共識的 4 個階段

| 階段 | 目標 | 做法 |
|------|------|------|
| **1. 認知** | 理解為什麼要拆 | 回顧過去「做不完」的 Sprint |
| **2. 學習** | 學會怎麼拆 | Workshop：SPIDR + INVEST |
| **3. 演練** | 實際操作 | Refinement 現場引導 |
| **4. 內化** | 養成習慣 | 每次 Sprint Review 檢討 Story 品質 |

---

## 🚨 Story 拆不好的警訊

### Sprint 中的紅燈信號

- [ ] **第三天才發現需求遺漏**
  - → 代表 Scenario 討論不夠細

- [ ] **QA 測到一半發現規則衝突**
  - → 代表 Business Rules 沒釐清

- [ ] **Dev 說「這個當初沒講」**
  - → 代表 Story 細節保留太多空白

- [ ] **Sprint Review 只能 demo 半成品**
  - → 代表 Story 沒有按價值拆分

- [ ] **常態性加班趕工**
  - → 代表估算失準，Story 太大

---

### Refinement 時的紅燈信號

- [ ] **會議常常超時**
  - → 代表 Story 太大、太複雜

- [ ] **團隊估不出點數**
  - → 代表不確定性太高

- [ ] **Scenario 寫不出來**
  - → 代表需求太模糊

- [ ] **討論變得很發散**
  - → 代表 Story 範圍沒界定清楚

---

## 🎯 給不同角色的建議

### 給 PM（Product Manager）
> 你是 Story 品質的第一道防線

**三個堅持**：
1. **堅持拆小**：寧可被說灌點數，不要 Sprint 做不完
2. **堅持價值**：每張 Story 都要有明確的使用者價值
3. **堅持驗證**：用 INVEST 檢驗，不合格就不進 Backlog

**三個不做**：
1. **不寫死實作**：保留 Negotiable 空間
2. **不跳過 Refinement**：省 30 分鐘，賠整個 Sprint
3. **不讓技術債偽裝成 Story**：分開追蹤

---

### 給 BA（Business Analyst）/ 需求分析師
> 你是需求與實作的橋樑

**核心任務**：
1. **釐清模糊需求**：用 Gherkin 實例化
2. **識別邊界條件**：把「例外」變成「Scenario」
3. **協助拆解**：用 SPIDR 引導 Refinement

**輸出品質標準**：
- 每張 Story 至少 2 個 Scenario（正常 + 例外）
- Business Rules 明確列出
- Acceptance Criteria 可測試

---

### 給 Architect（架構師）
> 你要確保技術可行性

**參與 Refinement 的價值**：
1. **及早識別技術風險**：需要 Spike 的盡早做
2. **避免過度設計**：Negotiable 原則很重要
3. **確保技術債可控**：拆解時考慮重構時機

**提醒團隊**：
- 不要在 Story 裡寫死技術方案
- 保留實作彈性
- 技術債獨立追蹤

---

### 給 QA（Quality Assurance）
> 你要確保 Story 可測試

**Refinement 時的關鍵角色**：
1. **檢查 Testable**：能寫出測試案例嗎？
2. **補充邊界條件**：「如果...會怎樣？」
3. **驗證 Scenario 完整性**：有沒有遺漏的路徑？

**測試案例設計**：
- 從 Gherkin Scenario 直接轉成測試案例
- 確保每個 Business Rule 都有對應測試
- 例外處理也要測試

---

### 給 Dev（Developer）
> 你要確保 Story 可估算、可實作

**Refinement 時要問的問題**：
1. **能估算嗎？**（Estimable）
2. **能獨立做嗎？**（Independent）
3. **一個 Sprint 做得完嗎？**（Small）

**實作時的原則**：
- 先做核心路徑（Happy Path）
- 例外處理分開拆 Story
- 隨時回頭檢查 Acceptance Criteria

---

## 📚 延伸學習資源

### 核心概念來源

- **INVEST** - Bill Wake (2003)
  - 原文：https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/

- **SPIDR** - Mike Cohn
  - 書籍：《User Stories Applied》

- **實例化需求** - Gojko Adzic
  - 書籍：《Specification by Example》

---

### 推薦閱讀順序

1. **入門**：《User Story Mapping》by Jeff Patton
2. **進階**：《Specification by Example》by Gojko Adzic
3. **實戰**：《Agile Estimating and Planning》by Mike Cohn

---

## 🎬 結語

### 核心心法

> Story 拆不好，多半不是技術能力的問題，
> 是缺一個團隊能共用的思考框架。

**與其每次 Sprint Review 費力解釋為什麼沒做完，
不如在 Refinement 多留 30 分鐘：**
- 把 Story 拆清楚
- 把邊界條件講仔細

**那三十分鐘省下來的，是整個 Sprint 的混亂跟返工。**

---

### SPIDR + INVEST 總結

```
SPIDR = 刀法（從哪裡切）
  ├─ Spike: 技術不確定時先探索
  ├─ Paths: 按使用路徑拆
  ├─ Interfaces: 按介面拆
  ├─ Data: 按資料類型拆
  └─ Rules: 按業務規則拆

INVEST = 品管（切得好不好）
  ├─ Independent: 能獨立交付嗎？
  ├─ Negotiable: 有協商空間嗎？
  ├─ Valuable: 有使用者價值嗎？
  ├─ Estimable: 能估算嗎？
  ├─ Small: 一個 Sprint 做得完嗎？
  └─ Testable: 能寫測試案例嗎？
```

---

**Version**: 1.0 | **Created**: 2026-02-05 | **Based on**: 實戰經驗淬鍊

