<script>
  import {STATUS_STYLES} from "$lib/constants.js";

  let { status, variant = 'default' } = $props();

  const styles = {
    default: STATUS_STYLES[status] || 'bg-gray-100 text-gray-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-yellow-100 text-yellow-700',
    info: 'bg-blue-100 text-blue-700'
  };
</script>

<span class="px-2 py-1 text-xs rounded-full {styles[variant]}">
  <slot>{status}</slot>
</span>
