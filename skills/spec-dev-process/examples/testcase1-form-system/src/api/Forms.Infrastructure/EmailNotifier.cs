namespace Forms.Infrastructure;

/// <summary>既有通知介面(issue-b 送出成功通知)。</summary>
public interface INotifier { Task NotifyAsync(Guid userId, string template, object model, CancellationToken ct); }

public sealed class EmailNotifier : INotifier
{
    public Task NotifyAsync(Guid userId, string template, object model, CancellationToken ct) => Task.CompletedTask; // SMTP 略
}
