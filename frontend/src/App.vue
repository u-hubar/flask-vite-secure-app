<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { setTokens } from "./hooks/useSession";

const defaultLayout = "default";

export default defineComponent({
  setup() {
    const { currentRoute } = useRouter();

    const layout = computed(
      () => `${currentRoute.value.meta.layout || defaultLayout}-layout`
    );

    onMounted(() => {
      const tokens = localStorage.getItem('pswd_man');
      if (!tokens) return;
      setTokens(JSON.parse(tokens))
    })

    return {
      layout,
    };
  },
});
</script>
