# 會員點數兌換 — test design

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | RewardsPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-003-1 |
| TST-002 | pointsApiTests | contract | CMP-002 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-003 | PointsControllerTests | integration | CMP-003 | AC-001-1, AC-001-2, AC-003-1 |
| TST-004 | RedeemRewardCommandHandlerTests | unit | CMP-004 | AC-001-1, AC-001-2 |
| TST-005 | ExpirePointsJobTests | unit | CMP-005 | AC-002-1 |
| TST-006 | ListTransactionsQueryHandlerTests | unit | CMP-006 | AC-003-1 |
| TST-007 | RedemptionTests | unit | CMP-007 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-008 | SqlPointsAccountRepositoryTests | integration | CMP-008 | AC-001-1, AC-001-2, AC-002-1, AC-003-1 |
| TST-009 | RewardVendorClientTests | contract | CMP-009 | AC-001-1, AC-001-2 |
| TST-010 | NFR-001FitnessTest | e2e | CMP-003 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 / Playwright | balance never negative | CI nightly |
