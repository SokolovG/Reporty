<script>
  import "../app.css";
  import { Header, Footer } from "$lib";

  let { children } = $props();
</script>

<div class="app">
  <Header />
  <main>
    {@render children()}
  </main>
  <Footer />
</div>
