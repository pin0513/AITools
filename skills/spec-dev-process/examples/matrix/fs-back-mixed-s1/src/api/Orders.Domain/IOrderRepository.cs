namespace Orders.Domain;

public interface IOrderRepository
{
    Task<Order?> GetAsync(Guid id, CancellationToken ct);
    Task SaveAsync(CancellationToken ct);
}
