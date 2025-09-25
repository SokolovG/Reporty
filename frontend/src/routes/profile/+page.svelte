<script lang="ts">
    import { getContext, setContext } from 'svelte';
    import { Button } from "$lib";
    const userContext = getContext("user")
    let user = { ...userContext }
    let { data }: { data: PageData } = $props();
    let taskTypes = data.taskTypes;
    let records = data.records;

    console.log(records)

    const totalTasks = records?.length || 0
    const openTasks = records?.filter(task => task.status === "OPEN")?.length || 0
    const closedTasks = records?.filter(task => task.status === "CLOSED")?.length || 0

    let aiProviders = [
        { id: 1, name: "OpenAI GPT-4", is_active: true },
        { id: 2, name: "Claude", is_active: true },
        { id: 3, name: "Local LLM", is_active: false }
    ];

    let isEditing = false;
    let editForm = { ...user };
    let newTaskType = { title: "", color: "#3B82F6" };
    let showAddTaskType = false;

    function toggleEdit() {
        isEditing = !isEditing;
        if (isEditing) {
            editForm = { ...user };
        }
    }

    function saveProfile() {
        user = { ...editForm };
        isEditing = false;
        setContext("user", user);
    }

    function addTaskType() {
        if (newTaskType.title.trim()) {
            taskTypes = [...taskTypes, { ...newTaskType }];
            newTaskType = { title: "", color: "#3B82F6" };
            showAddTaskType = false;
        }
    }

    function removeTaskType(index: number) {
        taskTypes = taskTypes.filter((_, i) => i !== index);
    }
</script>

<div class="bg-gradient-to-br from-blue-50 via-white to-indigo-50 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 text-center mb-2">Profile Settings</h1>
            <p class="text-gray-600 text-center">Manage your account and preferences</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Main Profile Section -->
            <div class="lg:col-span-2 space-y-6">
                <!-- Personal Information Card -->
                <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
                        <div class="flex items-center justify-between">
                            <h2 class="text-xl font-semibold text-white flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Personal Information
                            </h2>
                            <button
                                on:click={toggleEdit}
                                class="text-white hover:text-blue-200 transition-colors"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="p-6">
                        {#if !isEditing}
                            <div class="space-y-4">
                                <div class="flex items-center gap-4">
                                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-xl font-bold">
                                        {user.name ? user.name.split(' ').map(n => n[0]).join('') : 'U'}
                                    </div>
                                    <div>
                                        <h3 class="text-xl font-semibold text-gray-900">{user.display_name || user.name}</h3>
                                        <p class="text-gray-600">{user.email}</p>
                                        <div class="flex gap-2 mt-1">
                                            <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700">
                                                {user.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                            <span class="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">
                                                {user.is_verify ? 'Verified' : 'Unverified'}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-100">
                                    <div>
                                        <label class="text-sm font-medium text-gray-500">Department</label>
                                        <p class="text-gray-900">{user.department || 'Not specified'}</p>
                                    </div>
                                    <div>
                                        <label class="text-sm font-medium text-gray-500">Position</label>
                                        <p class="text-gray-900">{user.position || 'Not specified'}</p>
                                    </div>
                                </div>
                            </div>
                        {:else}
                            <form on:submit|preventDefault={saveProfile} class="space-y-4">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Display Name</label>
                                        <input
                                            bind:value={editForm.display_name}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                            placeholder="Your display name"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                        <input
                                            bind:value={editForm.email}
                                            type="email"
                                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                            readonly
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Department</label>
                                        <input
                                            bind:value={editForm.department}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                            placeholder="Your department"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">Position</label>
                                        <input
                                            bind:value={editForm.position}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                            placeholder="Your position"
                                        />
                                    </div>
                                </div>

                                <div class="flex gap-3 pt-4">
                                    <Button text="Save Changes" variant="primary" />
                                    <button
                                        type="button"
                                        on:click={toggleEdit}
                                        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        {/if}
                    </div>
                </div>

                <!-- AI Settings Card -->
                <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4">
                        <h2 class="text-xl font-semibold text-white flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                            AI Settings
                        </h2>
                    </div>

                    <div class="p-6 space-y-4">
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <h3 class="font-medium text-gray-900">Auto-process with AI</h3>
                                <p class="text-sm text-gray-600">Automatically process new records with AI</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    bind:checked={user.ai_auto_process}
                                    class="sr-only peer"
                                />
                                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                            </label>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">AI Provider</label>
                            <select
                                bind:value={user.ai_provider_id}
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                            >
                                <option value={null}>Select AI Provider</option>
                                {#each aiProviders.filter(p => p.is_active) as provider}
                                    <option value={provider.id}>{provider.name}</option>
                                {/each}
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar -->
            <div class="space-y-6">
                <!-- Task Types Card -->
                <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-green-600 to-teal-600 px-6 py-4">
                        <div class="flex items-center justify-between">
                            <h2 class="text-xl font-semibold text-white flex items-center gap-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                </svg>
                                Task Types
                            </h2>
                            <button
                                on:click={() => showAddTaskType = !showAddTaskType}
                                class="text-white hover:text-green-200 transition-colors"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div class="p-6">
                        {#if showAddTaskType}
                            <form on:submit|preventDefault={addTaskType} class="mb-4 p-4 bg-gray-50 rounded-lg">
                                <div class="space-y-3">
                                    <input
                                        bind:value={newTaskType.title}
                                        placeholder="Task type name"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        required
                                    />
                                    <div class="flex items-center gap-2">
                                        <input
                                            type="color"
                                            bind:value={newTaskType.color}
                                            class="w-8 h-8 border border-gray-300 rounded cursor-pointer"
                                        />
                                        <span class="text-sm text-gray-600">Choose color</span>
                                    </div>
                                    <div class="flex gap-2">
                                        <Button text="Add" variant="success" />
                                        <button
                                            type="button"
                                            on:click={() => showAddTaskType = false}
                                            class="px-3 py-2 text-sm border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            </form>
                        {/if}

                        <div class="space-y-2">
                            {#each taskTypes as taskType, index}
                                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg group">
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="w-4 h-4 rounded-full"
                                            style="background-color: {taskType.color}"
                                        ></div>
                                        <span class="text-gray-900">{taskType.title}</span>
                                    </div>
                                    <button
                                        on:click={() => removeTaskType(index)}
                                        class="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition-all"
                                    >
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>

                <!-- Quick Stats Card -->
                <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
                    <div class="bg-gradient-to-r from-orange-600 to-red-600 px-6 py-4">
                        <h2 class="text-xl font-semibold text-white flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            Quick Stats
                        </h2>
                    </div>

                    <div class="p-6">
                        <div class="space-y-4">
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Total Records</span>
                                <span class="font-semibold text-gray-900">{totalTasks}</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Open</span>
                                <span class="font-semibold text-yellow-600">{openTasks}</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-gray-600">Closed</span>
                                <span class="font-semibold text-grey-600">{closedTasks}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
