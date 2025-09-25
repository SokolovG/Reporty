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
