import type { Actions, PageServerLoad } from "./$types";
import { redirect } from "@sveltejs/kit";
import {createRecord} from "$lib/server/records";


export const actions: Actions = {
    create: async ({ request, fetch }) => {
        const formData = await request.formData();
        const result = await createRecord(formData, fetch);

        if (result.error) return result;
        throw redirect(303, '/records');
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

    appendText: async ({ request, fetch }) => {

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
export const load: PageServerLoad = async ({ fetch }) => {

    try {
        const [recordsResponse, taskTypesResponse] = await Promise.all([
            fetch('/api/v1/records'),
            fetch('/api/v1/settings/task-types')
        ]);

        if (!recordsResponse.ok || !taskTypesResponse.ok) {
            return { records: [], taskTypes: [] };
        }

        const records = await recordsResponse.json();
        const taskTypes = await taskTypesResponse.json();

        return { records, taskTypes };
    } catch (error) {
        // If it's a redirect, re-throw it
        if (error instanceof Response) {
            throw error;
        }
        return { records: [], taskTypes: [] };
    }
};
