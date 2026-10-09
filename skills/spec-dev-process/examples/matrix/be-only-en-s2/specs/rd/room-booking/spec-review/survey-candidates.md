# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| Room | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 6 | `public sealed record ListRoomsQuery(Guid Id) : IRequest<Room?>;` |
| Room | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 8 | `public sealed class ListRoomsQueryHandler(IRoomRepository repo) : IRequestHandler<ListRoomsQuery, Ro` |
| Room | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 10 | `public Task<Room?> Handle(ListRoomsQuery q, CancellationToken ct) => repo.GetAsync(q.Id, ct);` |
| Room | src/api/Rooms.Infrastructure/SqlRoomRepository.cs | 7 | `public Task<Room?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<Room?>(null);` |
| Room | src/api/Rooms.Domain/Room.cs | 5 | `public sealed class Room` |
| Booking | (無) | | |
| TimeSlot | (無) | | |
| BookRoom | (無) | | |
| CheckInBooking | (無) | | |
| ReleaseNoShow | (無) | | |
| ListDailyBookings | (無) | | |
| Room → Room/RoomsController/BookRoomCommandHandler/SqlRoomRepository/Rooms | src/database/001_rooms.sql | 2 | `CREATE TABLE Rooms (` |
| Room → Room/RoomsController/BookRoomCommandHandler/SqlRoomRepository/Rooms | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 1 | `using Rooms.Domain;` |
| Room → Room/RoomsController/BookRoomCommandHandler/SqlRoomRepository/Rooms | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 4 | `namespace Rooms.Application;` |
| Room → Room/RoomsController/BookRoomCommandHandler/SqlRoomRepository/Rooms | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 6 | `public sealed record ListRoomsQuery(Guid Id) : IRequest<Room?>;` |
| Room → Room/RoomsController/BookRoomCommandHandler/SqlRoomRepository/Rooms | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 8 | `public sealed class ListRoomsQueryHandler(IRoomRepository repo) : IRequestHandler<ListRoomsQuery, Ro` |
| Capacity rule | src/database/001_rooms.sql | 4 | `Capacity nvarchar(50) NOT NULL` |
| Capacity rule | src/api/Rooms.Domain/Room.cs | 8 | `public int Capacity { get; private set; }` |
| Booking → Booking/CheckInBookingCommandHandler/ListDailyBookingsQueryHandler | (無) | | |
| ListRooms → ListRooms/ListRoomsQueryHandler | src/api/Rooms.Application/ListRoomsQueryHandler.cs | 8 | `public sealed class ListRoomsQueryHandler(IRoomRepository repo) : IRequestHandler<ListRoomsQuery, Ro` |
| ListRooms → ListRooms/ListRoomsQueryHandler | src/api/Rooms.Api/Controllers/RoomsController.cs | 11 | `public async Task<IActionResult> ListRooms(Guid id, CancellationToken ct) => Ok(await sender.Send(ne` |
| BookRoom → BookRoom/BookRoomCommandHandler | (無) | | |
| CheckInBooking → CheckInBooking/CheckInBookingCommandHandler | (無) | | |
| ReleaseNoShow → ReleaseNoShow/ReleaseNoShowJob | (無) | | |
| ListDailyBookings → ListDailyBookings/ListDailyBookingsQueryHandler | (無) | | |
| SqlRoomRepository | src/api/Rooms.Infrastructure/SqlRoomRepository.cs | 5 | `public sealed class SqlRoomRepository : IRoomRepository` |
| CalendarServiceClient | src/api/Rooms.Infrastructure/CalendarServiceClient.cs | 5 | `public sealed class CalendarServiceClient : ICalendarService` |
| RoomsController | src/api/Rooms.Api/Controllers/RoomsController.cs | 8 | `public sealed class RoomsController(ISender sender) : ControllerBase` |
