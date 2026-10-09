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
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | f02360c87a98 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 48d8f995bcd8 | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 48d8f995bcd8 | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | d74420776754 | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | d74420776754 | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | d96c1207c5c4 | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | d96c1207c5c4 | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 76afe9ecab02 | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 76afe9ecab02 | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | 6a01e81dc6dd | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | 6a01e81dc6dd | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | 04233ced46c2 | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | 04233ced46c2 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | eace5ddbc9c0 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | b1c57a941d5f | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 6fec15575f67 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | b4bd238c823a | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | b4bd238c823a | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 167212a044fb | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 167212a044fb | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | c68292bd1cfe | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | c68292bd1cfe | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 8e5bb444fda4 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | 135364e9de3c | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | 135364e9de3c | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | d9d3e0cb66f4 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 289cb69f3c7c | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 289cb69f3c7c | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 2c017ad01f3e | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 2e27a19f5591 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 2e27a19f5591 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 35d403879b65 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 49df9ca9fe55 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 49df9ca9fe55 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | dcc709138db3 | pending |  |  |  |
