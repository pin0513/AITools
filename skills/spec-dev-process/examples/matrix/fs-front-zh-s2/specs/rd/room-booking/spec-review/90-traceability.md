# 會議室預約 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 13 · 測試元件 14 · 技術邊界 PASS 32/32 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-007 | CMP-008 | · | CMP-012, CMP-013 | TST-002, TST-005, TST-008 | TST-007, TST-012 | TST-006, TST-013 | TST-001 | ✓ |
| REQ-002 | CMP-007 | CMP-009, CMP-010 | · | CMP-012, CMP-013 | TST-003, TST-005, TST-009, TST-010 | TST-007, TST-012 | TST-006, TST-013 | TST-001 | ✓ |
| REQ-003 | CMP-007 | CMP-011 | · | CMP-012 | TST-004, TST-005, TST-011 | TST-007, TST-012 | TST-006 | TST-001 | ✓ |
| NFR-001 | CMP-007 | · | · | · | · | · | · | TST-014 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(顯示並觸發預約), CMP-002(預約的 UI 守衛), CMP-005(預約的前端狀態轉移), CMP-006(呼叫預約 API), CMP-007(接收預約請求), CMP-008(編排預約), CMP-012(持久化預約結果), CMP-013(為預約呼叫外部系統) | TST-001, TST-002, TST-005, TST-006, TST-007, TST-008, TST-012, TST-013 |
| AC-001-2 | REQ-001 | CMP-001(顯示並觸發預約), CMP-002(預約的 UI 守衛), CMP-005(預約的前端狀態轉移), CMP-006(呼叫預約 API), CMP-007(接收預約請求), CMP-008(編排預約), CMP-012(持久化預約結果), CMP-013(為預約呼叫外部系統) | TST-001, TST-002, TST-005, TST-006, TST-007, TST-008, TST-012, TST-013 |
| AC-002-1 | REQ-002 | CMP-001(顯示並觸發報到), CMP-003(報到的 UI 守衛), CMP-005(報到的前端狀態轉移), CMP-006(呼叫報到 API), CMP-007(接收報到請求), CMP-009(編排報到), CMP-012(持久化報到結果), CMP-010(編排釋放), CMP-013(為釋放呼叫外部系統) | TST-001, TST-003, TST-005, TST-006, TST-007, TST-009, TST-010, TST-012, TST-013 |
| AC-002-2 | REQ-002 | CMP-001(顯示並觸發報到), CMP-003(報到的 UI 守衛), CMP-005(報到的前端狀態轉移), CMP-006(呼叫報到 API), CMP-007(接收報到請求), CMP-009(編排報到), CMP-012(持久化報到結果), CMP-010(編排釋放), CMP-013(為釋放呼叫外部系統) | TST-001, TST-003, TST-005, TST-006, TST-007, TST-009, TST-010, TST-012, TST-013 |
| AC-003-1 | REQ-003 | CMP-001(顯示並觸發查看), CMP-004(查看的 UI 守衛), CMP-005(查看的前端狀態轉移), CMP-006(呼叫查看 API), CMP-007(接收查看請求), CMP-011(編排查看), CMP-012(持久化查看結果) | TST-001, TST-004, TST-005, TST-006, TST-007, TST-011, TST-012 |
| AC-N01-1 | NFR-001 | CMP-007(NFR 100 concurrent → 1 success) | TST-014 |

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
| INFO | G-SV-evidence | 會議室 → src/api/Rooms.Domain/Room.cs:5 已驗證(glossary 解析 Room) |
| INFO | G-SV-evidence | Capacity rule → src/api/Rooms.Domain/Room.cs:8 "Capacity" 已驗證(字面 "Capacity") |
| INFO | G-SV-evidence | ListRooms → src/api/Rooms.Application/ListRoomsQueryHandler.cs:8 已驗證(對照表 Application 層 ListRoomsQueryHandler) |
| INFO | G-SV-evidence | SqlRoomRepository → src/api/Rooms.Infrastructure/SqlRoomRepository.cs:5 已驗證(符號 SqlRoomRepository) |
| INFO | G-SV-evidence | CalendarServiceClient → src/api/Rooms.Infrastructure/CalendarServiceClient.cs:5 已驗證(符號 CalendarServiceClient) |
| INFO | G-SV-evidence | RoomsController → src/api/Rooms.Api/Controllers/RoomsController.cs:8 已驗證(符號 RoomsController) |
| INFO | G-SV-evidence | RoomBookingPage → src/web/src/pages/RoomBookingPage.tsx:3 已驗證(符號 RoomBookingPage) |
| INFO | G-SV-evidence | Room type → src/web/src/types/Room.ts:4 已驗證(符號 Room) |
