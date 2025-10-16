<script>
    let { variant = 'primary', text} = $props();
    const variants = {
        primary: 'bg-amber-600 hover:bg-amber-700',
        success: 'bg-emerald-600 hover:bg-emerald-700',
        warning: 'bg-orange-600 hover:bg-orange-700',
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
