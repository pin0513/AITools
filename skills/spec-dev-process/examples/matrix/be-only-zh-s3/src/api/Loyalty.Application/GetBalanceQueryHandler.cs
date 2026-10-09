using Loyalty.Domain;
using MediatR;

namespace Loyalty.Application;

public sealed record GetBalanceQuery(Guid Id) : IRequest<PointsAccount?>;

public sealed class GetBalanceQueryHandler(IPointsAccountRepository repo) : IRequestHandler<GetBalanceQuery, PointsAccount?>
{
    public Task<PointsAccount?> Handle(GetBalanceQuery q, CancellationToken ct) => repo.GetAsync(q.Id, ct);
}
