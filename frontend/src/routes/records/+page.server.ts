import type { Actions, PageServerLoad } from "./$types";
import {redirect} from "@sveltejs/kit";

const API_BASE = 'http://localhost:8080';

export const actions: Actions = {
    create: async ({ request, cookies }) => {
        const token = cookies.get('authToken');
        if (!token) {
            throw redirect(303, '/login');
        }

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
            const response = await fetch(`${API_BASE}/v1/records`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: 'Failed to create record' };
            }

        } catch (error) {
            return { error: 'Error during record creation' };
        }
        throw redirect(303, '/records');
    },

    delete: async ({ request, cookies }) => {
        const token = cookies.get('authToken');
        if (!token) {
            throw redirect(303, '/login');
        }

        const formData = await request.formData();
        const recordId = formData.get('recordId');

        if (!recordId) {
            return { error: 'Record ID is required' };
        }

        try {
            const response = await fetch(`${API_BASE}/v1/records/${recordId}`, {
                method: 'DELETE',
                headers: { 'Authorization': token }
            });

            if (!response.ok) {
                return { error: 'Failed to delete record' };
            }

        } catch (error) {
            return { error: 'Error during record deletion' };
        }
        throw redirect(303, '/records');
    },

    updateStatus: async ({ request, cookies }) => {
        const token = cookies.get('authToken');
        if (!token) {
            throw redirect(303, '/login');
        }

        const formData = await request.formData();
        const recordId = formData.get('recordId');
        const newStatus = formData.get('status');

        if (!recordId || !newStatus) {
            return { error: 'Record ID and status are required' };
        }

        try {
            const response = await fetch(`${API_BASE}/v1/records/${recordId}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify({ status: newStatus })
            });
            if (!response.ok) {
                return { error: 'Failed to update status' };
            }

        } catch (error) {
            return { error: 'Error during status update' };
        }
        throw redirect(303, '/records');
    },

    appendText: async ({ request, cookies }) => {
        const token = cookies.get('authToken');
        if (!token) {
            throw redirect(303, '/login');
        }

        const formData = await request.formData();
        const recordId = formData.get('recordId');
        const additionalInput = formData.get('additionalInput');

        if (!recordId || !additionalInput) {
            return { error: 'Record ID and text are required' };
        }

        try {
            const response = await fetch(`${API_BASE}/v1/records/${recordId}/append`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify({ additionalInput: additionalInput.toString() })
            });

            if (!response.ok) {
                return { error: 'Failed to append text' };
            }

        } catch (error) {
            return { error: 'Error during text append' };
        }
        throw redirect(303, '/records');
    },

    processAI: async ({ request, cookies }) => {
        const token = cookies.get('authToken');
        if (!token) {
            throw redirect(303, '/login');
        }

        const formData = await request.formData();
        const recordId = formData.get('recordId');

        if (!recordId) {
            return { error: 'Record ID is required' };
        }

        try {
            const response = await fetch(`${API_BASE}/v1/records/${recordId}/process`, {
                method: 'POST',
                headers: { 'Authorization': token }
            });

            if (!response.ok) {
                return { error: 'Failed to process with AI' };
            }

        } catch (error) {
            return { error: 'Error during AI processing' };
        }
        throw redirect(303, '/records');
    }
};
export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('authToken');

    if (!token) {
        throw redirect(303, '/login');
    }

    try {
        const [recordsResponse, taskTypesResponse] = await Promise.all([
            fetch(`${API_BASE}/v1/records`, {
                headers: { 'Authorization': token }
            }),
            fetch(`${API_BASE}/v1/settings/task-types`, {
                headers: { 'Authorization': token }
            })
        ]);

        if (!recordsResponse.ok || !taskTypesResponse.ok) {
            throw redirect(303, '/login');
        }

        const records = await recordsResponse.json();
        const taskTypes = await taskTypesResponse.json();

        return { records, taskTypes };
    } catch (error) {
        console.log("❌ Error loading data:", error);
    }
};
