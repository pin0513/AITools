# 訂單取消與退款 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 7 · 測試元件 8 · 技術邊界 PASS 24/24 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-001 | CMP-002 | CMP-005 | CMP-006 | TST-002, TST-005 | TST-001, TST-006 | · | · | ✓ |
| REQ-002 | CMP-001 | CMP-003 | CMP-005 | CMP-006, CMP-007 | TST-003, TST-005 | TST-001, TST-006 | TST-007 | · | ✓ |
| REQ-003 | CMP-001 | CMP-004 | CMP-005 | CMP-006 | TST-004, TST-005 | TST-001, TST-006 | · | · | ✓ |
| NFR-001 | CMP-001 | · | · | · | · | · | · | TST-008 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(接收cancel請求), CMP-002(編排cancel), CMP-005(cancel的業務規則與不變量), CMP-006(持久化cancel結果) | TST-001, TST-002, TST-005, TST-006 |
| AC-001-2 | REQ-001 | CMP-001(接收cancel請求), CMP-002(編排cancel), CMP-005(cancel的業務規則與不變量), CMP-006(持久化cancel結果) | TST-001, TST-002, TST-005, TST-006 |
| AC-002-1 | REQ-002 | CMP-001(接收refund請求), CMP-003(編排refund), CMP-005(refund的業務規則與不變量), CMP-006(持久化refund結果), CMP-007(為refund呼叫外部系統) | TST-001, TST-003, TST-005, TST-006, TST-007 |
| AC-002-2 | REQ-002 | CMP-001(接收refund請求), CMP-003(編排refund), CMP-005(refund的業務規則與不變量), CMP-006(持久化refund結果), CMP-007(為refund呼叫外部系統) | TST-001, TST-003, TST-005, TST-006, TST-007 |
| AC-003-1 | REQ-003 | CMP-001(接收view請求), CMP-004(編排view), CMP-005(view的業務規則與不變量), CMP-006(持久化view結果) | TST-001, TST-004, TST-005, TST-006 |
| AC-N01-1 | NFR-001 | CMP-001(NFR P95 < 5 min) | TST-008 |

## Gate 問題

| 等級 | 規則 | 訊息 |
|---|---|---|
| INFO | G-SA-steps | SA0 sa/00-lexicon.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA1 sa/01-break-words.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA2 sa/02-entities-relations.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA3 sa/03-roles.md 齊全(0 張圖) |
| INFO | G-SA-steps | SA4 sa/04-usecase.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA5 sa/05-activity.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA6 sa/06-sequence.md 齊全(1 張圖) |
| INFO | G-SA-steps | SA7 sa/07-state.md 齊全(1 張圖) |
| INFO | G-GL-consistency | 「訂單」→ Order 與 prev 一致 |
| INFO | G-SV-evidence | 訂單 (Order) → src/api/Orders.Domain/Order.cs:5 已驗證(符號 Order) |
| INFO | G-SV-evidence | Shipped rule → src/api/Orders.Domain/Order.cs:3 "Shipped" 已驗證(字面 "Shipped") |
| INFO | G-SV-evidence | GetOrder → src/api/Orders.Application/GetOrderQueryHandler.cs:8 已驗證(對照表 Application 層 GetOrderQueryHandler) |
| INFO | G-SV-evidence | SqlOrderRepository → src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 已驗證(符號 SqlOrderRepository) |
| INFO | G-SV-evidence | PaymentGatewayClient → src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 已驗證(符號 PaymentGatewayClient) |
| INFO | G-SV-evidence | OrdersController → src/api/Orders.Api/Controllers/OrdersController.cs:8 已驗證(符號 OrdersController) |
