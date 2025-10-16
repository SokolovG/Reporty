<script>
  let { data } = $props();
  const name = data.user?.displayName || data.user?.name || "Guest"
</script>

<div class="bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
  <div class="container mx-auto px-4 py-8">
    <section class="text-center mb-12">
      <!-- Welcome Message with beautiful styling -->
      <div class="mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
          <span class="inline-block animate-pulse">👋</span>
          <span class="bg-gradient-to-r from-amber-700 to-orange-700 bg-clip-text text-transparent">
            Nice to see you, {name}!
          </span>
        </h1>
      </div>

      <!-- Main Title with enhanced styling -->
      <div class="mb-12">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Welcome to
        </h2>
        <h2 class="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-amber-700 via-orange-700 to-red-600 bg-clip-text text-transparent mb-6">
          Reporty
        </h2>
        <p class="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Your powerful reporting platform for creating, managing, and analyzing data with ease
        </p>
      </div>

      <!-- Enhanced Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16">
        <a
          href="/records"
          class="group bg-gradient-to-r from-amber-600 to-orange-600 text-white px-8 py-4 rounded-xl hover:from-amber-700 hover:to-orange-700 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 min-w-[200px]"
        >
          <span class="flex items-center justify-center gap-2">
            <svg class="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Create Record
          </span>
        </a>

        <a
          href="/reports"
          class="group bg-white text-gray-700 px-8 py-4 rounded-xl border-2 border-gray-200 hover:border-amber-300 hover:bg-amber-50 transition-all duration-300 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 min-w-[200px]"
        >
          <span class="flex items-center justify-center gap-2">
            <svg class="w-5 h-5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            View Reports
          </span>
        </a>
      </div>
      </section>
  </div>
</div>
