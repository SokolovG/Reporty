import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types"

export const load: PageServerLoad = async ({fetch}) => {
    try {
        const providersResponse = await fetch('/ai-preferences/providers');

        if (!providersResponse.ok) {
            return { providers: [] };
        }

        const providersJson = await providersResponse.json();

        if (!providersJson.success) {
            return { error: 'Error during getting AI providers' };
        }

        const providers = providersJson.data;

        return {
            providers: providers
        };

    } catch (error) {
        if (error instanceof Response) {
            throw error;
        }
        return { error: 'Error during getting AI providers' };
    }
}

export const actions: Actions = {
    updateProvider: async ({ request, fetch }) => {
        const formData = await request.formData();
        const providerId = formData.get("providerId");
        const basePrompt = formData.get("basePrompt");
        const modelName = formData.get("modelName");
        const apiKey = formData.get("apiKey")
        const isActive = formData.get("isActive") === "on";

        const data = {
            basePrompt: basePrompt?.toString(),
            modelName: modelName?.toString(),
            isActive: isActive,
            apiKey: apiKey?.toString(),
        };

        try {
            const response = await fetch(`/ai-preferences/providers/${providerId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                return { error: "Failed to update AI provider" };
            }

            const responseData = await response.json();
            if (!responseData.success) {
                return { error: "Failed to update AI provider" };
            }

        } catch (error) {
            if (error instanceof Response) {
                throw error;
            }
            return { error: 'Error during AI provider update' };
        }

        throw redirect(303, "/profile/ai-providers");
    }
}
