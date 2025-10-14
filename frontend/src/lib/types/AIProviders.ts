export interface AIProvider {
    id: number
    name: string
    isActive: boolean
    modelName?: string
    basePrompt?: string
    requiresApiKey?: boolean
}

export interface AIPreferences {
    aiAutoProcess: boolean
    aiProviderId?: number | null
}

export interface AIPreferencesUpdateRequest {
    aiAutoProcess?: boolean
    aiProviderId?: number | null
}
