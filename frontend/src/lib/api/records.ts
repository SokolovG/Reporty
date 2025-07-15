import type {Record, CreateRecordRequest, appendRecordRequest} from '../types/record'
import apiClient from "$lib/api/client";

export async function createRecord(newRecord:CreateRecordRequest): Promise<Record> {
    try{
        const response = await apiClient.post('/v1/records', newRecord);
        return response.data;
    } catch (error) {
        console.log(error);
        throw new Error("Error during record creation");
    }
}

export async function getRecord(recordId: number):Promise<Record>{
    try {
        console.log('Calling API:', `/v1/records/${recordId}`);
        const response = await apiClient.get(`/v1/records/${recordId}`);
        return response.data;
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }

}

export async function getRecords() : Promise<Record[]>{
    try {
        const response = await apiClient.get('/v1/records');
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function deleteRecord(recordId: number): Promise<undefined> {
    try {
        await apiClient.delete(`/v1/records/${recordId}`);
        return
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function updateStatus(recordId: number, newStatus: string) {
    try {
        const data = {"status": newStatus}
        const response = await apiClient.patch(`/v1/records/${recordId}/status`, data);
        return response.data;
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function appendToRecord(recordId: number, recordData: appendRecordRequest) {
    try {
        const response = await apiClient.post(`/v1/records/${recordId}/append`, recordData);
        return response.data;
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }
}

export async function editRecord(recordId: number, newData: string):Promise<Record> {
    try {
        const response = await apiClient.patch(`/v1/records/${recordId}/`, newData);
        return response.data;
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }
}
