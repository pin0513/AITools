using Loyalty.Application;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Loyalty.Api.Controllers;

[ApiController]
public sealed class PointsController(ISender sender) : ControllerBase
{
    [HttpGet("/members/{id}/points")]
    public async Task<IActionResult> GetBalance(Guid id, CancellationToken ct) => Ok(await sender.Send(new GetBalanceQuery(id), ct));
}
