# 會員點數兌換 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 5 · 測試元件 6 · 技術邊界 PASS 17/17 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | · | · | · | · | TST-002, TST-004 | · | TST-005 | TST-001 | ✓ |
| REQ-002 | · | · | · | · | TST-004 | · | TST-005 | · | ✓ |
| REQ-003 | · | · | · | · | TST-003, TST-004 | · | TST-005 | TST-001 | ✓ |
| NFR-001 | · | · | · | · | · | · | · | TST-006 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(顯示並觸發redeem), CMP-002(redeem的 UI 守衛), CMP-004(redeem的前端狀態轉移), CMP-005(呼叫redeem API) | TST-001, TST-002, TST-004, TST-005 |
| AC-001-2 | REQ-001 | CMP-001(顯示並觸發redeem), CMP-002(redeem的 UI 守衛), CMP-004(redeem的前端狀態轉移), CMP-005(呼叫redeem API) | TST-001, TST-002, TST-004, TST-005 |
| AC-002-1 | REQ-002 | CMP-004(expire的前端狀態轉移), CMP-005(呼叫expire API) | TST-004, TST-005 |
| AC-003-1 | REQ-003 | CMP-001(顯示並觸發view), CMP-003(view的 UI 守衛), CMP-004(view的前端狀態轉移), CMP-005(呼叫view API) | TST-001, TST-003, TST-004, TST-005 |
| AC-N01-1 | NFR-001 | CMP-005(NFR balance never negative) | TST-006 |

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
| INFO | G-SV-evidence | 點數帳戶 (PointsAccount) → src/web/src/types/PointsAccount.ts:4 已放行·弱證據(符號 PointsAccount;只比對到名字) |
| INFO | G-SV-evidence | Balance rule → src/web/src/types/PointsAccount.ts:2 "Balance" 已放行·強證據(字面 "Balance") |
| INFO | G-SV-evidence | GetBalance → src/web/src/api/pointsApi.ts:4 "/members" 已放行·強證據(字面 "/members") |
| INFO | G-SV-evidence | RewardsPage → src/web/src/pages/RewardsPage.tsx:4 "getBalance(id)" 已放行·強證據(字面 "getBalance(id)") |
