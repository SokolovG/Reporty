<script>
    let { variant = 'primary', text} = $props();
    const variants = {
        primary: 'bg-blue-600 hover:bg-blue-700',
        success: 'bg-green-600 hover:bg-green-700',
        warning: 'bg-yellow-600 hover:bg-yellow-700',
        danger: 'bg-red-600 hover:bg-red-700',
        purple: 'bg-purple-600 hover:bg-purple-700',
        indigo: 'bg-indigo-600 hover:bg-indigo-700'
    };
</script>

<button
    type="submit"
    class="text-white px-4 py-2 rounded-lg transition-colors {variants[variant]}">
    {text}
</button>
