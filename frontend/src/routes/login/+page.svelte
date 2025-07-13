<script lang="ts">
    import {loginUser} from "$lib/api/auth";

    let email = "";
    let password = "";
    let errorMessage= "";

    async function login(email: string, password: string) {
        const data = {
            email: email,
            password: password
        }

        try {
            await loginUser(data);
            errorMessage = '';
        }
        catch (error) {
            if (error instanceof Error) {
                errorMessage = error.message;
            } else {
                errorMessage = 'Error during login';
            }
        }
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-96 bg-white rounded-xl shadow-lg border p-10">
        <div class="text-center mb-10">
            <h1 class="text-3xl font-bold text-gray-900 mb-3">Daily Reports</h1>
            <p class="text-gray-600 text-base">Sign in to your account</p>
        </div>

        <!-- Login Form -->
        <form class="space-y-6">
            <div class="space-y-5">
                <!-- Email Field -->
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                        Email address
                    </label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        bind:value={email}
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-base"
                        placeholder="Enter your email"
                    >
                </div>

                <!-- Password Field -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                        Password
                    </label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        bind:value={password}
                        required
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 text-base"
                        placeholder="Enter your password"
                    >
                </div>
            </div>

            <!-- Submit Button -->
            <button
                type="submit"
                on:click={() => login(email, password)}
                class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-base"
            >
                Sign in
            </button>
        </form>
         {#if errorMessage}
            <div class="mt-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-red-800 text-sm">{errorMessage}</span>
                </div>
            </div>
        {/if}
        <!-- Register Link -->
        <div class="text-center mt-8">
            <p class="text-sm text-gray-600">
                Don't have an account?
                <a href="/register" class="font-medium text-blue-600 hover:text-blue-500 hover:underline ml-1">
                    Sign up here
                </a>
            </p>
        </div>
    </div>
</div>
