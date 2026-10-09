# 訂單取消與退款 — test design

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | OrderDetailPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-002 | CancelOrderDialogTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | CancellationHistoryTableTests | unit | CMP-003 | AC-003-1 |
| TST-004 | orderStoreTests | unit | CMP-004 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-005 | ordersApiTests | contract | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-006 | OrdersControllerTests | integration | CMP-006 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-007 | CancelOrderCommandHandlerTests | unit | CMP-007 | AC-001-1, AC-001-2 |
| TST-008 | IssueRefundCommandHandlerTests | unit | CMP-008 | AC-002-1, AC-002-2 |
| TST-009 | ListCancellationsQueryHandlerTests | unit | CMP-009 | AC-003-1 |
| TST-010 | OrderTests | unit | CMP-010 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-011 | SqlOrderRepositoryTests | integration | CMP-011 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-012 | PaymentGatewayClientTests | contract | CMP-012 | AC-002-1, AC-002-2 |
| TST-013 | NFR-001FitnessTest | e2e | CMP-006 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 / Playwright | P95 < 5 min | CI nightly |
