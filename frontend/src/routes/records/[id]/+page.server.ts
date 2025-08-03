import type { Actions, PageServerLoad } from "./$types";
import {error, redirect} from "@sveltejs/kit";

export const actions: Actions = {

    create: async ({ request, fetch }) => {

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
            const response = await fetch('/api/v1/records', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: 'Failed to create record' };
            }

            } catch (error) {
                if (error instanceof Response) {
                    throw error;
                }
            return { error: 'Error during record creation' };
        }
    },

    delete: async ({ request, fetch }) => {

        const formData = await request.formData();
        const recordId = formData.get('recordId');

        if (!recordId) {
            return { error: 'Record ID is required' };
        }

        try {
            const response = await fetch(`/api/v1/records/${recordId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                return { error: 'Failed to delete record' };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during record deletion' };
        }
        throw redirect(303, '/records');
    },

    updateStatus: async ({ request, fetch }) => {

        const formData = await request.formData();
        const recordId = formData.get('recordId');
        const newStatus = formData.get('status');

        if (!recordId || !newStatus) {
            return { error: 'Record ID and status are required' };
        }

        try {
            const response = await fetch(`/api/v1/records/${recordId}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (!response.ok) {
                return { error: 'Failed to update status' };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during status update' };
        }
        throw redirect(303, '/records');
    },

    extendRecord: async ({ request, fetch }) => {

        const formData = await request.formData();
        const recordId = formData.get('recordId');
        const additionalInput = formData.get('additionalInput');

        if (!recordId || !additionalInput) {
            return { error: 'Record ID and text are required' };
        }

        try {
            const response = await fetch(`/api/v1/records/${recordId}/append`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ additionalInput: additionalInput.toString() })
            });

            if (!response.ok) {
                return { error: 'Failed to append text' };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during text append' };
        }
        throw redirect(303, '/records');
    },

    processAI: async ({ request, fetch }) => {

        const formData = await request.formData();
        const recordId = formData.get('recordId');

        if (!recordId) {
            return { error: 'Record ID is required' };
        }

        try {
            const response = await fetch(`/api/v1/records/${recordId}/process`, {
                method: 'POST',
            });

            if (!response.ok) {
                return { error: 'Failed to process with AI' };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during AI processing' };
        }
        throw redirect(303, '/records');
    }
};

export const load: PageServerLoad = async ({ params, fetch }) => {

     try {
        const recordResponse = await fetch(`/api/v1/records/${params.id}`)

        if (!recordResponse.ok) {
            throw error(404, 'Record not found');
        }

        const record = await recordResponse.json();
        return { record };

    } catch (e) {
        console.log("❌ Error loading data:", e);
        throw error(500, 'Failed to load record details');
    };
};
