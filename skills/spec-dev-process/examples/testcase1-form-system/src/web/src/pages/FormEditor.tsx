import { createForm } from '../api/client';
export function FormEditor() {
  // issue-a:建立表單與欄位
  return <button onClick={() => createForm('new')}>Create</button>;
}
