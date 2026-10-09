export async function createForm(title: string): Promise<{ id: string }> {
  return fetch('/forms', { method: 'POST', body: JSON.stringify({ title }) }).then(r => r.json());
}
export async function submitForm(formId: string, answers: Record<string, string>): Promise<{ id: string }> {
  return fetch(`/forms/${formId}/submissions`, { method: 'POST', body: JSON.stringify({ answers }) }).then(r => r.json());
}
