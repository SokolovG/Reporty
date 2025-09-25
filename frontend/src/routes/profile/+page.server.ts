import type { PageServerLoad } from "../$types"

export const load: PageServerLoad = async ({fetch}) => {
    try {
        const taskTypesResponse = await fetch("api/v1/settings/task-types", {
            method: "GET",
            credentials: 'include'
        });
        if (!taskTypesResponse.ok) {
            return { error: 'Error during getting task types' };
            }


        const taskTypesData = await taskTypesResponse.json();
        console.log("YA")
        console.log(taskTypesData)
        if (!taskTypesData.success) {
            return { error: 'Error during getting task types' };
        }

        return {
            taskTypes: taskTypesData.data
        }

    } catch (error) {
        if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during getting task types' };
    }

}
