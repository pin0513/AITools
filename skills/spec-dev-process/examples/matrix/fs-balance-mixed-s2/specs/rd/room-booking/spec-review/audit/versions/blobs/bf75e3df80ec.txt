# 會議室預約 — test design

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | RoomBookingPageTests | e2e | CMP-001 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-002 | BookingFormTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-003 | CheckInButtonTests | unit | CMP-003 | AC-002-1, AC-002-2 |
| TST-004 | DailyBookingTableTests | unit | CMP-004 | AC-003-1 |
| TST-005 | bookingStoreTests | unit | CMP-005 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-006 | roomsApiTests | contract | CMP-006 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-007 | RoomsControllerTests | integration | CMP-007 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-008 | BookRoomCommandHandlerTests | unit | CMP-008 | AC-001-1, AC-001-2 |
| TST-009 | CheckInBookingCommandHandlerTests | unit | CMP-009 | AC-002-1, AC-002-2 |
| TST-010 | ReleaseNoShowJobTests | unit | CMP-010 | AC-002-1, AC-002-2 |
| TST-011 | ListDailyBookingsQueryHandlerTests | unit | CMP-011 | AC-003-1 |
| TST-012 | BookingTests | unit | CMP-012 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-013 | SqlRoomRepositoryTests | integration | CMP-013 | AC-001-1, AC-001-2, AC-002-1, AC-002-2, AC-003-1 |
| TST-014 | CalendarServiceClientTests | contract | CMP-014 | AC-001-1, AC-001-2, AC-002-1, AC-002-2 |
| TST-015 | NFR-001FitnessTest | e2e | CMP-007 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 / Playwright | 100 concurrent → 1 success | CI nightly |
