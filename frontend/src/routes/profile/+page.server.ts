import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types"

export const load: PageServerLoad = async ({fetch}) => {
    try {
        const [recordsResponse, taskTypesResponse, providersResponse] = await Promise.all([
            fetch('/api/v1/records'),
            fetch('/api/v1/settings/task-types'),
            fetch('api/v1/settings/ai_provider')
        ]);

        if (!recordsResponse.ok || !taskTypesResponse.ok || !providersResponse) {
            return { records: [], taskTypes: [] };
        }

        const taskTypesJson = await taskTypesResponse.json();
        const recordsJson = await recordsResponse.json();
        const providersJson = await providersResponse.json();

        if (!taskTypesJson.success) {
            return { error: 'Error during getting task types' };
        }

        if (!recordsJson.success) {
            return { error: 'Error during getting records' };
        }

        const taskTypes = taskTypesJson.data
        const records = recordsJson.data
        const providers = providersJson.data

        return {
            taskTypes: taskTypes,
            records: records,
            providers: providers
        };

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
            const response = await fetch("/api/v1/settings/task-types", {
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
            if (!responseData.success) {
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
            const response = await fetch("/api/v1/settings/task-types", {
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
            if (!responseData.success) {
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
            const response = await fetch(`/api/v1/settings/task-types/${taskTypeId}`, {
                method: "DELETE",
            });
            if (!response.ok) {
                return { error: 'Failed to delete record' };
            }
            const responseData = await response.json()
            if (!responseData.success) {
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
    updateUserInfo: async ({ request, fetch }) => {
        const formData = await request.formData();
        const display_name = formData.get("display_name");
        const department = formData.get("department");
        const position = formData.get("position");

        const data = {
            display_name: display_name?.toString() || null,
            department: department?.toString() || null,
            position: position?.toString() || null,
        };

        try {
            const response = await fetch("/api/v1/settings/user", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: "Failed to update user info" };
            }

            const responseData = await response.json();
            if (!responseData.success) {
                return { error: "Failed to update user info" };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during user info update' };
        }

        throw redirect(303, "/profile");
    },

    updateAISettings: async ({ request, fetch }) => {
        const formData = await request.formData();
        const ai_auto_process = formData.get("ai_auto_process") === "on";
        const ai_provider_id = formData.get("ai_provider_id");

        const data = {
            ai_auto_process: ai_auto_process,
            ai_provider_id: ai_provider_id ? parseInt(ai_provider_id.toString()) : null,
        };
        try {
            const response = await fetch("/api/v1/settings/ai_settings", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: "Failed to update AI settings" };
            }

            const responseData = await response.json();
            if (!responseData.success) {
                return { error: "Failed to update AI settings" };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during AI settings update' };
        }

        throw redirect(303, "/profile");
    },

    logout: async ({ fetch }) => {
        try {
            const response = await fetch("/api/v1/auth/logout", {
                method: "POST"
            });
            if (!response.ok) {
                return { error: "Failed to logout" };
            }
            throw redirect(303, '/login');

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            console.error('Logout error:', error);
            return {
                success: false,
                error: 'Unexpected error during logout'
            };
        }
    }

}
