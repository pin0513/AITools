# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale;「版本」是確認當時的文件版本,之後它依據的需求或 PM 段落變了 → upstream(上游已變,請重看)。
     哪類圖要做哪些確認見 rules/review/duties.yaml;版本紀錄在 audit/versions.jsonl。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 | 版本 |
|---|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | 6a37522020bb | pending |  |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | 6a37522020bb | pending |  |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | 773c1bab0497 | pending |  |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 885ca47ab3aa | pending |  |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 885ca47ab3aa | pending |  |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 97f8ae379542 | pending |  |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 97f8ae379542 | pending |  |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 9b031ae6f96a | pending |  |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 9b031ae6f96a | pending |  |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | aaa8647a19ba | pending |  |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | aaa8647a19ba | pending |  |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 1478bd3d6a95 | pending |  |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | fbb7c28b9b59 | pending |  |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | fbb7c28b9b59 | pending |  |  |  |  |
| STM-SA-001 | intent | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |  |
| STM-SA-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 1e175c27cc7f | pending |  |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 1e175c27cc7f | pending |  |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 720e72455ea1 | pending |  |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 720e72455ea1 | pending |  |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 82277478f6f0 | pending |  |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 82277478f6f0 | pending |  |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |  |
| STM-DOM-001 | testable | state | REQ-001 |  | 409fa2e03d70 | pending |  |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | 1abf07bf0ed1 | pending |  |  |  |  |
| C4-L1 | buildable | c4-context | * |  | e1d9b7c73316 | pending |  |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |  |
| C4-L3 | buildable | flowchart | * |  | b6087400618c | pending |  |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 0750617c12f0 | pending |  |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 0750617c12f0 | pending |  |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 55201349a7a6 | pending |  |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 55201349a7a6 | pending |  |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 268fdba731b4 | pending |  |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 268fdba731b4 | pending |  |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| ERD-001 | buildable | erd | * |  | d8dd9e92b51d | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | eb8480c115af | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | eb8480c115af | pending |  |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 85d1f14ed713 | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 782238614e07 | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 782238614e07 | pending |  |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 44b2d7d16e8d | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 62d56a213ae1 | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 62d56a213ae1 | pending |  |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | a4b1655dd953 | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | db76567a4663 | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | db76567a4663 | pending |  |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 8df995241953 | pending |  |  |  |  |
