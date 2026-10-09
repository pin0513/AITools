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
| SEQ-SA-001 | intent | sequence | REQ-001 |  | 22e8b297a707 | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-001 |  | 22e8b297a707 | pending |  |  |  |
| SEQ-SA-002 | intent | sequence | REQ-002 |  | 2e64895b6cfa | pending |  |  |  |
| SEQ-SA-002 | buildable | sequence | REQ-002 |  | 2e64895b6cfa | pending |  |  |  |
| SEQ-SA-003 | intent | sequence | REQ-003 |  | a2be7db6dcb6 | pending |  |  |  |
| SEQ-SA-003 | buildable | sequence | REQ-003 |  | a2be7db6dcb6 | pending |  |  |  |
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
| C4-L1 | buildable | c4-context | * |  | 6c4edff076ba | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 6a867ea39299 | pending |  |  |  |
| C4-L3 | buildable | flowchart | * |  | fd428edf9c3f | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 94d4ae1b5df2 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 94d4ae1b5df2 | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-002 |  | 8b9dcafa8891 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-002 |  | 8b9dcafa8891 | pending |  |  |  |
| SEQ-003 | buildable | sequence | REQ-003 |  | a90fb7ba0bfc | pending |  |  |  |
| SEQ-003 | testable | sequence | REQ-003 |  | a90fb7ba0bfc | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | e9cfe5654741 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 236356a94b6b | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | bf43c8e6ce99 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | bf43c8e6ce99 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 1c9a0bce8ad0 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 6e9ce4c35be0 | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 6e9ce4c35be0 | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 566daf8499c0 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 0bc9971a0f78 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 0bc9971a0f78 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 4bf078beff90 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | c0cb217460a2 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | c0cb217460a2 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 451a564d401a | pending |  |  |  |
