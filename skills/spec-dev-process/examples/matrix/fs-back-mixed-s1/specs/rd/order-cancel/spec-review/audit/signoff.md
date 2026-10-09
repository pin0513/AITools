# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale;「版本」是確認當時的文件版本,之後它依據的需求或 PM 段落變了 → upstream(上游已變,請重看)。
     哪類圖要做哪些確認見 rules/review/duties.yaml;版本紀錄在 audit/versions.jsonl。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 | 版本 |
|---|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | f51c89e8300f | pending |  |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | f51c89e8300f | pending |  |  |  |  |
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | ab7ee70e0c36 | pending |  |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | aac4f81ecb4d | pending |  |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | aac4f81ecb4d | pending |  |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 6e5c87ebfb50 | pending |  |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 6e5c87ebfb50 | pending |  |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 92e9ead15362 | pending |  |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 92e9ead15362 | pending |  |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | b6f83b536f8f | pending |  |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 918b1530e97e | pending |  |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | bdb0d943d470 | pending |  |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 95bbc593acd3 | pending |  |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 95bbc593acd3 | pending |  |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | f93cba84c4c2 | pending |  |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | f93cba84c4c2 | pending |  |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | ebb65f3ff1ed | pending |  |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | ebb65f3ff1ed | pending |  |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 87e0cbe57561 | pending |  |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | eace5ddbc9c0 | pending |  |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 9ee001cb58d6 | pending |  |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 6d07d4fd1dbb | pending |  |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | e732c43edd8a | pending |  |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | e732c43edd8a | pending |  |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | c977f8733790 | pending |  |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | c977f8733790 | pending |  |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | fae70e575822 | pending |  |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | fae70e575822 | pending |  |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |  |
| ERD-001 | buildable | erd | * |  | 8e5bb444fda4 | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | e61cdc531348 | pending |  |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | e61cdc531348 | pending |  |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 784517b83ba2 | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | c3d4d13bfb76 | pending |  |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | c3d4d13bfb76 | pending |  |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | ddd2077a4889 | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | f26fc6b65938 | pending |  |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | f26fc6b65938 | pending |  |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | acbbd55ed0af | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 717b457e1609 | pending |  |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 717b457e1609 | pending |  |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 337b65bcbc4f | pending |  |  |  |  |
