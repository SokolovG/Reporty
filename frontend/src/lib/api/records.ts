import type {Record, CreateRecordRequest} from  '../types/record'

export async function createRecord(newRecord:CreateRecordRequest): Promise<Record> {
    const response = await fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newRecord)
    });
    return response.json();
}

export async function getRecord(record_id: number):Promise<Record>{
    const response = await  fetch('/${record_id}', {
        method: 'GET',
    });
    return response.json()
}
