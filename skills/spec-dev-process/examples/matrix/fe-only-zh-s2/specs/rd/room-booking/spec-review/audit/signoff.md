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
| UCD-001 | intent | flowchart | REQ-001, REQ-002, REQ-003 |  | b69cc0249565 | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-001 |  | 596645eaeb9a | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-001 |  | 596645eaeb9a | pending |  |  |  |
| ACT-002 | intent | flowchart | REQ-002 |  | 24b5978a359e | pending |  |  |  |
| ACT-002 | testable | flowchart | REQ-002 |  | 24b5978a359e | pending |  |  |  |
| ACT-003 | intent | flowchart | REQ-003 |  | 5028da3f5e8f | pending |  |  |  |
| ACT-003 | testable | flowchart | REQ-003 |  | 5028da3f5e8f | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-001 |  | 62e0a35477f9 | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | 62e0a35477f9 | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | c37bbc300476 | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | c37bbc300476 | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | 892825da7c34 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | 892825da7c34 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| UC-001 | intent | flowchart | REQ-001 |  | 2bd3ef3e281e | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 2bd3ef3e281e | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | fc219fe46768 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | fc219fe46768 | pending |  |  |  |
| UC-003 | intent | flowchart | REQ-003 |  | aec1abb285c7 | pending |  |  |  |
| UC-003 | testable | flowchart | REQ-003 |  | aec1abb285c7 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001, REQ-002 |  | 75624ae41d98 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | aecc2d329bb7 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | f6f148d1518c | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | bc819a5404d4 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | 4dbdc722a183 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | cac13ab4964b | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | cac13ab4964b | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | e3148f787e59 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | e3148f787e59 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | 76b475ad7136 | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | 76b475ad7136 | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | dbd7b7bcc548 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | dbd7b7bcc548 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 78eac659acd0 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | fd267db8ae43 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | fd267db8ae43 | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 437da4517ed2 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | f49488bccaef | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | f49488bccaef | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 5a4fc816cb53 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | 755b9c6e52d7 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | 755b9c6e52d7 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 6c204b6586fd | pending |  |  |  |
