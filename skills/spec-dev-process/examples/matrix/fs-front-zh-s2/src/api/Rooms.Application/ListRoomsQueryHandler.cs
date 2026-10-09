using Rooms.Domain;
using MediatR;

namespace Rooms.Application;

public sealed record ListRoomsQuery(Guid Id) : IRequest<Room?>;

public sealed class ListRoomsQueryHandler(IRoomRepository repo) : IRequestHandler<ListRoomsQuery, Room?>
{
    public Task<Room?> Handle(ListRoomsQuery q, CancellationToken ct) => repo.GetAsync(q.Id, ct);
}
