<script lang="ts">
    import {
        getRecords,
        deleteRecord,
        updateStatus,
        appendToRecord, getRecord, editRecord
    } from "$lib/api/records";
    import { STATUS_STYLES, STATUS_LABELS } from '$lib/constants.js';
    import type {Record} from "$lib/types/record";
    import type {TaskType} from "$lib/types/settings";
    import { onMount } from 'svelte';
    import {getTaskTypes} from "$lib/api/settings";
    import { goto } from '$app/navigation';

    let records: Record[] = [];
    let newRecordText = "";
    let newRecordTitle = "";
    let newRecordTaskType = "";
    let errorMessage = "";
    let taskTypes: TaskType[] = [];
    let showQuickAdd: { [key: number]: boolean } = {};
    let quickAddText: { [key: number]: string } = {};

    async function loadRecords() {
        records = await getRecords();
    }

    async function handleTaskTypes() {
        taskTypes = await getTaskTypes();
    }

    async function handleDeleteRecord(recordId: number) {
        try {
            await deleteRecord(recordId);
            errorMessage = '';
            await loadRecords();
        }
        catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message;
            } else {
                errorMessage = 'Error during record delete';
            }
        }
    }

    async function handleUpdateStatus(recordId: number, newStatus: string) {
        try {
            await updateStatus(recordId, newStatus);
            errorMessage = '';
            await loadRecords();
        }
        catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message;
            } else {
                errorMessage = 'Error during record delete';
            }
        }
    }

    function toggleQuickAdd(recordId: number) {
        showQuickAdd[recordId] = !showQuickAdd[recordId];
    }
    function cancelQuickAdd(recordId: number) {
        showQuickAdd[recordId] = false;
    }
    async function saveQuickAdd(recordId: number) {
        const text = quickAddText[recordId];
        try {
            const data = {
                additionalInput: text
            }
            await appendToRecord(recordId, data);
            errorMessage = '';
            const updatedRecord = await getRecord(recordId);
            const index = records.findIndex(r => r.id === recordId);
            if (index !== -1) {
                records[index] = updatedRecord;
                records = records;
            }
        }
        catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message;
            } else {
                errorMessage = 'Error during record delete';
            }
        }
        quickAddText[recordId] = "";
        showQuickAdd[recordId] = false;
    }

    async function handleEditRecord(recordId: number) {
        try {
            await getRecord(recordId);
            errorMessage = '';
        }
        catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message;
            } else {
                errorMessage = 'Error during record delete';
            }
        }
    }

    function handleQuickAddKeydown(event: KeyboardEvent, recordId: number) {
        if (event.key === 'Enter') {
            saveQuickAdd(recordId);
        }
}
    onMount(async () => {
        await handleTaskTypes();
        await loadRecords();
    });
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Records</h1>
    </div>

    <!-- Quick Add -->
    <div class="mb-6">
        <div class="flex gap-3 mb-2">
            <input
                bind:value={newRecordTitle}
                placeholder="Title"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <select
                bind:value={newRecordTaskType}
                class="w-40 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
                {#each taskTypes as taskType}
                    <option value={taskType.title}>{taskType.title}</option>
                {/each}
            </select>
        </div>
        <div class="flex gap-3">
            <input
                bind:value={newRecordText}
                placeholder="What did you work on? (Ctrl/CMD +Enter to save)"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <form method="POST" action="?/create">
                <input
                    name="title"
                    placeholder="Title"
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                    required
                />

                <input
                    name="rawInput"
                    placeholder="What did you work on?"
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                    required
                />

                <select
                    name="taskType"
                    class="w-40 px-3 py-2 border border-gray-300 rounded-lg"
                >
                    <option value="">Select type</option>
                    {#each taskTypes as taskType}
                        <option value={taskType.title}>{taskType.title}</option>
                    {/each}
                </select>

                <button
                    type="submit"
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
                >
                    Add
                </button>
            </form>
            <button
                on:click={loadRecords}
                class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
            >
                Refresh
            </button>
        </div>
        {#if errorMessage}
            <div class="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-red-800 text-sm">{errorMessage}</span>
                </div>
            </div>
        {/if}
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

                        <div class="flex items-center gap-1">
                            <button class="p-1 text-gray-400 hover:text-blue-600 rounded" aria-label="Edit record" on:click={() => goto(`/records/${record.id}`)}>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            </button>
                            <button class="p-1 text-gray-400 hover:text-red-600 rounded" aria-label="Delete record" on:click = {() => handleDeleteRecord(record.id)}>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </button>
                        </div>
                    </div>
                        <div class="mt-3 pt-3 border-t border-gray-100">
                            {#if !showQuickAdd[record.id]}
                                <button
                                    class="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1 bg-blue-50 font-medium px-3 py-2 mb-4"
                                    on:click={() => toggleQuickAdd(record.id)}>

                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                    </svg>
                                    Quick add follow-up
                                </button>
                            {:else}
                                <!-- Inline форма -->
                                <div class="space-y-2">
                                    <input
                                        bind:value={quickAddText[record.id]}
                                        placeholder="Add follow-up note..."
                                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        on:keydown={(e) => handleQuickAddKeydown(e, record.id)}
                                    />
                                    <div class="flex gap-2">
                                        <button
                                            class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300"
                                            on:click={() => saveQuickAdd(record.id)}
                                            disabled={!quickAddText[record.id]?.trim()}
                                        >
                                            Add
                                        </button>
                                        <button
                                            class="px-3 py-1 text-sm text-gray-600 hover:text-gray-700"
                                            on:click={() => cancelQuickAdd(record.id)}>
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            {/if}
                        </div>
                                    <!-- Content -->
                    <div class="text-gray-900 mb-3">
                        {record.rawInput}
                    </div>

                    {#if record.isProcessed}
                        <div class="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
                            <div class="text-sm text-blue-900">
                                ✨ AI has processed this record successfully.
                            </div>
                        </div>
                    {/if}

                    <!-- Footer -->
                    <div class="flex items-center justify-between text-sm text-gray-500">
                        <span>
                            {new Date(record.createdAt).toLocaleString('eu-EU', {
                                year: 'numeric',
                                month: '2-digit',
                                day: '2-digit',
                                hour: '2-digit',
                                minute: '2-digit'
                            })}
                        </span>

                        <div class="flex gap-3">
                            {#if record.status === 'OPEN'}
                            <button
                                class="text-green-600 hover:text-green-700 hover:underline"
                                on:click={() => handleUpdateStatus(record.id, 'CLOSED')}
                            >
                                ✓ Complete
                            </button>
                        {/if}
                            {#if !record.isProcessed}
                                <button class="text-blue-600 hover:underline">Process</button>
                            {:else if !record.isApproved}
                                <button class="text-green-600 hover:underline">Approve</button>
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
