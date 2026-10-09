# 訂單取消與退款 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 12 · 測試元件 13 · 技術邊界 PASS 31/31 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-006 | CMP-007 | CMP-010 | CMP-011 | TST-002, TST-004, TST-007, TST-010 | TST-006, TST-011 | TST-005 | TST-001 | ✓ |
| REQ-002 | CMP-006 | CMP-008 | CMP-010 | CMP-011, CMP-012 | TST-004, TST-008, TST-010 | TST-006, TST-011 | TST-005, TST-012 | TST-001 | ✓ |
| REQ-003 | CMP-006 | CMP-009 | CMP-010 | CMP-011 | TST-003, TST-004, TST-009, TST-010 | TST-006, TST-011 | TST-005 | TST-001 | ✓ |
| NFR-001 | CMP-006 | · | · | · | · | · | · | TST-013 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(顯示並觸發取消), CMP-002(取消的 UI 守衛), CMP-004(取消的前端狀態轉移), CMP-005(呼叫取消 API), CMP-006(接收取消請求), CMP-007(編排取消), CMP-010(取消的業務規則與不變量), CMP-011(持久化取消結果) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011 |
| AC-001-2 | REQ-001 | CMP-001(顯示並觸發取消), CMP-002(取消的 UI 守衛), CMP-004(取消的前端狀態轉移), CMP-005(呼叫取消 API), CMP-006(接收取消請求), CMP-007(編排取消), CMP-010(取消的業務規則與不變量), CMP-011(持久化取消結果) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011 |
| AC-002-1 | REQ-002 | CMP-001(顯示並觸發退款), CMP-004(退款的前端狀態轉移), CMP-005(呼叫退款 API), CMP-006(接收退款請求), CMP-008(編排退款), CMP-010(退款的業務規則與不變量), CMP-011(持久化退款結果), CMP-012(為退款呼叫外部系統) | TST-001, TST-004, TST-005, TST-006, TST-008, TST-010, TST-011, TST-012 |
| AC-002-2 | REQ-002 | CMP-001(顯示並觸發退款), CMP-004(退款的前端狀態轉移), CMP-005(呼叫退款 API), CMP-006(接收退款請求), CMP-008(編排退款), CMP-010(退款的業務規則與不變量), CMP-011(持久化退款結果), CMP-012(為退款呼叫外部系統) | TST-001, TST-004, TST-005, TST-006, TST-008, TST-010, TST-011, TST-012 |
| AC-003-1 | REQ-003 | CMP-001(顯示並觸發查看), CMP-003(查看的 UI 守衛), CMP-004(查看的前端狀態轉移), CMP-005(呼叫查看 API), CMP-006(接收查看請求), CMP-009(編排查看), CMP-010(查看的業務規則與不變量), CMP-011(持久化查看結果) | TST-001, TST-003, TST-004, TST-005, TST-006, TST-009, TST-010, TST-011 |
| AC-N01-1 | NFR-001 | CMP-006(NFR P95 < 5 min) | TST-013 |

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
| INFO | G-SV-evidence | 訂單 → src/api/Orders.Domain/Order.cs:5 已驗證(glossary 解析 Order) |
| INFO | G-SV-evidence | Shipped rule → src/api/Orders.Domain/Order.cs:3 "Shipped" 已驗證(字面 "Shipped") |
| INFO | G-SV-evidence | GetOrder → src/api/Orders.Application/GetOrderQueryHandler.cs:8 已驗證(對照表 Application 層 GetOrderQueryHandler) |
| INFO | G-SV-evidence | SqlOrderRepository → src/api/Orders.Infrastructure/SqlOrderRepository.cs:5 已驗證(符號 SqlOrderRepository) |
| INFO | G-SV-evidence | PaymentGatewayClient → src/api/Orders.Infrastructure/PaymentGatewayClient.cs:5 已驗證(符號 PaymentGatewayClient) |
| INFO | G-SV-evidence | OrdersController → src/api/Orders.Api/Controllers/OrdersController.cs:8 已驗證(符號 OrdersController) |
| INFO | G-SV-evidence | OrderDetailPage → src/web/src/pages/OrderDetailPage.tsx:3 已驗證(符號 OrderDetailPage) |
| INFO | G-SV-evidence | Order type → src/web/src/types/Order.ts:4 已驗證(符號 Order) |
