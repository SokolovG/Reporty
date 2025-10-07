export interface User {
    id: number
    name: string
    email: string
    display_name?: string | null
    department?: string | null
    position?: string | null
    ai_auto_process: boolean
    ai_provider_id?: number | null
    is_active: boolean
    is_verify: boolean
}
