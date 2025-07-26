import type { Actions, PageServerLoad } from "./$types";

export const actions: Actions = {
    create: async ({ request, cookies }) => {

        const token = cookies.get('authToken');
        console.log(token)
        const formData = await request.formData();

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
        const response = await fetch('http://localhost:8080/v1/records', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            return { error: 'Failed to create record' };
        }

        return { success: true };
    } catch (error) {
        return { error: 'Error during record creation' };
    }
    },
    delete: async ({ request }) => {

    },
    edit: async ({ request }) => {

    },
    change_status: async ({ request }) => {

    },
    input_text: async ({ request }) => {

    }

};

export const load: PageServerLoad = async ({ params }) => {
    const recordsResponse = await fetch('http://localhost:8080/v1/records');
    const records = await recordsResponse.json();

    const taskTypesResponse = await fetch('http://localhost:8080/v1/settings/task-types');
    const taskTypes = await taskTypesResponse.json();

    return {
        records,
        taskTypes
    };
};
