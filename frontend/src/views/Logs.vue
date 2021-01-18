<template>
  <div>
    <h3 class="text-gray-700 text-3xl font-medium mb-6">Logs Console</h3>
    <p v-show="false" class="my-2 p-1" v-for="log in 5" :key="log" v-text="log" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  setup() {
    const logs = ref([] as string[])

    onMounted(async() => {
      // logs.value = await myEndpoint()
    })


  },
});
</script>