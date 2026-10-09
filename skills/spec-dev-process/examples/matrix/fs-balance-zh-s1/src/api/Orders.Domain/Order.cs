namespace Orders.Domain;

public enum OrderStatus { Placed, Shipped }

public sealed class Order
{
    public Guid Id { get; private set; }
    public OrderStatus Status { get; private set; } = OrderStatus.Placed;
}
