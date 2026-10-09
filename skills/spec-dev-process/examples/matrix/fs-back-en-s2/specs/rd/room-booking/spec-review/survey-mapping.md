# Survey Mapping

## Mapping
| Element | Element Type | Status | Code Target | Evidence | Note |
|---|---|---|---|---|---|
| Room | Aggregate | modify | Room | src/api/Rooms.Domain/Room.cs:5 | |
| Capacity rule | Rule | existing | Room.Capacity | src/api/Rooms.Domain/Room.cs:8 "Capacity" | |
| Booking | Entity | new | Booking | | |
| ListRooms | Query | existing | ListRoomsQueryHandler | src/api/Rooms.Application/ListRoomsQueryHandler.cs:8 | |
| BookRoom | Command | new | BookRoom | | |
| CheckInBooking | Command | new | CheckInBooking | | |
| ReleaseNoShow | Job | new | ReleaseNoShow | | |
| ListDailyBookings | Query | new | ListDailyBookings | | |
| SqlRoomRepository | Adapter | modify | SqlRoomRepository | src/api/Rooms.Infrastructure/SqlRoomRepository.cs:5 | |
| CalendarServiceClient | Adapter | existing | CalendarServiceClient | src/api/Rooms.Infrastructure/CalendarServiceClient.cs:5 | |
| RoomsController | Api | modify | RoomsController | src/api/Rooms.Api/Controllers/RoomsController.cs:8 | |
| RoomBookingPage | Page | modify | RoomBookingPage | src/web/src/pages/RoomBookingPage.tsx:3; src/web/src/pages/RoomBookingPage.tsx:4 "listRooms(id)" | |
| Room type | Type | existing | Room | src/web/src/types/Room.ts:4 | |
