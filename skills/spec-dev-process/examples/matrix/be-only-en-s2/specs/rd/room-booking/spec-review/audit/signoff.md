# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale。哪類圖要做哪些確認見 rules/review/duties.yaml。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | 1495f21f8393 | pending |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | 1495f21f8393 | pending |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | a1080cad4be9 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 7813f8a7c922 | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 7813f8a7c922 | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | e428660cb058 | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | e428660cb058 | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | decb50720d5f | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | decb50720d5f | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | ffdc4dab7695 | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | ffdc4dab7695 | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 57f622622ebc | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 57f622622ebc | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | b4621356316a | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | b4621356316a | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | a7caf0eea95b | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | a7caf0eea95b | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 7b3c60863f55 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 7b3c60863f55 | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 2ce5093b1e1b | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 2ce5093b1e1b | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | aecc2d329bb7 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | bf1f4f253c98 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 9ccbaee83cc5 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 72624a6a5884 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | dbd48bd2fc46 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | dbd48bd2fc46 | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 8350d9a66478 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 8350d9a66478 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | f499498e713e | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | f499498e713e | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 236356a94b6b | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | a2e3c51b7894 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | a2e3c51b7894 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | cd1da22b48c2 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | f36fb6c36aeb | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | f36fb6c36aeb | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | c81aa8d50ea1 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | da7671fbe97f | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | da7671fbe97f | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 297ba4b20fa4 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 5e6822484557 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 5e6822484557 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | f8387c5a8f4e | pending |  |  |  |
