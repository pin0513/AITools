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
| ACT-001 | intent | flowchart | REQ-001 |  | aac4f81ecb4d | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | aac4f81ecb4d | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 6e5c87ebfb50 | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 6e5c87ebfb50 | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 92e9ead15362 | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 92e9ead15362 | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | 7d0641e56b5d | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | 7d0641e56b5d | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | f58953d225c1 | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | f58953d225c1 | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | 6bb227fc2a98 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | 6bb227fc2a98 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 95bbc593acd3 | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 95bbc593acd3 | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | f93cba84c4c2 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | f93cba84c4c2 | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | ebb65f3ff1ed | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | ebb65f3ff1ed | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | eace5ddbc9c0 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 9ee001cb58d6 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 9ccbaee83cc5 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 904da6e509b4 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 12d159c32801 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 12d159c32801 | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | bc92010d9013 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | bc92010d9013 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 461ce8050044 | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 461ce8050044 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 8e5bb444fda4 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | e27fb0a060dd | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | e27fb0a060dd | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 00c4959ee5f0 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 2a5eb19525f5 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 2a5eb19525f5 | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 3b37af200477 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 2537c26adc08 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 2537c26adc08 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | e3a7743ad8c1 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 0130b78c5b7d | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 0130b78c5b7d | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 31c3fc0df76c | pending |  |  |  |
