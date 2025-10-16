<!-- frontend/src/routes/reports/+page.svelte -->
<script lang="ts">
    // import type { Report } from "$lib/types/report";
    // import { Button } from "$lib";
    import { enhance } from '$app/forms';
    import { goto } from '$app/navigation';

    let { data, form } = $props();
    let reports = data.reports?.data || [];
    let isGenerating = $state(false);

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-EN', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',

        });
    }

    function getPreview(content) {
        return content.length > 150 ? content.substring(0, 150) + '...' : content;
    }
</script>

<div class="container mx-auto px-4 py-8 max-w-6xl">
    <!-- Header with actions -->
    <div class="flex items-center justify-between mb-8">
        <div>
            <h1 class="text-3xl font-bold text-gray-900">Reports</h1>
            <p class="text-gray-600 mt-1">Generated daily reports from your work records</p>
        </div>

        <!-- Generate Report Button -->
        <form method="POST" action="?/create" use:enhance={() => {
            isGenerating = true;
            return async ({ update }) => {
                await update();
                isGenerating = false;
            };
        }}>
            <button
                type="submit"
                disabled={isGenerating}
                class="bg-amber-600 hover:bg-amber-700 disabled:bg-amber-400 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
                {#if isGenerating}
                    <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                {:else}
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                    Generate Today's Report
                {/if}
            </button>
        </form>
    </div>

    <!-- Success Message -->
    {#if form?.success}
        <div class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-green-800 font-medium">{form.success}</span>
            </div>
        </div>
    {/if}

    <!-- Error Message -->
    {#if form?.error}
        <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-rose-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                <span class="text-red-800">{form.error}</span>
            </div>
        </div>
    {/if}

    <!-- Reports Grid -->
    {#if reports.length === 0}
        <div class="text-center py-16">
            <div class="max-w-md mx-auto">
                <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No reports yet</h3>
                <p class="text-gray-600 mb-6">Create your first report by clicking the button above. It will include all your recent work records.</p>
                <div class="text-sm text-gray-500">
                    💡 Tip: Complete some records first, then generate a report
                </div>
            </div>
        </div>
    {:else}
        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {#each reports as report}
                <!-- svelte-ignore a11y_click_events_have_key_events -->
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <div class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer"
                    onclick={() => goto(`/reports/${report.id}`)}>


                    <div class="p-6 pb-4">
                        <div class="flex items-center justify-between mb-3">
                            <div class="flex items-center gap-2">
                <div class="w-3 h-3 bg-amber-500 rounded-full"></div>
                                <span class="text-sm font-medium text-gray-900">Report #{report.id}</span>
                            </div>
                            <span class="px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full">
                                {report.entriesCount} records
                            </span>
                        </div>

                        <h3 class="text-lg font-semibold text-gray-900 mb-1">
                            {formatDate(report.reportDate)}
                        </h3>

                        <p class="text-sm text-gray-500">
                            Generated {formatDate(report.generatedAt)}
                        </p>
                    </div>

                    <!-- Content Preview -->
                    <div class="px-6 pb-4">
                        <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-amber-400">
                            <p class="text-sm text-gray-700 leading-relaxed">
                                {getPreview(report.content)}
                            </p>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="px-6 py-4 bg-gray-50 rounded-b-xl">
                        <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-500">
                                Click to view details
                            </span>
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
