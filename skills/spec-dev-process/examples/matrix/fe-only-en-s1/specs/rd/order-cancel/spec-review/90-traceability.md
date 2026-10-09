# Order cancellation and refund — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 5 · 測試元件 6 · 技術邊界 PASS 18/18 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | · | · | · | · | TST-002, TST-004 | · | TST-005 | TST-001 | ✓ |
| REQ-002 | · | · | · | · | TST-004 | · | TST-005 | TST-001 | ✓ |
| REQ-003 | · | · | · | · | TST-003, TST-004 | · | TST-005 | TST-001 | ✓ |
| NFR-001 | · | · | · | · | · | · | · | TST-006 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(render and trigger cancel), CMP-002(UI guard for cancel), CMP-004(client state transition for cancel), CMP-005(call the API for cancel) | TST-001, TST-002, TST-004, TST-005 |
| AC-001-2 | REQ-001 | CMP-001(render and trigger cancel), CMP-002(UI guard for cancel), CMP-004(client state transition for cancel), CMP-005(call the API for cancel) | TST-001, TST-002, TST-004, TST-005 |
| AC-002-1 | REQ-002 | CMP-001(render and trigger refund), CMP-004(client state transition for refund), CMP-005(call the API for refund) | TST-001, TST-004, TST-005 |
| AC-002-2 | REQ-002 | CMP-001(render and trigger refund), CMP-004(client state transition for refund), CMP-005(call the API for refund) | TST-001, TST-004, TST-005 |
| AC-003-1 | REQ-003 | CMP-001(render and trigger view), CMP-003(UI guard for view), CMP-004(client state transition for view), CMP-005(call the API for view) | TST-001, TST-003, TST-004, TST-005 |
| AC-N01-1 | NFR-001 | CMP-005(NFR P95 < 5 min) | TST-006 |

## Gate 問題

| 等級 | 規則 | 訊息 |
|---|---|---|
| INFO | G-SA-steps | SA0 sa/00-lexicon.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA1 sa/01-break-words.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA2 sa/02-entities-relations.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA3 sa/03-roles.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA4 sa/04-usecase.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA5 sa/05-activity.md 齊全(3 張圖) |
| INFO | G-SA-steps | SA6 sa/06-sequence.md 齊全(3 張圖) |
| INFO | G-SA-steps | SA7 sa/07-state.md 齊全(1 張圖) |
| INFO | G-GL-consistency | 「order」→ Order 與 prev 一致 |
| INFO | G-SV-evidence | Order → src/web/src/types/Order.ts:4 已驗證(符號 Order) |
| INFO | G-SV-evidence | Shipped rule → src/web/src/types/Order.ts:2 "Shipped" 已驗證(字面 "Shipped") |
| INFO | G-SV-evidence | GetOrder → src/web/src/api/ordersApi.ts:3 已驗證(符號 GetOrder) |
| INFO | G-SV-evidence | OrderDetailPage → src/web/src/pages/OrderDetailPage.tsx:3 已驗證(符號 OrderDetailPage) |
