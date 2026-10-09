using Forms.Application.Forms;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Forms.Api.Controllers;

[ApiController]
[Route("forms")]
public sealed class FormsController(ISender sender) : ControllerBase
{
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateFormCommand cmd, CancellationToken ct)
        => Ok(new { id = await sender.Send(cmd, ct) });

    [HttpPost("{id:guid}/submissions")]
    public async Task<IActionResult> Submit(Guid id, [FromBody] SubmitFormBody body, CancellationToken ct)
        => Ok(new { id = await sender.Send(new SubmitFormCommand(id, body.SubmitterId, body.Answers), ct) });
}

public sealed record SubmitFormBody(Guid SubmitterId, IReadOnlyDictionary<string, string> Answers);
