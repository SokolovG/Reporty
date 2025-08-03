<script lang="ts">
    import type {Report} from "$lib/types/report";

    let { data } = $props();
    let reports: Report[] = data.reports;

</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- Header -->
    <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900 text-center">Reports</h1>
    </div>
    <!-- Reports List -->
    {#if reports.length === 0}
        <div class="text-center py-12 text-gray-500">
            <p>No reports yet. Complete tasks and generate your first one above! 👆</p>
        </div>
    {:else}
        <div class="space-y-3">
            {#each reports as report}
                <h1>Report {report.id}</h1>
            {/each}
        </div>
    {/if}
</div>
