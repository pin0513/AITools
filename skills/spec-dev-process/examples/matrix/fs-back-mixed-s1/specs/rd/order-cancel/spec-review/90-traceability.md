# 訂單取消與退款 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 9 · 測試元件 10 · 技術邊界 PASS 26/26 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-003 | CMP-004 | CMP-007 | CMP-008 | TST-004, TST-007 | TST-003, TST-008 | TST-002 | TST-001 | ✓ |
| REQ-002 | CMP-003 | CMP-005 | CMP-007 | CMP-008, CMP-009 | TST-005, TST-007 | TST-003, TST-008 | TST-002, TST-009 | TST-001 | ✓ |
| REQ-003 | CMP-003 | CMP-006 | CMP-007 | CMP-008 | TST-006, TST-007 | TST-003, TST-008 | TST-002 | TST-001 | ✓ |
| NFR-001 | CMP-003 | · | · | · | · | · | · | TST-010 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(顯示並觸發cancel), CMP-002(呼叫cancel API), CMP-003(接收cancel請求), CMP-004(編排cancel), CMP-007(cancel的業務規則與不變量), CMP-008(持久化cancel結果) | TST-001, TST-002, TST-003, TST-004, TST-007, TST-008 |
| AC-001-2 | REQ-001 | CMP-001(顯示並觸發cancel), CMP-002(呼叫cancel API), CMP-003(接收cancel請求), CMP-004(編排cancel), CMP-007(cancel的業務規則與不變量), CMP-008(持久化cancel結果) | TST-001, TST-002, TST-003, TST-004, TST-007, TST-008 |
| AC-002-1 | REQ-002 | CMP-001(顯示並觸發refund), CMP-002(呼叫refund API), CMP-003(接收refund請求), CMP-005(編排refund), CMP-007(refund的業務規則與不變量), CMP-008(持久化refund結果), CMP-009(為refund呼叫外部系統) | TST-001, TST-002, TST-003, TST-005, TST-007, TST-008, TST-009 |
| AC-002-2 | REQ-002 | CMP-001(顯示並觸發refund), CMP-002(呼叫refund API), CMP-003(接收refund請求), CMP-005(編排refund), CMP-007(refund的業務規則與不變量), CMP-008(持久化refund結果), CMP-009(為refund呼叫外部系統) | TST-001, TST-002, TST-003, TST-005, TST-007, TST-008, TST-009 |
| AC-003-1 | REQ-003 | CMP-001(顯示並觸發view), CMP-002(呼叫view API), CMP-003(接收view請求), CMP-006(編排view), CMP-007(view的業務規則與不變量), CMP-008(持久化view結果) | TST-001, TST-002, TST-003, TST-006, TST-007, TST-008 |
| AC-N01-1 | NFR-001 | CMP-003(NFR P95 < 5 min) | TST-010 |

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
| INFO | G-GL-consistency | 「訂單」→ Order 與 prev 一致 |
| INFO | G-SV-evidence | 訂單 (Order) → src/api/Orders.Domain/Order.cs:5 已放行·弱證據(符號 Order;只比對到名字) |
| INFO | G-SV-evidence | Shipped rule → src/api/Orders.Domain/Order.cs:3 "Shipped" 已放行·強證據(字面 "Shipped") |
| INFO | G-SV-evidence | GetOrder → src/api/Orders.Application/GetOrderQueryHandler.cs:8 已放行·弱證據(對照表 Application 層 GetOrderQueryHandler;只比對到名字) |
| INFO | G-SV-evidence | SqlOrderRepository → src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 已放行·弱證據(符號 SqlOrderRepository;只比對到名字) |
| INFO | G-SV-evidence | PaymentGatewayClient → src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 已放行·弱證據(符號 PaymentGatewayClient;只比對到名字) |
| INFO | G-SV-evidence | OrdersController → src/api/Orders.Api/Controllers/OrdersController.cs:8 已放行·弱證據(符號 OrdersController;只比對到名字) |
| INFO | G-SV-evidence | OrderDetailPage → src/web/src/pages/OrderDetailPage.tsx:4 "getOrder(id)" 已放行·強證據(字面 "getOrder(id)") |
| INFO | G-SV-evidence | Order type → src/web/src/types/Order.ts:4 已放行·弱證據(符號 Order;只比對到名字) |
