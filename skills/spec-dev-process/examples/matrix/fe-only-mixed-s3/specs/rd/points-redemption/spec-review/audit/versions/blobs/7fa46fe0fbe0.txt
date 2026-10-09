# 會員點數兌換 — test design

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | RewardsPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-003-1 |
| TST-002 | RedeemDialogTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | TransactionListTests | unit | CMP-003 | AC-003-1 |
| TST-004 | rewardsStoreTests | unit | CMP-004 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-005 | pointsApiTests | contract | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-006 | NFR-001FitnessTest | e2e | CMP-005 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 / Playwright | balance never negative | CI nightly |
