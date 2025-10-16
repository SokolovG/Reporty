<script>
  import {STATUS_STYLES} from "$lib/constants.js";

  let { status, variant = 'default' } = $props();

  const styles = {
    default: STATUS_STYLES[status] || 'bg-gray-100 text-gray-700',
    success: 'bg-emerald-100 text-emerald-700',
    warning: 'bg-amber-100 text-amber-700',
    info: 'bg-amber-100 text-amber-700'
  };
</script>

<span class="px-2 py-1 text-xs rounded-full {styles[variant]}">
  <slot>{status}</slot>
</span>
