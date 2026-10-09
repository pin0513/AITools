# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| 預約 | BookRoom |  | POST /rooms/{id}/bookings |  |  |  |  | room-booking |
| 預約單 | Booking | RoomBookingPage, BookingForm, DailyBookingTable, bookingStore |  |  |  |  |  | room-booking |
| Capacity rule | Capacity | Capacity |  |  |  |  |  | room-booking |
| 報到 | CheckInBooking |  | POST /bookings/{id}/check-in |  |  |  |  | room-booking |
| 查看 | ListDailyBookings |  | GET /bookings/daily |  |  |  |  | room-booking |
| ListRooms | ListRooms | listRooms |  |  |  |  |  | room-booking |
| 釋放 | ReleaseNoShow |  |  |  |  |  |  | room-booking |
| 會議室 | Room | RoomBookingPage, roomsApi, Room |  |  |  |  |  | room-booking |
| RoomBookingPage | RoomBookingPage | RoomBookingPage |  |  |  |  |  | room-booking |
| 時段 | TimeSlot |  |  |  |  |  |  | room-booking |
