using Rooms.Domain;

namespace Rooms.Infrastructure;

public sealed class SqlRoomRepository : IRoomRepository
{
    public Task<Room?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<Room?>(null);
    public Task SaveAsync(CancellationToken ct) => Task.CompletedTask;
}
