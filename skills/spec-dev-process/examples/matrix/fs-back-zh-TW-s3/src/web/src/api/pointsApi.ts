import type { PointsAccount } from '../types/PointsAccount';

export async function getBalance(id: string): Promise<PointsAccount> {
  return fetch(`/members/${id}/points`).then(r => r.json());
}
