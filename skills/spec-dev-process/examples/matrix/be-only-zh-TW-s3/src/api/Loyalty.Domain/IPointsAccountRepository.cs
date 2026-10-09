namespace Loyalty.Domain;

public interface IPointsAccountRepository
{
    Task<PointsAccount?> GetAsync(Guid id, CancellationToken ct);
    Task SaveAsync(CancellationToken ct);
}
