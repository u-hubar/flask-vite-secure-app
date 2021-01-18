<template>
  <tr>
    <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
      <div class="flex items-center">
        <div class="flex-shrink-0 h-10 w-10">
          <img
            class="h-10 w-10 rounded-full"
            src="https://www.flaticon.com/svg/static/icons/svg/743/743040.svg"
            alt=""
          />
        </div>
        <div class="ml-4">
          <div class="text-sm leading-5 font-medium text-gray-900">
            {{ service.service }}
          </div>
        </div>
      </div>
    </td>

    <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
      <div class="text-sm leading-5 text-gray-900">
        {{ service.url }}
      </div>
    </td>

    <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
      <div class="text-sm leading-5 text-gray-900">
        {{ service.username }}
      </div>
    </td>

    <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
      <div class="text-sm leading-5 text-gray-900">
        {{ service.password }}
      </div>
    </td>
  </tr>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

interface Service {
  username: string;
  password: string;
  service: string;
  url: string;
}

export default defineComponent({
  props: {
    service: {
      type: Object as PropType<Service>
    },
  },
});
</script>