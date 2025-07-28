<script lang="ts">
    import { enhance } from '$app/forms';
    import type { PageData, ActionData } from './$types';

    let { data, form }: { data: PageData, form: ActionData } = $props();
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-96 bg-white rounded-xl shadow-lg border p-10">
        <div class="text-center mb-10">
            <h1 class="text-3xl font-bold text-gray-900 mb-3">Daily Reports</h1>
            <p class="text-gray-600 text-base">Sign in to your account</p>
        </div>

        <form method="POST" action="?/login" use:enhance class="space-y-6">
            <input
                name="email"
                type="email"
                placeholder="Enter your email"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg"
                required
            />

            <input
                name="password"
                type="password"
                placeholder="Enter your password"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg"
                required
            />

            <button
                type="submit"
                class="w-full py-3 bg-blue-600 text-white rounded-lg"
            >
                Sign in
            </button>
        </form>

        {#if form?.error}
            <div class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <span class="text-red-800">{form.error}</span>
            </div>
        {/if}
    </div>
</div>
