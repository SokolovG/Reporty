import type {Record, CreateRecordRequest} from  '../types/record'
import {API_BASE_URL} from '$lib/config'

export async function createRecord(newRecord:CreateRecordRequest): Promise<Record> {
    const response = await fetch(`${API_BASE_URL}/records`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newRecord)
    });
    return response.json();
}

export async function getRecord(record_id: number):Promise<Record>{
    const response = await fetch(`${API_BASE_URL}/records/${record_id}`);
    return response.json();
}

export async function getRecords() : Promise<Record>{
    const response = await fetch(`${API_BASE_URL}/records`);
    return response.json();
}
