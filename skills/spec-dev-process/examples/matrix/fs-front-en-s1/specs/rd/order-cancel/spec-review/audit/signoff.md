# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale。哪類圖要做哪些確認見 rules/review/duties.yaml。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | f51c89e8300f | pending |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | f51c89e8300f | pending |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | ab7ee70e0c36 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 6e08d9b1934f | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 6e08d9b1934f | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 8d58713e05a9 | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 8d58713e05a9 | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | d8e6cea53fb9 | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | d8e6cea53fb9 | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 7717a06fcd85 | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 7717a06fcd85 | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | cbbf439dca0d | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | cbbf439dca0d | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 047b4bfd1157 | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 047b4bfd1157 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | eace5ddbc9c0 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 814ce9e1fe6d | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | d95806d2fbfd | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 42078f1b157f | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 42078f1b157f | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 6836e170d116 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 6836e170d116 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | caac2c24ecd8 | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | caac2c24ecd8 | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 8e5bb444fda4 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | 45d7c9fda9fc | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | 45d7c9fda9fc | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | fcca112c6a3b | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 1b46c149d32f | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 1b46c149d32f | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 5328bf1ce0c6 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 5d7af30e5864 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 5d7af30e5864 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 6449cfe01109 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 6de329f35a1b | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 6de329f35a1b | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | dcc709138db3 | pending |  |  |  |
