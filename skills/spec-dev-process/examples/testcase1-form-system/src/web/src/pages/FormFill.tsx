import { submitForm } from '../api/client';
export function FormFill({ formId }: { formId: string }) {
  // issue-b:填寫並送出
  return <button onClick={() => submitForm(formId, {})}>Submit</button>;
}
