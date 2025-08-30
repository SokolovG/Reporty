<script lang="ts">
    import type {Record} from "$lib/types/record";
    import type {TaskType} from "$lib/types/settings";
    import { goto } from '$app/navigation';
    import {StatusBadge, Button} from "$lib";

    let { data, form } = $props();

    let records: Record[] = data.records;
    let taskTypes: TaskType[] = data.taskTypes;

</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900 text-center">Records</h1>
    </div>

    <!-- Quick Add Form -->
    <div class="mb-6">
        <form method="POST" action="?/create" class="space-y-3">
            <div class="flex gap-3">
                <input
                    name="title"
                    placeholder="Title"
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
                <select
                    name="taskType"
                    class="w-40 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                >
                    <option value="">Select type</option>
                    {#each taskTypes as taskType}
                        <option value={taskType.title}>{taskType.title}</option>
                    {/each}
                </select>
            </div>
            <div class="flex gap-3">
                <input
                    name="rawInput"
                    placeholder="What did you work on? (Enter to save)"
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
                <button
                    type="submit"
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Add
                </button>
            </div>
        </form>

        <!-- Error Message -->
        {#if form?.error}
            <div class="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-red-800 text-sm">{form.error}</span>
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
                            <StatusBadge status={record.status}/>
                            <StatusBadge variant={record.isProcessed ? 'success' : 'warning'}>
                                {record.isProcessed ? 'Processed' : 'Pending'}
                            </StatusBadge>
                        </div>

                        <div class="flex items-center gap-1">
                            <button
                                class="p-1 text-gray-400 hover:text-blue-600 rounded"
                                aria-label="Edit record"
                                onclick={() => goto(`/records/${record.id}`)}
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            </button>

                            <!-- Delete Form -->
                            <form method="POST" action="/records/{record.id}?/delete" style="display: inline;">
                                <input type="hidden" name="recordId" value={record.id} />
                                <button
                                    type="submit"
                                    class="p-1 text-gray-400 hover:text-red-600 rounded"
                                    aria-label="Delete record"
                                >
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="text-gray-900 mb-3">
                        {record.rawInput}
                    </div>

                    <!-- Quick Add Section -->
                    <div class="mt-3 pt-3 border-t border-gray-100 mb-4">
                            <!-- Quick Add Form -->
                            <form
                                method="POST"
                                action="/records/{record.id}?/extendRecord"
                                class="flex gap-2"
                            >
                                <input type="hidden" name="recordId" value={record.id} />
                                <input
                                    name="additionalInput"
                                    placeholder="Add follow-up note..."
                                    class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                    required
                                />
                                <Button text="Add" variant="primary"></Button>
                            </form>
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
                        <span class="ml-1">
                            {new Date(record.createdAt).toLocaleString('ru-RU', {
                                year: 'numeric',
                                month: '2-digit',
                                day: '2-digit',
                                hour: '2-digit',
                                minute: '2-digit'
                            })}
                        </span>

                        <div class="flex gap-3">
                            {#if record.status === 'OPEN'}
                                <form method="POST" action="/records/{record.id}?/updateStatus" style="display: inline;">
                                    <input type="hidden" name="recordId" value={record.id} />
                                    <input type="hidden" name="newStatus" value="CLOSED" />
                                    <button type="submit" class="text-green-600 hover:text-green-700 hover:underline">
                                        ✓ Complete
                                    </button>
                                </form>
                            {/if}

                            {#if !record.isProcessed}
                                <form method="POST" action="/records/{record.id}?/processAI" style="display: inline;">
                                    <input type="hidden" name="recordId" value={record.id} />
                                    <button type="submit" class="text-blue-600 hover:underline">Process</button>
                                </form>
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
