export interface AIProvider {
    id: number
    name: string
    is_active: boolean
    model_name?: string
    base_prompt?: string
    requires_api_key?: boolean
}

export interface AIPreferences {
    ai_auto_process: boolean
    ai_provider_id?: number | null
}

export interface AIPreferencesUpdateRequest {
    ai_auto_process?: boolean
    ai_provider_id?: number | null
}
