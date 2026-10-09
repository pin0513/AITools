# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale。哪類圖要做哪些確認見 rules/review/duties.yaml。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | 6a37522020bb | pending |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | 6a37522020bb | pending |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | 74bae04a5683 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | b6d18f4958da | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | b6d18f4958da | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 5f16c2ac602a | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 5f16c2ac602a | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 31a5dfc252ae | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 31a5dfc252ae | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | dd19c757a3a6 | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | dd19c757a3a6 | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | 0419c13602c6 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | 0419c13602c6 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 373cf25b4e91 | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 373cf25b4e91 | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 96bd4c2be895 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 96bd4c2be895 | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | a2e6a2a04031 | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | a2e6a2a04031 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | 1abf07bf0ed1 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 92eb9479e001 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 9ccbaee83cc5 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 266b82ca1d7d | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | d3722604a8c2 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | d3722604a8c2 | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 596691978cc5 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 596691978cc5 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 3b60527d4ae3 | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 3b60527d4ae3 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | d8dd9e92b51d | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | 4a98084d0568 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | 4a98084d0568 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 6457fd428276 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 1e229dd1e10a | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 1e229dd1e10a | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | a0f4e4223f08 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 0429bc4f9d55 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 0429bc4f9d55 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 99ddcf4c7d6f | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | e7fdad8a69c9 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | e7fdad8a69c9 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 134d93b2025f | pending |  |  |  |
