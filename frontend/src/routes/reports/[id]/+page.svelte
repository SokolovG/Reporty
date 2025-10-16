<!-- frontend/src/routes/reports/[id]/+page.svelte -->
<script lang="ts">
    import { goto } from '$app/navigation';
    import type { Report } from '$lib/types/report';
    // import { Button } from "$lib";

    let { data } = $props();
    let report: Report = data.report;

    function goBack() {
        goto('/reports');
    }

    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    function formatDateTime(dateString: string): string {
        return new Date(dateString).toLocaleString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function copyToClipboard() {
        navigator.clipboard.writeText(report.content);
        // TODO: показать toast уведомление
    }

    function exportAsText() {
        const blob = new Blob([report.content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `report-${report.reportDate}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // Разбиваем контент на строки для красивого отображения
    function parseContent(content: string) {
        const lines = content.split('\n');
        const result = [];
        let currentSection = null;

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;

            if (trimmed.startsWith('Report for')) {
                result.push({ type: 'title', content: trimmed });
            } else if (trimmed.match(/^\d+\./)) {
                result.push({ type: 'task', content: trimmed });
            } else if (trimmed.startsWith('Total tasks:')) {
                result.push({ type: 'summary', content: trimmed });
            } else {
                result.push({ type: 'text', content: trimmed });
            }
        }
        return result;
    }

    $parsedContent = parseContent(report.content);
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-8">
        <button
            onclick={goBack}
            class="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6 transition-colors"
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Reports
        </button>

        <div class="flex items-start justify-between">
            <div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">
                    Daily Report
                </h1>
                <div class="flex items-center gap-4 text-sm text-gray-600">
                    <span class="flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {formatDate(report.reportDate)}
                    </span>
                    <span class="flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {report.entriesCount} records
                    </span>
                    <span class="flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Generated {formatDateTime(report.generatedAt)}
                    </span>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-3">
                <button
                    onclick={copyToClipboard}
                    class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy
                </button>

                <button
                    onclick={exportAsText}
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Export
                </button>
            </div>
        </div>
    </div>

    <!-- Report Content -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
        <!-- Header Badge -->
        <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200 rounded-t-xl">
            <div class="flex items-center gap-2">
                <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span class="font-medium text-gray-900">Report #{report.id}</span>
                <span class="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded-full">
                    {report.entriesCount} tasks completed
                </span>
            </div>
        </div>

        <!-- Content -->
        <div class="p-6">
            <div class="prose prose-gray max-w-none">
                {#each parsedContent as item}
                    {#if item.type === 'title'}
                        <h2 class="text-2xl font-bold text-gray-900 mb-6 pb-3 border-b border-gray-200">
                            {item.content}
                        </h2>
                    {:else if item.type === 'task'}
                        <div class="mb-4 p-4 bg-gray-50 rounded-lg border-l-4 border-blue-400">
                            <p class="text-gray-800 font-medium">{item.content}</p>
                        </div>
                    {:else if item.type === 'summary'}
                        <div class="mt-8 p-4 bg-green-50 rounded-lg border border-green-200">
                            <p class="text-green-800 font-semibold flex items-center gap-2">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                </svg>
                                {item.content}
                            </p>
                        </div>
                    {:else}
                        <p class="text-gray-700 mb-3 leading-relaxed">{item.content}</p>
                    {/if}
                {/each}
            </div>
        </div>

        <!-- Footer Actions -->
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-xl">
            <div class="flex items-center justify-between">
                <div class="text-sm text-gray-500">
                    Report generated on {formatDateTime(report.generatedAt)}
                </div>

                <div class="flex gap-3">
                    <button class="text-blue-600 hover:text-blue-700 text-sm font-medium">
                        Share Report
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
