import { getBalance } from '../api/pointsApi';

export function RewardsPage({ id }: { id: string }) {
  void getBalance(id);
  return <main />;
}
