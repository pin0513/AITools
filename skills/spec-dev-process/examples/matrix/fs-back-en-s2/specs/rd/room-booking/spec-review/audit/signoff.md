# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale;「版本」是確認當時的文件版本,之後它依據的需求或 PM 段落變了 → upstream(上游已變,請重看)。
     哪類圖要做哪些確認見 rules/review/duties.yaml;版本紀錄在 audit/versions.jsonl。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 | 版本 |
|---|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | 1495f21f8393 | pending |  |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | 1495f21f8393 | pending |  |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | a1080cad4be9 | pending |  |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 7813f8a7c922 | pending |  |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 7813f8a7c922 | pending |  |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | e428660cb058 | pending |  |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | e428660cb058 | pending |  |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | decb50720d5f | pending |  |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | decb50720d5f | pending |  |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | 22e8b297a707 | pending |  |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | 22e8b297a707 | pending |  |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 2e64895b6cfa | pending |  |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 2e64895b6cfa | pending |  |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | a2be7db6dcb6 | pending |  |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | a2be7db6dcb6 | pending |  |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | a7caf0eea95b | pending |  |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | a7caf0eea95b | pending |  |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 7b3c60863f55 | pending |  |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 7b3c60863f55 | pending |  |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 2ce5093b1e1b | pending |  |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 2ce5093b1e1b | pending |  |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | aecc2d329bb7 | pending |  |  |  |  |
| C4-L1 | buildable | c4-context | * |  | bf1f4f253c98 | pending |  |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 6a60d39bd50d | pending |  |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 4a1f40b582af | pending |  |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 4a1f40b582af | pending |  |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | e82922918486 | pending |  |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | e82922918486 | pending |  |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 9aaa3d75731c | pending |  |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 9aaa3d75731c | pending |  |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| ERD-001 | buildable | erd | * |  | 236356a94b6b | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | ffade339b47b | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | ffade339b47b | pending |  |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 1a343657112b | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 7fa7c3328c3a | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 7fa7c3328c3a | pending |  |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 79c12db5f422 | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | a9ac5ed36204 | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | a9ac5ed36204 | pending |  |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 4c4c53310dbe | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 3c87663b325d | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 3c87663b325d | pending |  |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 2de4e0325692 | pending |  |  |  |  |
