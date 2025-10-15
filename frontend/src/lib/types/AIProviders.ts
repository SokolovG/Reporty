export interface AIModel {
    id: number
    name: string
    providerId: number
}

export interface AIProvider {
    id: number
    name: string
    isActive: boolean
    apiKey?: string
    requiresApiKey?: boolean
    models: AIModel[]
    modelName?: string
    selectedModelId?: number
}

export interface AIPreferencesUpdateRequest {
    aiAutoProcess?: boolean
    aiProviderId?: number | null
}
