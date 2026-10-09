namespace Orders.Infrastructure;

public interface IPaymentGateway { Task RefundAsync(Guid id, CancellationToken ct); }

public sealed class PaymentGatewayClient : IPaymentGateway
{
    public Task RefundAsync(Guid id, CancellationToken ct) => Task.CompletedTask;
}
