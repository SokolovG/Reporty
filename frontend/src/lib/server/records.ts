export async function createRecord (formData: FormData, fetch: Function){
    const text = formData.get('rawInput');
    const title = formData.get('title');
    const taskType = formData.get('taskType');

    if (!text || !title) {
    return { error: 'Title and text are required' };
  }

  const data = {
    rawInput: text.toString(),
    title: taskType ? `${taskType}: ${title}` : title.toString()
  };

  const response = await fetch('/api/v1/records', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    return { error: 'Failed to create record' };
  }

  return { success: true };
}

export function deleteRecord (){}
export function updateRecord (){}
export function extendRecord (){}
export function processAIRecord (){}
