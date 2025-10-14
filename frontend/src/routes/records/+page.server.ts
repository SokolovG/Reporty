import type {Actions, PageServerLoad} from "./$types";
import {redirect} from "@sveltejs/kit";

export const actions: Actions = {
    create: async ({ request, fetch }) => {
        const formData: FormData = await request.formData();
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

        try {
          const response = await fetch('/api/v1/records', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });

          if (!response.ok) {
            return { error: 'Failed to create record' };
          }

        } catch (error) {
          if (error instanceof Response) throw error;
          return { error: 'Error during record creation' };
        }

        throw redirect(303, '/records');
      }
};


export const load: PageServerLoad = async ({ fetch }) => {

    try {
        const [recordsResponse, taskTypesResponse] = await Promise.all([
            fetch('/api/v1/records'),
            fetch('/api/v1/profile/task-types')
        ]);

        if (!recordsResponse.ok || !taskTypesResponse.ok) {
            return { records: [], taskTypes: [] };
        }

        const recordsJson = await recordsResponse.json();
        const records = recordsJson.data
        const taskTypesJson = await taskTypesResponse.json();
        const taskTypes = taskTypesJson.data

        return { records, taskTypes };
    } catch (error) {
        // If it's a redirect, re-throw it
        if (error instanceof Response) {
            throw error;
        }
        return { records: [], taskTypes: [] };
    }
};
