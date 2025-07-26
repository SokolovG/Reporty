import type {TaskType} from "$lib/types/settings";

export async function getTaskTypes(): Promise<TaskType[]> {
    try{
        const response = await fetch('/v1/settings/task-types');
        console.log(response.json())
        return response.json();
    } catch (error) {
        console.log(error);
        throw new Error("Unexpected error");
    }
}
