<template>
  <div>
    <h3 class="text-gray-700 text-3xl font-medium">Passwords Dashboard</h3>


    <div class="mt-8"></div>

    <div class="flex flex-col mt-8">
      <div class="-my-2 py-2 overflow-x-auto sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div
          class="align-middle inline-block min-w-full shadow overflow-hidden sm:rounded-lg border-b border-gray-200"
        >
          <table class="min-w-full">
            <thead>
              <tr>
                <th
                  class="px-6 py-2 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider"
                >
                  Service
                </th>
                <th
                  class="px-6 py-2 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider"
                >
                  Password
                </th>
              </tr>
            </thead>

            <tbody class="bg-white">
              <tr v-for="(s, index) in services" :key="index">
                <td
                  class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                >
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
                        {{ s.service }}
                      </div>
                    </div>
                  </div>
                </td>

                <td
                  class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                >
                  <div class="text-sm leading-5 text-gray-900">
                    {{ s.password }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

interface Service {
  service: string;
  password: string;
}

export default defineComponent({
  setup() {
    const testService: Service = {
      service: "google.com",
      password: "HASH"
    };

    const services = ref<Service[]>([...Array(10).keys()].map(() => testService));

    return {
      services,
    };
  },
});
</script>
