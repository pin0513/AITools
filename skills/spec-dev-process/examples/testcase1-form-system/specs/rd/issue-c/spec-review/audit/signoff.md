# 圖與表審計 — 人工簽核

<!-- SSOT:人工決定寫在這裡。決定 = approved / rejected / pending。核准時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,狀態自動變成 stale。工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用 spec-dev.py signoff。 -->

## 簽核

| 圖 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|
| CLS-SA-001 | class | REQ-001 |  | b88bf3e6a275 | pending |  |  |  |
| UCD-001 | flowchart | REQ-001 |  | 8a816cccfa0a | pending |  |  |  |
| ACT-001 | flowchart | REQ-002 |  | 123032485715 | pending |  |  |  |
| SEQ-SA-001 | sequence | REQ-002, REQ-003 |  | dfe6c54871d1 | pending |  |  |  |
| STM-SA-001 | state | REQ-001 |  | 43330ee1cdfe | pending |  |  |  |
| UC-002 | flowchart | REQ-002 |  | ad646d9b1873 | pending |  |  |  |
| STM-DOM-001 | state | REQ-001 |  | 3bcdf090924f | pending |  |  |  |
| STM-UI-001 | state | REQ-001 |  | 9c4202c11cf5 | pending |  |  |  |
| CLS-001 | class | REQ-002 |  | 7a059064d857 | pending |  |  |  |
| C4-L1 | c4-context | * |  | 17374d96d526 | pending |  |  |  |
| C4-L2 | c4-container | * |  | 71b0d7b1cd43 | pending |  |  |  |
| C4-L3 | c4-component | * |  | bc85db5de39e | pending |  |  |  |
| SEQ-001 | sequence | REQ-002 |  | 5ac425162801 | pending |  |  |  |
| SEQ-002 | sequence | REQ-004 |  | 514f15191856 | pending |  |  |  |
| ERD-001 | erd | * |  | 7e99e251500e | pending |  |  |  |
| AUTO-TRACE-REQ-001 | flowchart | REQ-001 |  | 44fb879c3698 | pending |  |  |  |
| AUTO-SEQ-REQ-001 | sequence | REQ-001 |  | 8f963037c01b | pending |  |  |  |
| AUTO-TRACE-REQ-002 | flowchart | REQ-002 |  | 251e5468132d | pending |  |  |  |
| AUTO-SEQ-REQ-002 | sequence | REQ-002 |  | a8ea032618fd | pending |  |  |  |
| AUTO-TRACE-REQ-003 | flowchart | REQ-003 |  | 2b44673f3885 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | sequence | REQ-003 |  | 5359a2c2033e | pending |  |  |  |
| AUTO-TRACE-REQ-004 | flowchart | REQ-004 |  | 70f91c5f61cb | pending |  |  |  |
| AUTO-SEQ-REQ-004 | sequence | REQ-004 |  | 435aa27bc28b | pending |  |  |  |
| AUTO-TRACE-NFR-001 | flowchart | NFR-001 |  | a3397a2cbad6 | pending |  |  |  |
| AUTO-SEQ-NFR-001 | sequence | NFR-001 |  | 0f2f282d4ba8 | pending |  |  |  |
| AUTO-TRACE-NFR-002 | flowchart | NFR-002 |  | d1f29a931bb0 | pending |  |  |  |
| AUTO-SEQ-NFR-002 | sequence | NFR-002 |  | 04ae73fe4a2e | pending |  |  |  |
| AUTO-TRACE-NFR-003 | flowchart | NFR-003 |  | 0ec92cec3432 | pending |  |  |  |
| AUTO-SEQ-NFR-003 | sequence | NFR-003 |  | 9d21d387657b | pending |  |  |  |
