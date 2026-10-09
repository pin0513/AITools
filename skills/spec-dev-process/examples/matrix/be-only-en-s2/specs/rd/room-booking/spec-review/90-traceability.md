# Meeting room booking — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 4 · 技術元件 8 · 測試元件 9 · 技術邊界 PASS 27/27 · 未覆蓋需求 0

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-001 | CMP-002 | CMP-006 | CMP-007, CMP-008 | TST-002, TST-006 | TST-001, TST-007 | TST-008 | · | ✓ |
| REQ-002 | CMP-001 | CMP-003, CMP-004 | CMP-006 | CMP-007, CMP-008 | TST-003, TST-004, TST-006 | TST-001, TST-007 | TST-008 | · | ✓ |
| REQ-003 | CMP-001 | CMP-005 | CMP-006 | CMP-007 | TST-005, TST-006 | TST-001, TST-007 | · | · | ✓ |
| NFR-001 | CMP-001 | · | · | · | · | · | · | TST-009 | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(receive the book request), CMP-002(orchestrate book), CMP-006(enforce the book invariant), CMP-007(persist the book result), CMP-008(call the external system for book) | TST-001, TST-002, TST-006, TST-007, TST-008 |
| AC-001-2 | REQ-001 | CMP-001(receive the book request), CMP-002(orchestrate book), CMP-006(enforce the book invariant), CMP-007(persist the book result), CMP-008(call the external system for book) | TST-001, TST-002, TST-006, TST-007, TST-008 |
| AC-002-1 | REQ-002 | CMP-001(receive the check in request), CMP-003(orchestrate check in), CMP-006(enforce the check in invariant), CMP-007(persist the check in result), CMP-004(orchestrate release), CMP-008(call the external system for release) | TST-001, TST-003, TST-004, TST-006, TST-007, TST-008 |
| AC-002-2 | REQ-002 | CMP-001(receive the check in request), CMP-003(orchestrate check in), CMP-006(enforce the check in invariant), CMP-007(persist the check in result), CMP-004(orchestrate release), CMP-008(call the external system for release) | TST-001, TST-003, TST-004, TST-006, TST-007, TST-008 |
| AC-003-1 | REQ-003 | CMP-001(receive the view request), CMP-005(orchestrate view), CMP-006(enforce the view invariant), CMP-007(persist the view result) | TST-001, TST-005, TST-006, TST-007 |
| AC-N01-1 | NFR-001 | CMP-001(NFR 100 concurrent → 1 success) | TST-009 |

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
| INFO | G-GL-consistency | 「meeting room」→ Room 與 prev 一致 |
| INFO | G-SV-evidence | Room → src/api/Rooms.Domain/Room.cs:5 已驗證(符號 Room) |
| INFO | G-SV-evidence | Capacity rule → src/api/Rooms.Domain/Room.cs:8 "Capacity" 已驗證(字面 "Capacity") |
| INFO | G-SV-evidence | ListRooms → src/api/Rooms.Application/ListRoomsQueryHandler.cs:8 已驗證(對照表 Application 層 ListRoomsQueryHandler) |
| INFO | G-SV-evidence | SqlRoomRepository → src/api/Rooms.Infrastructure/SqlRoomRepository.cs:5 已驗證(符號 SqlRoomRepository) |
| INFO | G-SV-evidence | CalendarServiceClient → src/api/Rooms.Infrastructure/CalendarServiceClient.cs:5 已驗證(符號 CalendarServiceClient) |
| INFO | G-SV-evidence | RoomsController → src/api/Rooms.Api/Controllers/RoomsController.cs:8 已驗證(符號 RoomsController) |
