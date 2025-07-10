<script lang="ts">
    import {getRecords} from "$lib/api/records";
    import type {Record} from "$lib/types/record";

    let records: Record[] = [];

    async function loadRecords() {
        records = await getRecords();
    }

</script>

<main>
    <h1>Welcome to Reporty</h1>
    <div>
        <button on:click={loadRecords}>Load records</button>
        {#each records as record}
            <p>record.title</p>
        {/each}
    </div>
</main>
