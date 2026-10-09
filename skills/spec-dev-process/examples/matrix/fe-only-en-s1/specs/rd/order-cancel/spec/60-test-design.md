# Order cancellation and refund — test design

## Test Components
| ID | Name | kind | CMP Refs | AC Refs |
|---|---|---|---|---|
| TST-001 | OrderDetailPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-002 | CancelOrderDialogTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | CancellationHistoryTableTests | unit | CMP-003 | AC-003-1 |
| TST-004 | orderStoreTests | unit | CMP-004 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-005 | ordersApiTests | contract | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-006 | NFR-001FitnessTest | e2e | CMP-005 | AC-N01-1 |

## Fitness Function
| NFR | Measurement | Threshold | Where |
|---|---|---|---|
| NFR-001 | k6 / Playwright | P95 < 5 min | CI nightly |
