namespace Rooms.Infrastructure;

public interface ICalendarService { Task SyncAsync(Guid id, CancellationToken ct); }

public sealed class CalendarServiceClient : ICalendarService
{
    public Task SyncAsync(Guid id, CancellationToken ct) => Task.CompletedTask;
}
