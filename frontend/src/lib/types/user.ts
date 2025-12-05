export interface User {
    id: number
    name: string
    email: string
    displayName?: string | null
    department?: string | null
    position?: string | null
    aiAutoProcess: boolean
    aiProviderId?: number | null
    isActive: boolean
    isVerify: boolean
    aiModelId: number | null
    customPrompt: string | null
}
