<script lang="ts">
  let { user } = $props();
</script>

<header class="w-full bg-white border-b border-gray-200 shadow-sm">
  <nav class="container mx-auto px-4 py-4">
    <div class="flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center space-x-2">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">R</span>
        </div>
        <span class="text-xl font-bold text-gray-900"><a href="/">Reporty</a></span>
      </div>

      <!-- Navigation -->
      <div class="hidden md:flex items-center space-x-6">
        <a href="/" class="text-gray-600 hover:text-blue-600 transition-colors">
          Home
        </a>
        <a href="/records" class="text-gray-600 hover:text-blue-600 transition-colors">
          Records
        </a>
        <a href="/reports" class="text-gray-600 hover:text-blue-600 transition-colors">
          Reports
        </a>
        <a href="/settings" class="text-gray-600 hover:text-blue-600 transition-colors">
          Settings
        </a>
      </div>
    </div>
  </nav>
</header>
