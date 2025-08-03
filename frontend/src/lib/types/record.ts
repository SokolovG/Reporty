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
