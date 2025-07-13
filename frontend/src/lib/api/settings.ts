import type {TaskType} from "$lib/types/settings";
import apiClient from "$lib/api/client";

export async function getTaskTypes(): Promise<TaskType[]> {
    try{
        const response = await apiClient.get('/v1/settings/task-types');
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.log(error);
        throw new Error("Unexpected error");
    }
}
