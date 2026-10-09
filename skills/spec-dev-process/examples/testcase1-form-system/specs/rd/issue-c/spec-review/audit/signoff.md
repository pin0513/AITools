# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale。哪類圖要做哪些確認見 rules/review/duties.yaml。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | intent | class | REQ-001 |  | b88bf3e6a275 | pending |  |  |  |
| CLS-SA-001 | buildable | class | REQ-001 |  | b88bf3e6a275 | pending |  |  |  |
| UCD-001 | intent | flowchart | REQ-001 |  | 8a816cccfa0a | pending |  |  |  |
| ACT-001 | intent | flowchart | REQ-002 |  | 123032485715 | pending |  |  |  |
| ACT-001 | testable | flowchart | REQ-002 |  | 123032485715 | pending |  |  |  |
| SEQ-SA-001 | intent | sequence | REQ-002, REQ-003 |  | dfe6c54871d1 | pending |  |  |  |
| SEQ-SA-001 | buildable | sequence | REQ-002, REQ-003 |  | dfe6c54871d1 | pending |  |  |  |
| STM-SA-001 | intent | state | REQ-001 |  | 43330ee1cdfe | pending |  |  |  |
| STM-SA-001 | testable | state | REQ-001 |  | 43330ee1cdfe | pending |  |  |  |
| UC-002 | intent | flowchart | REQ-002 |  | ad646d9b1873 | pending |  |  |  |
| UC-002 | testable | flowchart | REQ-002 |  | ad646d9b1873 | pending |  |  |  |
| STM-DOM-001 | buildable | state | REQ-001 |  | 3bcdf090924f | pending |  |  |  |
| STM-DOM-001 | testable | state | REQ-001 |  | 3bcdf090924f | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-001 |  | 9c4202c11cf5 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-001 |  | 9c4202c11cf5 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-002 |  | 7a059064d857 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 17374d96d526 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 71b0d7b1cd43 | pending |  |  |  |
| C4-L3 | buildable | c4-component | * |  | bc85db5de39e | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-002 |  | 5ac425162801 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-002 |  | 5ac425162801 | pending |  |  |  |
| SEQ-002 | buildable | sequence | REQ-004 |  | 514f15191856 | pending |  |  |  |
| SEQ-002 | testable | sequence | REQ-004 |  | 514f15191856 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | 7e99e251500e | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | 44fb879c3698 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | 44fb879c3698 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 8f963037c01b | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 251e5468132d | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 251e5468132d | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | a8ea032618fd | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 2b44673f3885 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 2b44673f3885 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 5359a2c2033e | pending |  |  |  |
| AUTO-TRACE-REQ-004 | intent | flowchart | REQ-004 |  | 70f91c5f61cb | pending |  |  |  |
| AUTO-TRACE-REQ-004 | testable | flowchart | REQ-004 |  | 70f91c5f61cb | pending |  |  |  |
| AUTO-SEQ-REQ-004 | buildable | sequence | REQ-004 |  | 435aa27bc28b | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | a3397a2cbad6 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | a3397a2cbad6 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | 0f2f282d4ba8 | pending |  |  |  |
| AUTO-TRACE-NFR-002 | intent | flowchart | NFR-002 |  | d1f29a931bb0 | pending |  |  |  |
| AUTO-TRACE-NFR-002 | testable | flowchart | NFR-002 |  | d1f29a931bb0 | pending |  |  |  |
| AUTO-SEQ-NFR-002 | buildable | sequence | NFR-002 |  | 04ae73fe4a2e | pending |  |  |  |
| AUTO-TRACE-NFR-003 | intent | flowchart | NFR-003 |  | 0ec92cec3432 | pending |  |  |  |
| AUTO-TRACE-NFR-003 | testable | flowchart | NFR-003 |  | 0ec92cec3432 | pending |  |  |  |
| AUTO-SEQ-NFR-003 | buildable | sequence | NFR-003 |  | 9d21d387657b | pending |  |  |  |
