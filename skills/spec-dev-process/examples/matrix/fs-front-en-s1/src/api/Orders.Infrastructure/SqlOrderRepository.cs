using Orders.Domain;

namespace Orders.Infrastructure;

public sealed class SqlOrderRepository : IOrderRepository
{
    public Task<Order?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<Order?>(null);
    public Task SaveAsync(CancellationToken ct) => Task.CompletedTask;
}
