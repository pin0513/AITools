# points-redemption SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:rewards.html, ref:refs.md · CJK 候選 228 → 邊界熵後 73 → 去冗後 71

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| 點數 | 18 | 27.0 |  | — | 升 | mock:rewards.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 |
| 獎品 | 7 | 11.0 | Reward | 0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |
| 點數交易 | 7 | 11.0 | PointTransaction | 0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§3.3 會員可查看點數交 |
| 餘額 | 6 | 11.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 pm_spec:pm-spec.md§5 驗收條件 |
| 兌換獎品 | 5 | 8.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |
| 點數帳 | 5 | 7.0 |  | — | 升 | mock:rewards.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 |
| 點數帳戶 | 4 | 6.0 | PointsAccount | 5 (src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs:7) | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 |
| 數帳戶餘額 | 3 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 |
| 點數帳戶餘 | 3 | 5.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 |
| 兌換單 | 3 | 4.0 | Redemption | 0 | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |
| 員兌換獎品 | 2 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§5 驗收條件 |
| 會員兌換獎 | 2 | 4.0 |  | — | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 到期點數交 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |
| 扣點 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |
| 日期 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 會員可查看點數交 pm_spec:pm-spec.md§5 驗收條件 |
| 期點數交易 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |
| 獎品供應商 | 2 | 3.0 | RewardVendor | 0 | 升 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |
| 類型 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 會員可查看點數交 pm_spec:pm-spec.md§5 驗收條件 |
| 餘額足夠 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§5 驗收條件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 兌換 | 12 | 18.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 |
| 到期 | 4 | 6.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |
| 查看 | 3 | 4.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 會員可查看點數交 |
| 行兌換 | 1 | 3.0 | 降 | pm_spec:pm-spec.md§4 非功能需求 |
| 線上兌換 | 2 | 2.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 |
| 數交易顯示 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 舊點數到期 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 |
| 以查看 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.3 會員可查看點數交 |
| 供應商出貨 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 |
| 寫一筆到期 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.2 點數 12 個月 |
| 法線上兌換 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§1 背景與目標 |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| 會員 | 8 | 13.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 pm_spec:pm-spec.md§3.3 會員可查看點數交 |
| 月排程 | 2 | 3.0 | 降 | pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |
| 系統 | 2 | 3.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 點數 12 個月 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| pending | 1 | mock:rewards.html |
| 待兌換 | 1 | pm_spec:pm-spec.md§3.1 點數帳戶點數足夠 |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| INSUFFICIENT_POINTS | 1 | 0 | pm_spec:pm-spec.md |
| Pending | 1 | 0 | mock:rewards.html |
| mock | 1 | 0 | mock:rewards.html |
| status | 1 | 2 (src/api/Loyalty.Domain/PointsAccount.cs:3) | mock:rewards.html |
| shape | 1 | 0 | ref:refs.md |
