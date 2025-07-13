export interface Record {
    id: number,
    created_at: string,
    aiProcessed: boolean
    externalTaskId: boolean
    finalDescription: boolean
    isApproved: boolean
    isProcessed: boolean
    rawInput: string
    title: string
}

export interface CreateRecordRequest {
    content: string
    title: string
}
