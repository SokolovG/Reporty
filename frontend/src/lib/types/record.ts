export interface Record {
    id: BigInteger,
    date: Date,
    content: string
}

export interface CreateRecordRequest {
    content: string
}
