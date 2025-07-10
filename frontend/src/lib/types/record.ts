export interface Record {
    id: number,
    created_at: string,
    ai_processed: boolean
    external_task_id: boolean
    final_description: boolean
    is_approved: boolean
    is_processed: boolean
    raw_input: string
    title: string
    user_id: number
}

export interface CreateRecordRequest {
    content: string
}
