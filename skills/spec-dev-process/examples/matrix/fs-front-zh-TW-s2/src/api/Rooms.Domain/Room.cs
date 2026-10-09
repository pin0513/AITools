namespace Rooms.Domain;

// no status in this aggregate yet

public sealed class Room
{
    public Guid Id { get; private set; }
    public int Capacity { get; private set; }
}
