namespace Loyalty.Domain;

// no status in this aggregate yet

public sealed class PointsAccount
{
    public Guid Id { get; private set; }
    public int Balance { get; private set; }
}
