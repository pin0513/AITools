namespace Rooms.Domain;

public interface IRoomRepository
{
    Task<Room?> GetAsync(Guid id, CancellationToken ct);
    Task SaveAsync(CancellationToken ct);
}
