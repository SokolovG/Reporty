export interface AIModel {
    id: number
    name: string
    providerId: number
}

export interface AIProvider {
    id: number
    name: string
    isActive: boolean
    basePrompt?: string
    apiKey?: string
    requiresApiKey?: boolean
    modlels: []

}

export interface AIPreferencesUpdateRequest {
    aiAutoProcess?: boolean
    aiProviderId?: number | null
}
