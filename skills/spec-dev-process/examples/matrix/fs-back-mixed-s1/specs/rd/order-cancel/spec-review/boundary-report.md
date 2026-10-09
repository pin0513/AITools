# 訂單取消與退款 — 技術邊界核對報告

<!-- 由 spec-dev.py check 產生,不要手改 -->

| 規則 | 目標 | 狀態 | 證據 | 處置 |
|---|---|---|---|---|
| B1 | NFR-001 | PASS | link → CMP-003 |  |
| B1 | REQ-001 | PASS | link → CMP-001, CMP-002, CMP-003, CMP-004, CMP-007, CMP-008 |  |
| B1 | REQ-002 | PASS | link → CMP-001, CMP-002, CMP-003, CMP-005, CMP-007, CMP-008, CMP-009 |  |
| B1 | REQ-003 | PASS | link → CMP-001, CMP-002, CMP-003, CMP-006, CMP-007, CMP-008 |  |
| B2 | CMP-001 | PASS | Page → CMP-002 (ApiClient) |  |
| B2 | CMP-002 | PASS | ApiClient → CMP-003 (Api) |  |
| B2 | CMP-003 | PASS | Api → CMP-004 (Application) |  |
| B2 | CMP-003 | PASS | Api → CMP-005 (Application) |  |
| B2 | CMP-003 | PASS | Api → CMP-006 (Application) |  |
| B2 | CMP-004 | PASS | Application → CMP-007 (Domain) |  |
| B2 | CMP-004 | PASS | Application → CMP-008 經介面 IOrderRepository |  |
| B2 | CMP-005 | PASS | Application → CMP-007 (Domain) |  |
| B2 | CMP-005 | PASS | Application → CMP-008 經介面 IOrderRepository |  |
| B2 | CMP-005 | PASS | Application → CMP-009 經介面 IPaymentGateway |  |
| B2 | CMP-006 | PASS | Application → CMP-007 (Domain) |  |
| B2 | CMP-006 | PASS | Application → CMP-008 經介面 IOrderRepository |  |
| B4 | CMP-009 | PASS | PaymentGateway 在 Infrastructure 且有失敗模式 |  |
| B5 | Orders | PASS | owner = Orders |  |
| B5 | Refund | PASS | owner = Orders |  |
| B6 | NFR-001 | PASS | 綁定 API-002 |  |
| B7 | AC-001-1 | PASS | → TST-001, TST-002, TST-003, TST-004, TST-007, TST-008 |  |
| B7 | AC-001-2 | PASS | → TST-001, TST-002, TST-003, TST-004, TST-007, TST-008 |  |
| B7 | AC-002-1 | PASS | → TST-001, TST-002, TST-003, TST-005, TST-007, TST-008, TST-009 |  |
| B7 | AC-002-2 | PASS | → TST-001, TST-002, TST-003, TST-005, TST-007, TST-008, TST-009 |  |
| B7 | AC-003-1 | PASS | → TST-001, TST-002, TST-003, TST-006, TST-007, TST-008 |  |
| B7 | AC-N01-1 | PASS | → TST-010 |  |
