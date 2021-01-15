<template>
  <div>
    {{ open }}
    <div>
      <div class="flex justify-between">
        <h3 class="text-gray-700 text-3xl font-medium">Passwords Dashboard</h3>

        <div class="flex space-x-2">
          <button
            @click="showPasswords()"
            class="mt-3 px-6 py-3 bg-green-600 rounded-md text-white font-medium tracking-wide hover:bg-green-500"
          >
            Show Passwords
          </button>

          <button
            @click="open = true"
            class="mt-3 px-6 py-3 bg-indigo-600 rounded-md text-white font-medium tracking-wide hover:bg-indigo-500"
          >
            Add new service
          </button>
        </div>
      </div>
    </div>

    <div class="mt-8"></div>

    <modal :open.sync="open" :title="masterPassword ? 'Add service' : 'Enter master password'">
      <template #default>
        <add-service v-if="masterPassword" />
        <enter-master-password v-else />
      </template>
    </modal>

    <div class="flex flex-col mt-8">
      <div class="-my-2 py-2 overflow-x-auto sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div
          class="align-middle inline-block min-w-full shadow overflow-hidden sm:rounded-lg border-b border-gray-200"
        >
          <table class="min-w-full">
            <thead>
              <tr>
                <th
                  v-for="item in ['Service', 'URL', 'Username', 'Password']"
                  :key="item"
                  class="px-6 py-2 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider"
                >
                  Service
                </th>
              </tr>
            </thead>

            <tbody class="bg-white">
              <services-row
                v-for="(s, index) in services"
                :service="s"
                :key="index"
              />
            </tbody>
          </table>
          <div
            class="px-5 py-5 bg-white border-t flex flex-col xs:flex-row items-center xs:justify-between"
          >
            <div class="inline-flex mt-2 xs:mt-0">
              <button
                class="text-sm bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-l"
              >
                Prev
              </button>
              <button
                class="text-sm bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-r"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import AddService from "../components/modals/AddService.vue";
import EnterMasterPassword from "../components/modals/EnterMasterPassword.vue";
import Modal from "../components/Modal.vue"
import ServicesRow from "../components/table/ServicesRow.vue";

import { computed, defineComponent, onMounted, ref } from "vue";
import { checkMaster } from "../axios/requests";
import { useRouter } from "vue-router";
import { useSession } from "../hooks/useSession";
import { Service } from "../types"

export default defineComponent({
  components: {
    AddService,
    EnterMasterPassword,
    Modal,
    ServicesRow,
  },
  setup() {
    const testService: Service = {
      service: "Google Cloud",
      url: "https://cloud.google.com/",
      username: "Vlad",
      password: "HASH",
    };

   //  const register = () => {
   //   const data = JSON.parse(JSON.stringify(newService.value));
   // };

    const services = ref<Service[]>(
      [...Array(9).keys()].map(() => testService)
    );

    const open = ref(false);

    const isAuthenticated = computed(() => {
      const session = useSession();
      return Boolean(session.refresh.value.length);
    });

    const masterPassword = ref('');

    function showPasswords() {
      if (masterPassword.value) () => {}
      else open.value = true;
    }

    onMounted(() => {
      if (!isAuthenticated.value) useRouter().push("/");
    });

    return {
      open,
      services,
      showPasswords,
      masterPassword
    };
  },
});
</script>

<style>
.modal {
  transition: opacity 0.25s ease;
}
</style>
