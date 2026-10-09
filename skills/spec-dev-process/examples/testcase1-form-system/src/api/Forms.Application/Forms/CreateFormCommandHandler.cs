using Forms.Domain;
using MediatR;

namespace Forms.Application.Forms;

public sealed record CreateFormCommand(Guid OwnerId, string Title) : IRequest<Guid>;

public sealed class CreateFormCommandHandler(IFormRepository repo) : IRequestHandler<CreateFormCommand, Guid>
{
    public async Task<Guid> Handle(CreateFormCommand cmd, CancellationToken ct)
    {
        var form = Form.Create(cmd.OwnerId, cmd.Title);
        await repo.AddAsync(form, ct);
        await repo.SaveAsync(ct);
        return form.Id;
    }
}
