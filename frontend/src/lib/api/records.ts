import type {Record, appendRecordRequest} from '../types/record'
import {json} from "@sveltejs/kit";

export async function getRecord(recordId: number):Promise<Record>{
    try {
        console.log('Calling API:', `/v1/records/${recordId}`);
        const response = await fetch(`/v1/records/${recordId}`);
        return response.json();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }

}

export async function getRecords() : Promise<Record[]>{
    try {
        const response = await fetch('/v1/records');
        console.log(response.json())
        return response.json();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function deleteRecord(recordId: number): Promise<undefined> {
    try {
        await fetch(`/v1/records/${recordId}`);
        return
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function updateStatus(recordId: number, newStatus: string) {
    try {
        const data = {"status": newStatus}
        const response = await fetch(`/v1/records/${recordId}/status`);
        return response.json();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");
    }
}

export async function appendToRecord(recordId: number, recordData: appendRecordRequest) {
    try {
        const response = await fetch(`/v1/records/${recordId}/append`);
        return response.json();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }
}

export async function editRecord(recordId: number, newData: string):Promise<Record> {
    try {
        const response = await fetch(`/v1/records/${recordId}/`);
        return response.json();
    } catch (error) {
        console.log(error)
        throw new Error("Unexpected error");

    }
}
