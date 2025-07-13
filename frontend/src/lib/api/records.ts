import type {Record, CreateRecordRequest} from  '../types/record'
import apiClient from "$lib/api/client";

export async function createRecord(newRecord:CreateRecordRequest): Promise<Record> {
    try{
        console.log(newRecord)
        const response = await apiClient.post('/records', {
        body: JSON.stringify(newRecord)
    });
    if (!response.status) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.data();
    } catch (error) {
        console.log(error);
        throw new Error("Error during record creation");
    }
}

export async function getRecord(record_id: number):Promise<Record>{
    try {
        const response = await apiClient.get(`/records/${record_id}`);
        return response.data();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }

}

export async function getRecords() : Promise<Record[]>{
    try {
        const response = await apiClient.get('/records');
        return response.data();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}
