<script lang="ts">
    import { getRecords, createRecord } from "$lib/api/records";
    import type {Record} from "$lib/types/record";

    let records: Record[] = [];
    let newRecordText = "";

    async function loadRecords() {
        records = await getRecords();
    }

    async function handleCreateRecord() {
        if (!newRecordText.trim()) return;
        const data = { content: newRecordText };
        await createRecord(data);
        newRecordText = "";
        await loadRecords();
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
            handleCreateRecord();
        }
    }
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Records</h1>
    </div>

    <!-- Quick Add -->
    <div class="mb-6">
        <div class="flex gap-3">
            <input
                bind:value={newRecordText}
                on:keydown={handleKeydown}
                placeholder="What did you work on? (Ctrl+Enter to save)"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <button
                on:click={handleCreateRecord}
                disabled={!newRecordText.trim()}
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
            >
                Add
            </button>
            <button
                on:click={loadRecords}
                class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
            >
                Refresh
            </button>
        </div>
    </div>

    <!-- Records List -->
    {#if records.length === 0}
        <div class="text-center py-12 text-gray-500">
            <p>No records yet. Add your first one above! 👆</p>
        </div>
    {:else}
        <div class="space-y-3">
            {#each records as record}
                <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                    <!-- Header -->
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <span class="text-sm text-gray-500">#{record.id}</span>
                            <span class="px-2 py-1 text-xs rounded-full {record.is_processed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}">
                                {record.is_processed ? 'Processed' : 'Pending'}
                            </span>
                            {#if record.is_approved}
                                <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">Approved</span>
                            {/if}
                        </div>

                        <div class="flex items-center gap-1">
                            <button class="p-1 text-gray-400 hover:text-blue-600 rounded" aria-label="Edit">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            </button>
                            <button class="p-1 text-gray-400 hover:text-red-600 rounded" aria-label="Delete">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="text-gray-900 mb-3">
                        {record.raw_input}
                    </div>

                    {#if record.is_processed}
                        <div class="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
                            <div class="text-sm text-blue-900">
                                ✨ AI has processed this record successfully.
                            </div>
                        </div>
                    {/if}

                    <!-- Footer -->
                    <div class="flex items-center justify-between text-sm text-gray-500">
                        <span>
                            {new Date(record.created_at).toLocaleDateString()}
                        </span>

                        <div class="flex gap-3">
                            {#if !record.is_processed}
                                <button class="text-blue-600 hover:underline">Process</button>
                            {:else if !record.is_approved}
                                <button class="text-green-600 hover:underline">Approve</button>
                            {/if}
                            <button class="text-gray-600 hover:underline">Details</button>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
