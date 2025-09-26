import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types"

export const load: PageServerLoad = async ({fetch}) => {
    try {
        const [recordsResponse, taskTypesResponse] = await Promise.all([
            fetch('/api/v1/records'),
            fetch('/api/v1/settings/task-types')
        ]);

        if (!recordsResponse.ok || !taskTypesResponse.ok) {
            return { records: [], taskTypes: [] };
        }

        const task_types_json = await taskTypesResponse.json();
        const records_json = await recordsResponse.json();

        if (!task_types_json.success) {
            return { error: 'Error during getting task types' };
        }

        if (!records_json.success) {
            return { error: 'Error during getting records' };
        }

        const taskTypes = task_types_json.data
        const records = records_json.data

        return {
            taskTypes: taskTypes,
            records: records
        }

    } catch (error) {
        if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during getting task types' };
    }

}

export const actions: Actions = {

    updateTaskType: async ({ request, fetch }) => {
        const formData = await request.formData()
        const title = formData.get("title")
        const color = formData.get("color")
        const isActive = formData.get("isActive")

        const data = {
            title: title.toString(),
            color: color?.toString()
            // isActive: isActive.
        };
        try {
            const response = await fetch("/task-types", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: "Failed to update task type" }
            }
            const responseData = await response.json()
            if (!responseData.status) {
                return { error: "Failed to update task type" }
            }

        } catch (error) {
            if (error instanceof Response) {
                    throw error;
                }
            return { error: 'Error during task type updation' };
        }
        throw redirect(303, "/profile")

    },

    addTaskType: async({ request, fetch }) => {
        const formData = await request.formData()
        const title = formData.get("title")
        const color = formData.get("color")


        const data = {
            title: title.toString(),
            color: color?.toString()
        };

        try {
            const response = await fetch("/task-types", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: "Failed to create task type" }
            }
            const responseData = await response.json()
            if (!responseData.status) {
                return { error: "Failed to create task type" }
            }

        } catch (error) {
            if (error instanceof Response) {
                    throw error;
                }
            return { error: 'Error during task type creation' };
        }
        throw redirect(303, "/profile")

    },
    removeTaskType: async({ request, fetch }) => {
        const formData = await request.formData()
        const taskTypeId = formData.get("taskTypeId")

        try {
            const response = await fetch(`/task-types/${taskTypeId}`, {
                method: "DELETE",
            });
            if (!response.ok) {
                return { error: 'Failed to delete record' };
            }
            const responseData = await response.json()
            if (!responseData.status) {
                return { error: 'Failed to delete record' };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during task type deletion' };
        }
        throw redirect(303, "/profile")

    },
    updateUserInfo: async ({ fetch }) => {

    },

    updateAISettings: async ({ fetch }) => {

    },

    logout: async ({ fetch }) => {

    },

    login: async ({ fetch }) => {

    }

}
