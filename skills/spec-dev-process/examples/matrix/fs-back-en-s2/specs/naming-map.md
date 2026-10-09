# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| book | BookRoom |  | POST /rooms/{id}/bookings | BookRoomCommandHandler |  |  |  | room-booking |
| booking | Booking | RoomBookingPage |  | CheckInBookingCommandHandler, ListDailyBookingsQueryHandler | Booking |  | Booking | room-booking |
| CalendarServiceClient | CalendarServiceClient |  |  |  |  | CalendarServiceClient |  | room-booking |
| Capacity rule | Capacity |  |  |  | Capacity |  |  | room-booking |
| check in | CheckInBooking |  | POST /bookings/{id}/check-in | CheckInBookingCommandHandler |  |  |  | room-booking |
| view | ListDailyBookings |  | GET /bookings/daily | ListDailyBookingsQueryHandler |  |  |  | room-booking |
| ListRooms | ListRooms |  |  | ListRoomsQueryHandler |  |  |  | room-booking |
| release | ReleaseNoShow |  |  | ReleaseNoShowJob |  |  |  | room-booking |
| meeting room | Room | RoomBookingPage, roomsApi, Room | RoomsController | BookRoomCommandHandler | Room | SqlRoomRepository | Rooms | room-booking |
| RoomBookingPage | RoomBookingPage | RoomBookingPage |  |  |  |  |  | room-booking |
| RoomsController | RoomsController |  | RoomsController |  |  |  |  | room-booking |
| SqlRoomRepository | SqlRoomRepository |  |  |  |  | SqlRoomRepository |  | room-booking |
| time slot | TimeSlot |  |  |  |  |  |  | room-booking |
