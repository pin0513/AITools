using Loyalty.Domain;

namespace Loyalty.Infrastructure;

public sealed class SqlPointsAccountRepository : IPointsAccountRepository
{
    public Task<PointsAccount?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<PointsAccount?>(null);
    public Task SaveAsync(CancellationToken ct) => Task.CompletedTask;
}
