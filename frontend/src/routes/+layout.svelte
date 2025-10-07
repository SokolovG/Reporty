<script lang="ts">
  import "../app.css";
  import { Header, Footer, setUser } from "$lib";
  import type { LayoutData } from './$types';
  import { setContext, onMount } from 'svelte';

  let { children, data }: { children: import('svelte').Snippet, data: LayoutData } = $props();

  setContext("user", data.user);

  // Initialize user store
  onMount(() => {
    if (data.user) {
      setUser(data.user);
    }
  });
</script>

<div class="app">
  <Header user={data.user} />
  <main>
    {@render children()}
  </main>
  <Footer />
</div>
