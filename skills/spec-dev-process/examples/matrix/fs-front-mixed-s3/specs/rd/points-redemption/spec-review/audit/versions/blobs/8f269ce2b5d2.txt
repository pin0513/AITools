# 會員點數兌換 — test design

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | RewardsPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-003-1 |
| TST-002 | RedeemDialogTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | TransactionListTests | unit | CMP-003 | AC-003-1 |
| TST-004 | rewardsStoreTests | unit | CMP-004 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-005 | pointsApiTests | contract | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-006 | PointsControllerTests | integration | CMP-006 | AC-001-1, AC-001-2, AC-003-1 |
| TST-007 | RedeemRewardCommandHandlerTests | unit | CMP-007 | AC-001-1, AC-001-2 |
| TST-008 | ExpirePointsJobTests | unit | CMP-008 | AC-002-1 |
| TST-009 | ListTransactionsQueryHandlerTests | unit | CMP-009 | AC-003-1 |
| TST-010 | SqlPointsAccountRepositoryTests | integration | CMP-010 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-011 | RewardVendorClientTests | contract | CMP-011 | AC-001-1, AC-001-2 |
| TST-012 | NFR-001FitnessTest | e2e | CMP-006 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 / Playwright | balance never negative | CI nightly |
