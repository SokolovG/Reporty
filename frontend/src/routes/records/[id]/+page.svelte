<script lang="ts">
    import { goto } from '$app/navigation';
    import type { Record } from '$lib/types/record';
    import {StatusBadge} from "$lib"

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
            <form method="POST" action="?/complete" style="display: inline;">
            {#if record.status === 'OPEN'}
                <button class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                    Mark as Complete
                </button>
            {/if}
            </form>
            <form method="POST" action="?/edit" style="display: inline;">
                <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Edit Record
                </button>
            </form>
            {#if !record.isProcessed}
                <button class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                    Process with AI
                </button>
            {:else if !record.isApproved}
                <form method="POST" action="?/approve" style="display: inline;">
                    <button class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                    Approve
                </button>
                </form>
            {/if}
             <form method="POST" action="?/delete" style="display: inline;">
                <input type="hidden" name="recordId" value={record.id} />
                 <button class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
                    Delete
                </button>
             </form>
        </div>
    </div>
</div>
