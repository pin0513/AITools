# 圖與表審計 — 人工確認

<!-- SSOT:人工決定寫在這裡,一張圖 × 一個確認事項一列(以事情區分,不以人區分;同一人可做多項)。
     決定 = approved(通過)/ rejected(退回,要備註)/ n/a(不需要,要寫理由)/ pending。通過時把「目前 hash」填進「簽核 hash」;
     之後圖一改,目前 hash 變了,該項自動變成 stale。哪類圖要做哪些確認見 rules/review/duties.yaml。
     工具每次執行只更新「目前 hash」與新增列,不會改你的決定。也可用看板(spec-dev.py serve)或 spec-dev.py signoff。 -->

## 簽核

| 圖 | 確認事項 | 類型 | 目標 | 簽核 hash | 目前 hash | 決定 | 審核者 | 日期 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| UC-001 | intent | flowchart | REQ-001 |  | 750a3edf9baa | pending |  |  |  |
| UC-001 | testable | flowchart | REQ-001 |  | 750a3edf9baa | pending |  |  |  |
| STM-UI-001 | intent | state | REQ-002 |  | 00515f698421 | pending |  |  |  |
| STM-UI-001 | testable | state | REQ-002 |  | 00515f698421 | pending |  |  |  |
| CLS-001 | buildable | class | REQ-001 |  | 3a4506cbc347 | pending |  |  |  |
| C4-L1 | buildable | c4-context | * |  | 159e1d9f18b4 | pending |  |  |  |
| C4-L2 | buildable | c4-container | * |  | 549122d75dd3 | pending |  |  |  |
| C4-L3 | buildable | c4-component | * |  | 289da345d333 | pending |  |  |  |
| SEQ-001 | buildable | sequence | REQ-001 |  | 296b87ac9b45 | pending |  |  |  |
| SEQ-001 | testable | sequence | REQ-001 |  | 296b87ac9b45 | pending |  |  |  |
| ERD-001 | buildable | erd | * |  | df1563ceff41 | pending |  |  |  |
| AUTO-TRACE-REQ-001 | intent | flowchart | REQ-001 |  | 41814e38c1dc | pending |  |  |  |
| AUTO-TRACE-REQ-001 | testable | flowchart | REQ-001 |  | 41814e38c1dc | pending |  |  |  |
| AUTO-SEQ-REQ-001 | buildable | sequence | REQ-001 |  | 8ce043f34cfe | pending |  |  |  |
| AUTO-TRACE-REQ-002 | intent | flowchart | REQ-002 |  | 9febc508bf7f | pending |  |  |  |
| AUTO-TRACE-REQ-002 | testable | flowchart | REQ-002 |  | 9febc508bf7f | pending |  |  |  |
| AUTO-SEQ-REQ-002 | buildable | sequence | REQ-002 |  | 4cd49a8bb1a2 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | intent | flowchart | REQ-003 |  | 27d57b142050 | pending |  |  |  |
| AUTO-TRACE-REQ-003 | testable | flowchart | REQ-003 |  | 27d57b142050 | pending |  |  |  |
| AUTO-SEQ-REQ-003 | buildable | sequence | REQ-003 |  | 9673a14261b5 | pending |  |  |  |
| AUTO-TRACE-NFR-001 | intent | flowchart | NFR-001 |  | ed7206aee43f | pending |  |  |  |
| AUTO-TRACE-NFR-001 | testable | flowchart | NFR-001 |  | ed7206aee43f | pending |  |  |  |
| AUTO-SEQ-NFR-001 | buildable | sequence | NFR-001 |  | f2dd3588d20f | pending |  |  |  |
| AUTO-TRACE-NFR-002 | intent | flowchart | NFR-002 |  | 6e4c1d61ece0 | pending |  |  |  |
| AUTO-TRACE-NFR-002 | testable | flowchart | NFR-002 |  | 6e4c1d61ece0 | pending |  |  |  |
| AUTO-SEQ-NFR-002 | buildable | sequence | NFR-002 |  | 8e4e7094915c | pending |  |  |  |
