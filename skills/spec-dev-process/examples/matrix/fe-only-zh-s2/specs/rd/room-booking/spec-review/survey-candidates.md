# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| Room | src/web/src/types/Room.ts | 4 | `export type Room = {` |
| Room | src/web/src/api/roomsApi.ts | 1 | `import type { Room } from '../types/Room';` |
| Room | src/web/src/api/roomsApi.ts | 3 | `export async function listRooms(id: string): Promise<Room> {` |
| Booking | (無) | | |
| TimeSlot | (無) | | |
| BookRoom | (無) | | |
| CheckInBooking | (無) | | |
| ReleaseNoShow | (無) | | |
| ListDailyBookings | (無) | | |
| 會議室 → Room/RoomBookingPage/roomsApi | src/web/src/types/Room.ts | 4 | `export type Room = {` |
| 會議室 → Room/RoomBookingPage/roomsApi | src/web/src/api/roomsApi.ts | 1 | `import type { Room } from '../types/Room';` |
| 會議室 → Room/RoomBookingPage/roomsApi | src/web/src/api/roomsApi.ts | 3 | `export async function listRooms(id: string): Promise<Room> {` |
| 會議室 → Room/RoomBookingPage/roomsApi | src/web/src/pages/RoomBookingPage.tsx | 1 | `import { listRooms } from '../api/roomsApi';` |
| 會議室 → Room/RoomBookingPage/roomsApi | src/web/src/pages/RoomBookingPage.tsx | 3 | `export function RoomBookingPage({ id }: { id: string }) {` |
| Capacity rule | src/web/src/types/Room.ts | 2 | `export type RoomStatus = 'Capacity';` |
| 預約單 → Booking/RoomBookingPage/BookingForm/DailyBookingTable/bookingStore | src/web/src/pages/RoomBookingPage.tsx | 3 | `export function RoomBookingPage({ id }: { id: string }) {` |
| ListRooms → ListRooms/listRooms | src/web/src/api/roomsApi.ts | 3 | `export async function listRooms(id: string): Promise<Room> {` |
| ListRooms → ListRooms/listRooms | src/web/src/pages/RoomBookingPage.tsx | 1 | `import { listRooms } from '../api/roomsApi';` |
| ListRooms → ListRooms/listRooms | src/web/src/pages/RoomBookingPage.tsx | 4 | `void listRooms(id);` |
| RoomBookingPage | src/web/src/pages/RoomBookingPage.tsx | 3 | `export function RoomBookingPage({ id }: { id: string }) {` |
