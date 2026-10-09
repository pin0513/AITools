# points-redemption SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:rewards.html, ref:refs.md · CJK 候選 0 → 邊界熵後 0 → 去冗後 0

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| points | 18 | 18.0 |  | — | 升 | mock:rewards.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A member |
| balance | 6 | 6.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§4 Non-functi pm_spec:pm-spec.md§5 Acceptance |
| points transaction | 6 | 6.0 | PointTransaction | 0 | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§3.3 A member pm_spec:pm-spec.md§5 Acceptance |
| reward | 6 | 6.0 | Reward | 0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§5 Acceptance |
| points account | 4 | 4.0 | PointsAccount | 5 (src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs:7) | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§4 Non-functi |
| redemption | 4 | 4.0 | Redemption | 0 | 升 | mock:rewards.html pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§4 Non-functi pm_spec:pm-spec.md§5 Acceptance |
| points account balance | 3 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§4 Non-functi |
| balance covers | 2 | 2.0 |  | — | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§5 Acceptance |
| date | 2 | 2.0 |  | — | 升 | pm_spec:pm-spec.md§3.3 A member pm_spec:pm-spec.md§5 Acceptance |
| expiry points transaction | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§5 Acceptance |
| job | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§5 Acceptance |
| monthly | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 Points e pm_spec:pm-spec.md§5 Acceptance |
| online | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§1 Background |
| reward vendor | 2 | 2.0 | RewardVendor | 0 | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§5 Acceptance |
| type | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 A member pm_spec:pm-spec.md§5 Acceptance |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| redeem | 7 | 7.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A member |
| deduct | 2 | 2.0 | 升 | pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§5 Acceptance |
| expire | 2 | 2.0 | 升 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 Points e |
| view | 2 | 2.0 | 升 | mock:rewards.html pm_spec:pm-spec.md§3.3 A member |
| create | 1 | 1.0 | 降 | pm_spec:pm-spec.md§5 Acceptance |
| earn | 1 | 1.0 | 降 | pm_spec:pm-spec.md§5 Acceptance |
| fulfill | 1 | 1.0 | 降 | pm_spec:pm-spec.md§3.1 A member |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| member | 8 | 8.0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A member pm_spec:pm-spec.md§3.3 A member |
| system | 2 | 2.0 | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 Points e |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| pending | 2 | mock:rewards.html pm_spec:pm-spec.md§3.1 A member |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| points | 16 | 2 (src/api/Loyalty.Api/Controllers/PointsController.cs:10) | mock:rewards.html pm_spec:pm-spec.md |
| member | 8 | 0 | pm_spec:pm-spec.md |
| balance | 6 | 3 (src/database/001_pointsaccounts.sql:4) | pm_spec:pm-spec.md |
| reward | 6 | 0 | pm_spec:pm-spec.md |
| transaction | 6 | 0 | pm_spec:pm-spec.md |
| redeem | 5 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| account | 4 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| redemption | 4 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| covers | 2 | 0 | pm_spec:pm-spec.md |
| date | 2 | 0 | pm_spec:pm-spec.md |
| deducted | 2 | 0 | pm_spec:pm-spec.md |
| expire | 2 | 0 | pm_spec:pm-spec.md |
| expiry | 2 | 0 | pm_spec:pm-spec.md |
| monthly | 2 | 0 | pm_spec:pm-spec.md |
| months | 2 | 0 | pm_spec:pm-spec.md |
| online | 2 | 0 | pm_spec:pm-spec.md |
| redeems | 2 | 0 | pm_spec:pm-spec.md |
| system | 2 | 0 | pm_spec:pm-spec.md |
| type | 2 | 3 (src/web/src/types/PointsAccount.ts:2) | pm_spec:pm-spec.md |
| vendor | 2 | 0 | pm_spec:pm-spec.md |
| view | 2 | 0 | mock:rewards.html pm_spec:pm-spec.md |
| Goal | 1 | 0 | pm_spec:pm-spec.md |
| INSUFFICIENT_POINTS | 1 | 0 | pm_spec:pm-spec.md |
| Pending | 1 | 0 | mock:rewards.html |
| Points | 1 | 2 (src/api/Loyalty.Api/Controllers/PointsController.cs:10) | pm_spec:pm-spec.md |
| become | 1 | 0 | pm_spec:pm-spec.md |
| called | 1 | 0 | pm_spec:pm-spec.md |
| cannot | 1 | 0 | pm_spec:pm-spec.md |
| collects | 1 | 0 | pm_spec:pm-spec.md |
| concurrent | 1 | 0 | pm_spec:pm-spec.md |
| cost | 1 | 0 | pm_spec:pm-spec.md |
| created | 1 | 0 | pm_spec:pm-spec.md |
| drops | 1 | 0 | pm_spec:pm-spec.md |
| each | 1 | 0 | pm_spec:pm-spec.md |
| earned | 1 | 0 | pm_spec:pm-spec.md |
| enough | 1 | 0 | pm_spec:pm-spec.md |
| even | 1 | 0 | pm_spec:pm-spec.md |
| every | 1 | 0 | pm_spec:pm-spec.md |
| fulfills | 1 | 0 | pm_spec:pm-spec.md |
| history | 1 | 0 | pm_spec:pm-spec.md |
