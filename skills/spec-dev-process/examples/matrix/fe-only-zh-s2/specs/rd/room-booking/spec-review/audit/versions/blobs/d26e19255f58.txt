# Survey Mapping

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| 會議室 | Aggregate | modify | Room | src/web/src/types/Room.ts:4 | |
| Capacity rule | Rule | existing | Room.Capacity | src/web/src/types/Room.ts:2 "Capacity" | |
| 預約單 | Entity | new | Booking | | |
| ListRooms | Query | existing | listRooms | src/web/src/api/roomsApi.ts:3 | |
| BookRoom | Command | new | BookRoom | | |
| CheckInBooking | Command | new | CheckInBooking | | |
| ReleaseNoShow | Job | new | ReleaseNoShow | | |
| ListDailyBookings | Query | new | ListDailyBookings | | |
| RoomBookingPage | Page | modify | RoomBookingPage | src/web/src/pages/RoomBookingPage.tsx:3 | |
