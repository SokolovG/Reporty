<script lang="ts">
    import { Button } from "$lib";
    import { enhance } from '$app/forms';
    import type { AIProvider } from "$lib/types/AIProviders.js";

    let { data, form } = $props();
    let providers = data.providers || [];
    let editingProvider: AIProvider | null = $state(null);

    function toggleEdit(provider: AIProvider) {
        if (editingProvider && editingProvider.id == provider.id){
        editingProvider = null;
        } else {
            editingProvider = { ...provider };
        }
    }

    function cancelEdit() {
        editingProvider = null;
    }
</script>

<div class="bg-gradient-to-br from-blue-50 via-white to-indigo-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-6xl">
        <!-- Header -->
        <div class="mb-8">
            <div class="flex items-center gap-4 mb-4">
                <a href="/profile" class="text-blue-600 hover:text-blue-800 transition-colors" aria-label="Edit ai providers">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                </a>
                <h1 class="text-3xl font-bold text-gray-900">AI Providers Management</h1>
            </div>
            <p class="text-gray-600">Configure and manage AI providers (Admin only)</p>
        </div>

        {#if form?.error}
            <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p class="text-red-700">{form.error}</p>
            </div>
        {/if}

        <!-- Providers Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {#each providers as provider}
                <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xl font-semibold text-white">{provider.name}</h3>
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-1 text-xs rounded-full {provider.isActive ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}">
                                    {provider.isActive ? 'Active' : 'Inactive'}
                                </span>
                                <button
                                    aria-label="Edit ai providers"
                                    onclick={() => toggleEdit(provider)}
                                    class="text-white hover:text-purple-200 transition-colors"
                                >
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="p-6">
                        {#if editingProvider && editingProvider.id === provider.id}
                            <form
                                method="POST"
                                action="?/updateProvider"
                                use:enhance={() => {
                                    return async ({ update }) => {
                                        await update();
                                        editingProvider = null;
                                    };
                                }}
                                class="space-y-4"
                            >
                                <input type="hidden" name="providerId" value={provider.id} />

                                <div>
                                    <div class="block text-sm font-medium text-gray-700 mb-1">Model Name</div>
                                    <input
                                        name="modelName"
                                        bind:value={editingProvider.modelName}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        placeholder="e.g., gpt-4, claude-3"
                                    />
                                </div>

                                <div>
                                    <div class="block text-sm font-medium text-gray-700 mb-1">Base Prompt</div>
                                    <textarea
                                        name="basePrompt"
                                        bind:value={editingProvider.basePrompt}
                                        rows="4"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        placeholder="System prompt for this AI provider..."
                                    ></textarea>
                                </div>
                                {#if editingProvider.requiresApiKey}
                                    <div>
                                        <div class="block text-sm font-medium text-gray-700 mb-1">Api Key</div>
                                        <textarea
                                            name="apiKey"
                                            bind:value={editingProvider.apiKey}
                                            rows="4"
                                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                            placeholder="Api key for provider..."
                                        ></textarea>
                                    </div>
                                {/if}

                                <div class="flex items-center gap-4">
                                    <label class="flex items-center gap-2">
                                        <input
                                            type="checkbox"
                                            name="isActive"
                                            bind:checked={editingProvider.isActive}
                                            class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                        />
                                        <span class="text-sm text-gray-700">Active</span>
                                    </label>
                                </div>

                                <div class="flex gap-3 pt-4">
                                    <Button text="Save Changes" variant="primary" />
                                    <button
                                        type="button"
                                        onclick={cancelEdit}
                                        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        {:else}
                            <div class="space-y-4">
                                <div>
                                    <div class="text-sm font-medium text-gray-500">Model</div>
                                    <p class="text-gray-900">{provider.modelName || 'Not specified'}</p>
                                </div>

                                <div>
                                    <div class="text-sm font-medium text-gray-500">API Key Required</div>
                                    <p class="text-gray-900">{provider.requiresApiKey ? 'Yes' : 'No'}</p>
                                </div>

                                {#if provider.basePrompt}
                                    <div>
                                        <div class="text-sm font-medium text-gray-500">Base Prompt</div>
                                        <p class="text-gray-900 text-sm bg-gray-50 p-3 rounded-lg mt-1">
                                            {provider.basePrompt.length > 200
                                                ? provider.basePrompt.substring(0, 200) + '...'
                                                : provider.basePrompt}
                                        </p>
                                    </div>
                                {/if}
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>

        {#if providers.length === 0}
            <div class="text-center py-12">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No AI Providers</h3>
                <p class="text-gray-600">No AI providers are configured in the system.</p>
            </div>
        {/if}
    </div>
</div>
