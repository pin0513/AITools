import type { Room } from '../types/Room';

export async function listRooms(id: string): Promise<Room> {
  return fetch(`/rooms`).then(r => r.json());
}
