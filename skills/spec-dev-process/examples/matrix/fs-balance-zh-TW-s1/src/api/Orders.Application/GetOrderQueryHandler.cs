using Orders.Domain;
using MediatR;

namespace Orders.Application;

public sealed record GetOrderQuery(Guid Id) : IRequest<Order?>;

public sealed class GetOrderQueryHandler(IOrderRepository repo) : IRequestHandler<GetOrderQuery, Order?>
{
    public Task<Order?> Handle(GetOrderQuery q, CancellationToken ct) => repo.GetAsync(q.Id, ct);
}
