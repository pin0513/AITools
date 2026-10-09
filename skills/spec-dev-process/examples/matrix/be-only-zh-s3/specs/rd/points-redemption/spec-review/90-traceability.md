# 會員點數兌換 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 7 · 測試元件 8 · 技術邊界 PASS 22/22 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-001 | CMP-002 | CMP-005 | CMP-006, CMP-007 | TST-002, TST-005 | TST-001, TST-006 | TST-007 | · | ✓ |
| REQ-002 | · | CMP-003 | CMP-005 | CMP-006 | TST-003, TST-005 | TST-006 | · | · | ✓ |
| REQ-003 | CMP-001 | CMP-004 | CMP-005 | CMP-006 | TST-004, TST-005 | TST-001, TST-006 | · | · | ✓ |
| NFR-001 | CMP-001 | · | · | · | · | · | · | TST-008 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(接收兌換請求), CMP-002(編排兌換), CMP-005(兌換的業務規則與不變量), CMP-006(持久化兌換結果), CMP-007(為兌換呼叫外部系統) | TST-001, TST-002, TST-005, TST-006, TST-007 |
| AC-001-2 | REQ-001 | CMP-001(接收兌換請求), CMP-002(編排兌換), CMP-005(兌換的業務規則與不變量), CMP-006(持久化兌換結果), CMP-007(為兌換呼叫外部系統) | TST-001, TST-002, TST-005, TST-006, TST-007 |
| AC-002-1 | REQ-002 | CMP-003(編排到期), CMP-005(到期的業務規則與不變量), CMP-006(持久化到期結果) | TST-003, TST-005, TST-006 |
| AC-003-1 | REQ-003 | CMP-001(接收查看請求), CMP-004(編排查看), CMP-005(查看的業務規則與不變量), CMP-006(持久化查看結果) | TST-001, TST-004, TST-005, TST-006 |
| AC-N01-1 | NFR-001 | CMP-001(NFR balance never negative) | TST-008 |

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
| INFO | G-GL-consistency | 「點數帳戶」→ PointsAccount 與 prev 一致 |
| INFO | G-SV-evidence | 點數帳戶 → src/api/Loyalty.Domain/PointsAccount.cs:5 已驗證(glossary 解析 PointsAccount) |
| INFO | G-SV-evidence | Balance rule → src/api/Loyalty.Domain/PointsAccount.cs:8 "Balance" 已驗證(字面 "Balance") |
| INFO | G-SV-evidence | GetBalance → src/api/Loyalty.Application/GetBalanceQueryHandler.cs:8 已驗證(對照表 Application 層 GetBalanceQueryHandler) |
| INFO | G-SV-evidence | SqlPointsAccountRepository → src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs:5 已驗證(符號 SqlPointsAccountRepository) |
| INFO | G-SV-evidence | RewardVendorClient → src/api/Loyalty.Infrastructure/RewardVendorClient.cs:5 已驗證(符號 RewardVendorClient) |
| INFO | G-SV-evidence | PointsController → src/api/Loyalty.Api/Controllers/PointsController.cs:8 已驗證(符號 PointsController) |
