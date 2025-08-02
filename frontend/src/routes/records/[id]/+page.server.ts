import type { Actions, PageServerLoad } from "./$types";
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
