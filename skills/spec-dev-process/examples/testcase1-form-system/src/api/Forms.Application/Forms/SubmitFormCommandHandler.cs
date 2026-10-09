using Forms.Domain;
using MediatR;

namespace Forms.Application.Forms;

public sealed record SubmitFormCommand(Guid FormId, Guid SubmitterId, IReadOnlyDictionary<string, string> Answers) : IRequest<Guid>;

public sealed class SubmitFormCommandHandler(IFormRepository forms, IFormSubmissionRepository submissions) : IRequestHandler<SubmitFormCommand, Guid>
{
    public async Task<Guid> Handle(SubmitFormCommand cmd, CancellationToken ct)
    {
        var form = await forms.GetAsync(cmd.FormId, ct) ?? throw new DomainException("FORM_NOT_FOUND");
        var submission = FormSubmission.Create(form, cmd.SubmitterId, cmd.Answers);
        await submissions.AddAsync(submission, ct);
        await submissions.SaveAsync(ct);
        return submission.Id;
    }
}
