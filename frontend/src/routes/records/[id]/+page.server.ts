import type { Actions, PageServerLoad } from "./$types";
import {API_BASE} from "$lib/constants";
import {error, redirect} from "@sveltejs/kit";

export const actions: Actions = {
    edit: async ({}) => {

    },
    process: async ({}) => {

    },
    approve: async ({}) => {

    },
    delete: async ({}) => {

    }
}

export const load: PageServerLoad = async ({ cookies, params }) => {
     const token = cookies.get('authToken');

     if (!token) {
        throw redirect(303, '/login');
     }

     try {
        const recordResponse = await fetch(`${API_BASE}/v1/records/${params.id}`, {
                headers: { 'Authorization': token }
            })

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
