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
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | 773c1bab0497 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 23f8f89437b0 | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 23f8f89437b0 | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 0484d57f037f | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 0484d57f037f | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 0423ad066c8c | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 0423ad066c8c | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | aaa8647a19ba | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | aaa8647a19ba | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | fbb7c28b9b59 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | fbb7c28b9b59 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | d2107b7e846c | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | d2107b7e846c | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 5acf7541c540 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 5acf7541c540 | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 9250776a3c42 | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 9250776a3c42 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | 1abf07bf0ed1 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | e5136e2e15f2 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | cb6102f1b331 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 9b295b79c57b | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 9b295b79c57b | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | f56d730df64b | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | f56d730df64b | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 4d2705338217 | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 4d2705338217 | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | d8dd9e92b51d | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | ca9aef7fe3de | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | ca9aef7fe3de | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 46fb3336a617 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | d9de4c9f6d07 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | d9de4c9f6d07 | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 5e79b0882f73 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 986265a47f2a | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 986265a47f2a | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 99fb9953907a | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | e021b410759c | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | e021b410759c | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 8df995241953 | pending |  |  |  |
