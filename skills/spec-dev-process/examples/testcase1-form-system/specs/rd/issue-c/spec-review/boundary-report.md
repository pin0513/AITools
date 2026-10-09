# 表單審核流程 — 技術邊界核對報告

<!-- 由 spec-dev.py check 產生,不要手改 -->

| 規則 | 目標 | 狀態 | 證據 | 處置 |
|---|---|---|---|---|
| B1 | NFR-001 | PASS | link → CMP-001 |  |
| B1 | NFR-002 | PASS | link → CMP-005, CMP-006 |  |
| B1 | NFR-003 | PASS | link → CMP-002, CMP-003 |  |
| B1 | REQ-001 | PASS | link → CMP-004, CMP-005 |  |
| B1 | REQ-002 | PASS | link → CMP-001, CMP-002, CMP-003, CMP-005, CMP-006, CMP-007 |  |
| B1 | REQ-003 | PASS | link → CMP-004, CMP-005 |  |
| B1 | REQ-004 | PASS | link → CMP-005, CMP-006, CMP-007, CMP-008, CMP-010 |  |
| B2 | CMP-001 | PASS | Api → CMP-002 (Application) |  |
| B2 | CMP-001 | PASS | Api → CMP-003 (Application) |  |
| B2 | CMP-001 | PASS | Api → CMP-004 (Application) |  |
| B2 | CMP-001 | PASS | Api → CMP-009 (Application) |  |
| B2 | CMP-002 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-002 | PASS | Application → CMP-006 經介面 IFormSubmissionRepository(modify) |  |
| B2 | CMP-003 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-003 | PASS | Application → CMP-006 經介面 IFormSubmissionRepository(modify) |  |
| B2 | CMP-003 | PASS | Application → CMP-007 經介面 INotifier(existing) |  |
| B2 | CMP-004 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-004 | PASS | Application → CMP-006 經介面 IFormSubmissionRepository(modify) |  |
| B2 | CMP-008 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-008 | PASS | Application → CMP-006 經介面 IFormSubmissionRepository(modify) |  |
| B2 | CMP-008 | PASS | Application → CMP-007 經介面 INotifier(existing) |  |
| B2 | CMP-008 | PASS | Application → CMP-010 經介面 IWorkdayCalendar(new) |  |
| B2 | CMP-009 | PASS | Application → CMP-006 經介面 IFormSubmissionRepository(modify) |  |
| B4 | CMP-007 | PASS | SMTP 在 Infrastructure 且有失敗模式 |  |
| B5 | Form | PASS | owner = Forms |  |
| B5 | FormSubmission | PASS | owner = Forms |  |
| B5 | ReviewRecord | PASS | owner = Forms |  |
| B5 | ReviewReminder | PASS | owner = Forms |  |
| B6 | NFR-001 | PASS | 綁定 API-002, API-003 |  |
| B6 | NFR-002 | PASS | 綁定 CMP-005, CMP-006 |  |
| B6 | NFR-003 | PASS | 綁定 CMP-002, CMP-003 |  |
| B7 | AC-001-1 | PASS | → TST-001 |  |
| B7 | AC-001-2 | PASS | → TST-001, TST-004 |  |
| B7 | AC-002-1 | PASS | → TST-001, TST-002, TST-005, TST-009 |  |
| B7 | AC-002-2 | PASS | → TST-001, TST-003, TST-005 |  |
| B7 | AC-002-3 | PASS | → TST-001, TST-003, TST-008 |  |
| B7 | AC-003-1 | PASS | → TST-001, TST-004 |  |
| B7 | AC-003-2 | PASS | → TST-001, TST-004 |  |
| B7 | AC-004-1 | PASS | → TST-006, TST-007, TST-008, TST-010 |  |
| B7 | AC-004-2 | PASS | → TST-001, TST-006 |  |
| B7 | AC-N01-1 | PASS | → TST-005, TST-011 |  |
| B7 | AC-N02-1 | PASS | → TST-007 |  |
| B7 | AC-N03-1 | PASS | → TST-002, TST-003 |  |
