using Rooms.Application;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace Rooms.Api.Controllers;

[ApiController]
public sealed class RoomsController(ISender sender) : ControllerBase
{
    [HttpGet("/rooms")]
    public async Task<IActionResult> ListRooms(Guid id, CancellationToken ct) => Ok(await sender.Send(new ListRoomsQuery(id), ct));
}
