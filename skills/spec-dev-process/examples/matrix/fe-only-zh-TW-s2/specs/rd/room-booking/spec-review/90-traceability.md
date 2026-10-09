# 會議室預約 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 6 · 測試元件 7 · 技術邊界 PASS 20/20 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | · | · | · | · | TST-002, TST-005 | · | TST-006 | TST-001 | ✓ |
| REQ-002 | · | · | · | · | TST-003, TST-005 | · | TST-006 | TST-001 | ✓ |
| REQ-003 | · | · | · | · | TST-004, TST-005 | · | TST-006 | TST-001 | ✓ |
| NFR-001 | · | · | · | · | · | · | · | TST-007 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(顯示並觸發預約), CMP-002(預約的 UI 守衛), CMP-005(預約的前端狀態轉移), CMP-006(呼叫預約 API) | TST-001, TST-002, TST-005, TST-006 |
| AC-001-2 | REQ-001 | CMP-001(顯示並觸發預約), CMP-002(預約的 UI 守衛), CMP-005(預約的前端狀態轉移), CMP-006(呼叫預約 API) | TST-001, TST-002, TST-005, TST-006 |
| AC-002-1 | REQ-002 | CMP-001(顯示並觸發報到), CMP-003(報到的 UI 守衛), CMP-005(報到的前端狀態轉移), CMP-006(呼叫報到 API) | TST-001, TST-003, TST-005, TST-006 |
| AC-002-2 | REQ-002 | CMP-001(顯示並觸發報到), CMP-003(報到的 UI 守衛), CMP-005(報到的前端狀態轉移), CMP-006(呼叫報到 API) | TST-001, TST-003, TST-005, TST-006 |
| AC-003-1 | REQ-003 | CMP-001(顯示並觸發查看), CMP-004(查看的 UI 守衛), CMP-005(查看的前端狀態轉移), CMP-006(呼叫查看 API) | TST-001, TST-004, TST-005, TST-006 |
| AC-N01-1 | NFR-001 | CMP-006(NFR 100 concurrent → 1 success) | TST-007 |

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
| INFO | G-GL-consistency | 「會議室」→ Room 與 prev 一致 |
| INFO | G-SV-evidence | 會議室 → src/web/src/types/Room.ts:4 已放行·弱證據(glossary 解析 Room;只比對到名字) |
| INFO | G-SV-evidence | Capacity rule → src/web/src/types/Room.ts:2 "Capacity" 已放行·強證據(字面 "Capacity") |
| INFO | G-SV-evidence | ListRooms → src/web/src/api/roomsApi.ts:4 "/rooms" 已放行·強證據(字面 "/rooms") |
| INFO | G-SV-evidence | RoomBookingPage → src/web/src/pages/RoomBookingPage.tsx:4 "listRooms(id)" 已放行·強證據(字面 "listRooms(id)") |
