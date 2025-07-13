<script lang="ts">
    import {getRecords} from "$lib/api/records";
    import type {Record} from "$lib/types/record";

    let records: Record[] = [];

    async function loadRecords() {
        records = await getRecords();
    }
</script>

<div class="container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Records</h1>
        <p class="text-gray-600">Manage your daily work records and AI transformations</p>
    </div>

    <!-- Action Bar -->
    <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-6 mb-6">
        <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div class="flex flex-col sm:flex-row gap-3">
                <button
                    on:click={loadRecords}
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2"
                >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Load Records
                </button>

                <button class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Add New Record
                </button>
            </div>

            <!-- Search and Filter -->
            <div class="flex gap-3 w-full sm:w-auto">
                <input
                    type="text"
                    placeholder="Search records..."
                    class="flex-1 sm:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                />
                <select class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                    <option>All Status</option>
                    <option>Processed</option>
                    <option>Not Processed</option>
                    <option>Approved</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Records List -->
    <div class="space-y-4">
        {#if records.length === 0}
            <!-- Empty State -->
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-12 text-center">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No records found</h3>
                <p class="text-gray-600 mb-6">Click "Load Records" to fetch your data or create your first record.</p>
                <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    Create First Record
                </button>
            </div>
        {:else}
            <!-- Records Grid -->
            {#each records as record}
                <div class="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                    <div class="p-6">
                        <!-- Record Header -->
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex-1">
                                <div class="flex items-center gap-3 mb-2">
                                    <h3 class="text-lg font-semibold text-gray-900">
                                        {record.title || `Record #${record.id}`}
                                    </h3>
                                    <span class="text-sm text-gray-500">#{record.id}</span>
                                </div>

                                <!-- Status Badges -->
                                <div class="flex gap-2">
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                                        {record.is_processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
                                        {record.is_processed ? 'AI Processed' : 'Pending Processing'}
                                    </span>

                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                                        {record.is_approved ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}">
                                        {record.is_approved ? 'Approved' : 'Not Approved'}
                                    </span>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="flex items-center gap-2 ml-4">
                                <button class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                </button>

                                <button class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>

                                <button class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Record Content -->
                        <div class="space-y-4">
                            <!-- Raw Input -->
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Raw Input</label>
                                <div class="bg-gray-50 rounded-lg p-3 border">
                                    <p class="text-sm text-gray-900 whitespace-pre-wrap">{record.raw_input}</p>
                                </div>
                            </div>

                            <!-- AI Processed (if available) -->
                            {#if record.is_processed}
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">AI Processed Output</label>
                                    <div class="bg-blue-50 rounded-lg p-3 border border-blue-200">
                                        <p class="text-sm text-gray-900">
                                            <!-- Add processed_output field when available -->
                                            AI has processed this record successfully.
                                        </p>
                                    </div>
                                </div>
                            {/if}
                        </div>

                        <!-- Record Footer -->
                        <div class="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
                            <div class="flex items-center text-sm text-gray-500">
                                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                Created {new Date(record.created_at).toLocaleDateString()} at {new Date(record.created_at).toLocaleTimeString()}
                            </div>

                            <div class="flex gap-2">
                                {#if !record.is_processed}
                                    <button class="text-blue-600 hover:text-blue-700 text-sm font-medium">
                                        Process with AI
                                    </button>
                                {:else if !record.is_approved}
                                    <button class="text-green-600 hover:text-green-700 text-sm font-medium">
                                        Approve
                                    </button>
                                {/if}

                                <button class="text-gray-600 hover:text-gray-700 text-sm font-medium">
                                    View Details
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
        {/if}
    </div>

    <!-- Pagination (if needed) -->
    {#if records.length > 0}
        <div class="mt-8 flex items-center justify-between">
            <p class="text-sm text-gray-700">
                Showing <span class="font-medium">1</span> to <span class="font-medium">{records.length}</span> of <span class="font-medium">{records.length}</span> results
            </p>

            <div class="flex gap-2">
                <button class="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50" disabled>
                    Previous
                </button>
                <button class="px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    1
                </button>
                <button class="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50" disabled>
                    Next
                </button>
            </div>
        </div>
    {/if}
</div>
