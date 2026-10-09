namespace Loyalty.Infrastructure;

public interface IRewardVendor { Task FulfillAsync(Guid id, CancellationToken ct); }

public sealed class RewardVendorClient : IRewardVendor
{
    public Task FulfillAsync(Guid id, CancellationToken ct) => Task.CompletedTask;
}
