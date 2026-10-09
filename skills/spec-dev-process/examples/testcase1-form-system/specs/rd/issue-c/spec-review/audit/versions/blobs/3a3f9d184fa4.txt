# 表單審核流程 — 測試設計

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | FormSubmissionTests | unit | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-002-3, AC-003-1, AC-003-2, AC-004-2 |
| TST-002 | ApproveSubmissionCommandHandlerTests | unit | CMP-002 | AC-002-1, AC-N03-1 |
| TST-003 | RejectSubmissionCommandHandlerTests | unit | CMP-003 | AC-002-2, AC-002-3, AC-N03-1 |
| TST-004 | ResubmitSubmissionCommandHandlerTests | unit | CMP-004 | AC-001-2, AC-003-1, AC-003-2 |
| TST-005 | SubmissionsControllerTests | integration | CMP-001 | AC-002-1, AC-002-2, AC-N01-1 |
| TST-006 | ReviewReminderJobTests | unit | CMP-008 | AC-004-1, AC-004-2 |
| TST-007 | SqlFormSubmissionRepositoryTests | integration | CMP-006 | AC-004-1, AC-N02-1 |
| TST-008 | EmailNotifierContractTests | contract | CMP-007 | AC-002-3, AC-004-1 |
| TST-009 | PendingReviewsQueryHandlerTests | unit | CMP-009 | AC-002-1 |
| TST-010 | WorkdayCalendarTests | unit | CMP-010 | AC-004-1 |
| TST-011 | ReviewApiLoadTest(k6) | e2e | CMP-001 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 對 API-002/API-003 | P95 < 1s @ 50 VU | CI nightly |
| NFR-002 | TST-007 嘗試 DELETE/UPDATE ReviewRecord | 100% 被 trigger 拒絕 | CI |
| NFR-003 | TST-002/TST-003 非審核者 | 100% 403 | CI |

## 架構測試
| 規則 | 工具 | 斷言 |
|---|---|---|
| B2 | NetArchTest | Forms.Domain 不依賴 Forms.Application / Forms.Infrastructure / Forms.Api |
| B4 | NetArchTest | 只有 Forms.Infrastructure 可引用 System.Net.Mail |
