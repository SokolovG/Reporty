export interface AIProvider {
    id: number
    name: string
    is_active: boolean
    model_name?: string
    base_prompt?: string
    requires_api_key?: boolean
}
