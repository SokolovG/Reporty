export interface Record {
    id: number,
    createdAt: string,
    aiProcessed: boolean
    externalTaskId: boolean
    finalDescription: boolean
    isApproved: boolean
    isProcessed: boolean
    rawInput: string
    title: string
    status: string
}

export interface CreateRecordRequest {
    rawInput: string
    title: string
}

export interface appendRecordRequest {
    additionalInput: string
}
