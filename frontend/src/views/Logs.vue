<template>
  <div>
    <h3 class="text-gray-700 text-3xl font-medium mb-6">Logs Console</h3>
    <div class="flex flex-col space-y-1 mb-8" v-for="log in logs.slice().reverse()" :key="log.id">
      <span class="bg-clip-text font-black text-black">{{log.datetime}}</span>
      <span class="bg-clip-text font-black text-gray-500">{{log.user_agent}}</span>
      <span class="bg-clip-text font-black text-gray-500">{{log.user_ip}}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { fetchLogs } from "../axios/requests";
import { Logs } from "../axios/responseTypes";

export default defineComponent({
  setup() {
    const logs = ref([] as Logs[])

    onMounted(async() => {
      logs.value = await fetchLogs()
    })

  return {
    logs,
  }
  },
});
</script>