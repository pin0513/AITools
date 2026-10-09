# Order cancellation and refund — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 11 · 測試元件 12 · 技術邊界 PASS 28/28 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-006 | CMP-007 | · | CMP-010 | TST-002, TST-004, TST-007 | TST-006, TST-010 | TST-005 | TST-001 | ✓ |
| REQ-002 | CMP-006 | CMP-008 | · | CMP-010, CMP-011 | TST-004, TST-008 | TST-006, TST-010 | TST-005, TST-011 | TST-001 | ✓ |
| REQ-003 | CMP-006 | CMP-009 | · | CMP-010 | TST-003, TST-004, TST-009 | TST-006, TST-010 | TST-005 | TST-001 | ✓ |
| NFR-001 | CMP-006 | · | · | · | · | · | · | TST-012 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(render and trigger cancel), CMP-002(UI guard for cancel), CMP-004(client state transition for cancel), CMP-005(call the API for cancel), CMP-006(receive the cancel request), CMP-007(orchestrate cancel), CMP-010(persist the cancel result) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010 |
| AC-001-2 | REQ-001 | CMP-001(render and trigger cancel), CMP-002(UI guard for cancel), CMP-004(client state transition for cancel), CMP-005(call the API for cancel), CMP-006(receive the cancel request), CMP-007(orchestrate cancel), CMP-010(persist the cancel result) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010 |
| AC-002-1 | REQ-002 | CMP-001(render and trigger refund), CMP-004(client state transition for refund), CMP-005(call the API for refund), CMP-006(receive the refund request), CMP-008(orchestrate refund), CMP-010(persist the refund result), CMP-011(call the external system for refund) | TST-001, TST-004, TST-005, TST-006, TST-008, TST-010, TST-011 |
| AC-002-2 | REQ-002 | CMP-001(render and trigger refund), CMP-004(client state transition for refund), CMP-005(call the API for refund), CMP-006(receive the refund request), CMP-008(orchestrate refund), CMP-010(persist the refund result), CMP-011(call the external system for refund) | TST-001, TST-004, TST-005, TST-006, TST-008, TST-010, TST-011 |
| AC-003-1 | REQ-003 | CMP-001(render and trigger view), CMP-003(UI guard for view), CMP-004(client state transition for view), CMP-005(call the API for view), CMP-006(receive the view request), CMP-009(orchestrate view), CMP-010(persist the view result) | TST-001, TST-003, TST-004, TST-005, TST-006, TST-009, TST-010 |
| AC-N01-1 | NFR-001 | CMP-006(NFR P95 < 5 min) | TST-012 |

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
| INFO | G-SV-evidence | Order → src/api/Orders.Domain/Order.cs:5 已驗證(符號 Order) |
| INFO | G-SV-evidence | Shipped rule → src/api/Orders.Domain/Order.cs:3 "Shipped" 已驗證(字面 "Shipped") |
| INFO | G-SV-evidence | GetOrder → src/api/Orders.Application/GetOrderQueryHandler.cs:8 已驗證(對照表 Application 層 GetOrderQueryHandler) |
| INFO | G-SV-evidence | SqlOrderRepository → src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 已驗證(符號 SqlOrderRepository) |
| INFO | G-SV-evidence | PaymentGatewayClient → src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 已驗證(符號 PaymentGatewayClient) |
| INFO | G-SV-evidence | OrdersController → src/api/Orders.Api/Controllers/OrdersController.cs:8 已驗證(符號 OrdersController) |
| INFO | G-SV-evidence | OrderDetailPage → src/web/src/pages/OrderDetailPage.tsx:3 已驗證(符號 OrderDetailPage) |
| INFO | G-SV-evidence | Order type → src/web/src/types/Order.ts:4 已驗證(符號 Order) |
