# points-redemption SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:rewards.html, ref:refs.md · CJK 候選 72 → 邊界熵後 30 → 去冗後 29

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| pointtransaction | 7 | 11.0 | PointTransaction | 0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§3.3 member 可 |
| 餘額 | 6 | 11.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 pm_spec:pm-spec.md§5 驗收條件 |
| 點數 | 7 | 10.0 |  | — | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§3.3 member 可 |
| reward | 5 | 8.0 | Reward | 0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |
| pointsaccount | 4 | 6.0 | PointsAccount | 3 (src/web/src/types/PointsAccount.ts:4) | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§4 非功能需求 |
| redemption | 3 | 4.0 | Redemption | 0 | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |
| member pointtransaction | 2 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§5 驗收條件 |
| reward redemption | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |
| rewardvendor | 2 | 3.0 | RewardVendor | 0 | 升 | pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |
| 扣點 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |
| 日期 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 member 可 pm_spec:pm-spec.md§5 驗收條件 |
| 類型 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 member 可 pm_spec:pm-spec.md§5 驗收條件 |
| 餘額足夠 | 2 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§5 驗收條件 |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| redeem | 8 | 13.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 PointsAc |
| expire | 4 | 6.0 | 升 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |
| view | 3 | 4.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.3 member 可 |
| 建立 | 1 | 2.0 | 降 | pm_spec:pm-spec.md§5 驗收條件 |
| 出貨 | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 PointsAc |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| member | 8 | 13.0 | 升 | pm_spec:pm-spec.md§1 背景與目標 pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.1 PointsAc pm_spec:pm-spec.md§3.3 member 可 |
| system | 2 | 3.0 | 降 | pm_spec:pm-spec.md§2 使用者與情境 pm_spec:pm-spec.md§3.2 點數 12 個月 |
| 月排程 | 2 | 3.0 | 降 | pm_spec:pm-spec.md§3.2 點數 12 個月 pm_spec:pm-spec.md§5 驗收條件 |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| pending | 2 | mock:rewards.html pm_spec:pm-spec.md§3.1 PointsAc |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| member | 8 | 0 | pm_spec:pm-spec.md |
| redeem | 8 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| PointTransaction | 7 | 0 | pm_spec:pm-spec.md |
| Reward | 5 | 0 | pm_spec:pm-spec.md |
| PointsAccount | 4 | 3 (src/web/src/types/PointsAccount.ts:4) | mock:rewards.html pm_spec:pm-spec.md |
| expire | 4 | 0 | pm_spec:pm-spec.md |
| Redemption | 3 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| view | 3 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| RewardVendor | 2 | 0 | pm_spec:pm-spec.md |
| system | 2 | 0 | pm_spec:pm-spec.md |
| Pending | 2 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| INSUFFICIENT_POINTS | 1 | 0 | pm_spec:pm-spec.md |
| mock | 1 | 0 | mock:rewards.html |
| status | 1 | 1 (src/web/src/types/PointsAccount.ts:6) | mock:rewards.html |
| shape | 1 | 0 | ref:refs.md |
