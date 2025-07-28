<script lang="ts">
  import "../app.css";
  import { Header, Footer } from "$lib";
  import type { LayoutData } from './$types';

  let { children, data }: { children: import('svelte').Snippet, data: LayoutData } = $props();
</script>

<div class="app">
  <Header user={data.user} />
  <main>
    {@render children()}
  </main>
  <Footer />
</div>
