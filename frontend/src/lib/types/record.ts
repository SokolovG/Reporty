export interface Record {
    id: number,
    date: string,
    content: string
}

export interface CreateRecordRequest {
    content: string
}
