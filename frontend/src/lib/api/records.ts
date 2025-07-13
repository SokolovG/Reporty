import type {Record, CreateRecordRequest} from  '../types/record'
import apiClient from "$lib/api/client";

export async function createRecord(newRecord:CreateRecordRequest): Promise<Record> {
    try{
        console.log(newRecord)
        const response = await apiClient.post('/v1/records', {
        body: JSON.stringify(newRecord)
    });
        return response.data();
    } catch (error) {
        console.log(error);
        throw new Error("Error during record creation");
    }
}

export async function getRecord(record_id: number):Promise<Record>{
    try {
        const response = await apiClient.get(`/v1/records/${record_id}`);
        return response.data();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }

}

export async function getRecords() : Promise<Record[]>{
    try {
        const response = await apiClient.get('/v1/records');
        return response.data();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}
