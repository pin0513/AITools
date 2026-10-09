# Loyalty points redemption — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 12 · 測試元件 13 · 技術邊界 PASS 29/29 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-006 | CMP-007 | CMP-010 | CMP-011, CMP-012 | TST-002, TST-004, TST-007, TST-010 | TST-006, TST-011 | TST-005, TST-012 | TST-001 | ✓ |
| REQ-002 | · | CMP-008 | CMP-010 | CMP-011 | TST-004, TST-008, TST-010 | TST-011 | TST-005 | · | ✓ |
| REQ-003 | CMP-006 | CMP-009 | CMP-010 | CMP-011 | TST-003, TST-004, TST-009, TST-010 | TST-006, TST-011 | TST-005 | TST-001 | ✓ |
| NFR-001 | CMP-006 | · | · | · | · | · | · | TST-013 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(render and trigger redeem), CMP-002(UI guard for redeem), CMP-004(client state transition for redeem), CMP-005(call the API for redeem), CMP-006(receive the redeem request), CMP-007(orchestrate redeem), CMP-010(enforce the redeem invariant), CMP-011(persist the redeem result), CMP-012(call the external system for redeem) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011, TST-012 |
| AC-001-2 | REQ-001 | CMP-001(render and trigger redeem), CMP-002(UI guard for redeem), CMP-004(client state transition for redeem), CMP-005(call the API for redeem), CMP-006(receive the redeem request), CMP-007(orchestrate redeem), CMP-010(enforce the redeem invariant), CMP-011(persist the redeem result), CMP-012(call the external system for redeem) | TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011, TST-012 |
| AC-002-1 | REQ-002 | CMP-004(client state transition for expire), CMP-005(call the API for expire), CMP-008(orchestrate expire), CMP-010(enforce the expire invariant), CMP-011(persist the expire result) | TST-004, TST-005, TST-008, TST-010, TST-011 |
| AC-003-1 | REQ-003 | CMP-001(render and trigger view), CMP-003(UI guard for view), CMP-004(client state transition for view), CMP-005(call the API for view), CMP-006(receive the view request), CMP-009(orchestrate view), CMP-010(enforce the view invariant), CMP-011(persist the view result) | TST-001, TST-003, TST-004, TST-005, TST-006, TST-009, TST-010, TST-011 |
| AC-N01-1 | NFR-001 | CMP-006(NFR balance never negative) | TST-013 |

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
| INFO | G-GL-consistency | 「points account」→ PointsAccount 與 prev 一致 |
| INFO | G-SV-evidence | PointsAccount → src/api/Loyalty.Domain/PointsAccount.cs:5 已驗證(符號 PointsAccount) |
| INFO | G-SV-evidence | Balance rule → src/api/Loyalty.Domain/PointsAccount.cs:8 "Balance" 已驗證(字面 "Balance") |
| INFO | G-SV-evidence | GetBalance → src/api/Loyalty.Application/GetBalanceQueryHandler.cs:8 已驗證(對照表 Application 層 GetBalanceQueryHandler) |
| INFO | G-SV-evidence | SqlPointsAccountRepository → src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs:5 已驗證(符號 SqlPointsAccountRepository) |
| INFO | G-SV-evidence | RewardVendorClient → src/api/Loyalty.Infrastructure/RewardVendorClient.cs:5 已驗證(符號 RewardVendorClient) |
| INFO | G-SV-evidence | PointsController → src/api/Loyalty.Api/Controllers/PointsController.cs:8 已驗證(符號 PointsController) |
| INFO | G-SV-evidence | RewardsPage → src/web/src/pages/RewardsPage.tsx:3 已驗證(符號 RewardsPage) |
| INFO | G-SV-evidence | PointsAccount type → src/web/src/types/PointsAccount.ts:4 已驗證(符號 PointsAccount) |
