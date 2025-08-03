<script lang="ts">
    import { goto } from '$app/navigation';
    import type { Record } from '$lib/types/record';
    import {StatusBadge, Button} from "$lib"

    let { data } = $props();

    let record: Record = data.record

    function goBack() {
        goto('/records');
    }

</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header with back button -->
    <div class="mb-6">
        <button
            onclick={goBack}
            class="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Records
        </button>
        <h1 class="text-3xl font-bold text-gray-900">Record Details</h1>
    </div>

    <!-- Record Content -->
    <div class="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <!-- Title and Status -->
        <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
                <span class="text-sm text-gray-500">{record.title}</span>
                <StatusBadge status={record.status}/>
                <span class="px-2 py-1 text-xs rounded-full {record.isProcessed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}">
                    {record.isProcessed ? 'Processed' : 'Pending'}
                </span>
                {#if record.isApproved}
                    <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">Approved</span>
                {/if}
            </div>

        </div>

        <div class="mb-6">
    <div class="flex items-center gap-2 mb-4">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900">Original Input</h3>
    </div>

    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-400 rounded-r-lg p-4 mb-6">
        <p class="text-gray-900 leading-relaxed">{record.rawInput}</p>
    </div>

    <div class="bg-white border-2 border-gray-200 rounded-lg p-4">
        <h4 class="text-sm font-medium text-gray-700 mb-3">Edit Content:</h4>

        <form method="POST" action="?/updateText" class="space-y-4">
            <input type="hidden" name="recordId" value={record.id} />

            <div class="relative">
                <textarea
                    name="rawInput"
                    class="w-full border-2 border-gray-300 rounded-lg p-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none transition-all duration-200 shadow-sm"
                    rows="4"
                    placeholder="Update your input..."
                >{record.rawInput}</textarea>

                <div class="absolute bottom-3 right-3 text-xs text-gray-400">
                    Press Ctrl+Enter to save
                </div>
            </div>

            <div class="flex gap-3 justify-end pt-2">
                <Button text="Cancel"></Button>
                <Button text="Save Changes" variant="primary" />
            </div>
        </form>
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
            <form method="POST" action="?/updateStatus" style="display: inline;">
                <input type="hidden" name="recordId" value={record.id} />
                {#if record.status === 'OPEN'}
                    <input type="hidden" name="newStatus" value="CLOSED"/>
                    <Button text="Mark as Complete" variant="success"></Button>
                {:else}
                    <input type="hidden" name="newStatus" value="OPEN"/>
                    <Button text="Reopen" variant="success"></Button>
                {/if}
            </form>
            <form method="POST" action="?/edit" style="display: inline;">
                <Button text="Edit Record" variant="primary"></Button>
            </form>
            {#if !record.isProcessed}
                <Button text="Process with AI" variant="purple"></Button>
            {:else if !record.isApproved}
                <form method="POST" action="?/approve" style="display: inline;">
                    <Button text="Approve" variant="indigo"></Button>
                </form>
            {/if}
             <form method="POST" action="?/delete" style="display: inline;">
                <input type="hidden" name="recordId" value={record.id} />
                 <Button text="Delete" variant="danger"></Button>
             </form>
        </div>
    </div>
</div>
