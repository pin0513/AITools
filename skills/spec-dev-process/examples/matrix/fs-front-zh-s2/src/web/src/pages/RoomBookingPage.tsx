import { listRooms } from '../api/roomsApi';

export function RoomBookingPage({ id }: { id: string }) {
  void listRooms(id);
  return <main />;
}
