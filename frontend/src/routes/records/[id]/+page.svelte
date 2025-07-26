<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { STATUS_STYLES, STATUS_LABELS } from '$lib/constants.js';
    import type { Record } from '$lib/types/record';

    let record: Record | null = null;
    let loading = true;
    let error = '';

    $: recordId = parseInt($page.params.id);

    async function loadRecord() {
        try {
            loading = true;
            record = await getRecord(recordId);
            error = '';
        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = 'Failed to load record';
            }
        } finally {
            loading = false;
        }
    }

    function goBack() {
        goto('/records');
    }

    onMount(() => {
        loadRecord();
    });
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header with back button -->
    <div class="mb-6">
        <button
            on:click={goBack}
            class="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Records
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Record Details</h1>
    </div>

    {#if loading}
        <div class="flex justify-center items-center h-64">
            <div class="text-gray-500">Loading...</div>
        </div>
    {:else if error}
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
                <span class="text-red-800">{error}</span>
            </div>
        </div>
    {:else if record}
        <!-- Record Content -->
        <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
            <!-- Title and Status -->
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-gray-500">{record.title}</span>
                    <span class="px-2 py-1 text-xs rounded-full {STATUS_STYLES[record.status]}">
                        {STATUS_LABELS[record.status]}
                    </span>
                    <span class="px-2 py-1 text-xs rounded-full {record.isProcessed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}">
                        {record.isProcessed ? 'Processed' : 'Pending'}
                    </span>
                    {#if record.isApproved}
                        <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">Approved</span>
                    {/if}
                </div>

            </div>

            <!-- Main Content -->
            <div class="mb-6">
                <h3 class="text-lg font-medium text-gray-900 mb-3">Original Input</h3>
                <div class="bg-gray-50 rounded-lg p-4 text-gray-900">
                    {record.rawInput}
                </div>
            </div>

            <!-- Metadata -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Created</h4>
                    <p class="text-sm text-gray-600">
                        {new Date(record.createdAt).toLocaleString('ru-RU', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </p>
                </div>
                <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Record ID</h4>
                    <p class="text-sm text-gray-600">#{record.id}</p>
                </div>
            </div>

            <!-- Processing Status -->
            {#if record.isProcessed}
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span class="text-blue-900 font-medium">AI Processing Complete</span>
                    </div>
                    <p class="text-blue-800 mt-2">This record has been successfully processed by AI.</p>
                </div>
            {/if}

            <!-- Actions -->
            <div class="flex gap-3 pt-4 border-t border-gray-200">
                {#if record.status === 'OPEN'}
                    <button class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                        Mark as Complete
                    </button>
                {/if}
                <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Edit Record
                </button>
                {#if !record.isProcessed}
                    <button class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                        Process with AI
                    </button>
                {:else if !record.isApproved}
                    <button class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                        Approve
                    </button>
                {/if}
                <button class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
                    Delete
                </button>
            </div>
        </div>
    {/if}
</div>
