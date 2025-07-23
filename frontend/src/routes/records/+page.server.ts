import type { Actions, PageServerLoad } from "./$types";

export const actions: Actions = {
    create: async ({ request }) => {

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
