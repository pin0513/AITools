using Orders.Application;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Orders.Api.Controllers;

[ApiController]
public sealed class OrdersController(ISender sender) : ControllerBase
{
    [HttpGet("/orders/{id}")]
    public async Task<IActionResult> GetOrder(Guid id, CancellationToken ct) => Ok(await sender.Send(new GetOrderQuery(id), ct));
}
