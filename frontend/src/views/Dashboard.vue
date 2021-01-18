<template>
  <div>
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
            @click="addNewService()"
            class="mt-3 px-6 py-3 bg-indigo-600 rounded-md text-white font-medium tracking-wide hover:bg-indigo-500"
          >
            Add new service
          </button>
        </div>
      </div>
    </div>

    <div class="mt-8"></div>

    <modal
      :lock="lock"
      v-model:open="open"
      :title="
        masterPassword && action === 'add service'
          ? 'Add service'
          : 'Enter master password'
      "
    >
      <template v-if="open" #default>
        <add-service
          @sync="(service) => services.push(service)"
          v-model:open="open"
          v-if="masterPassword && action === 'add service'"
        />
        <enter-master-password
          v-else
          @lock="lock = true"
          :action="action"
          @success="handleMasterPassword"
        />
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
                  v-text="item"
                />
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
import Modal from "../components/Modal.vue";
import ServicesRow from "../components/table/ServicesRow.vue";

import { computed, defineComponent, onMounted, ref } from "vue";
import {
  checkMaster,
  fetchServices,
  decryptPasswords,
} from "../axios/requests";
import { useRouter } from "vue-router";
import { useSession } from "../hooks/useSession";
import { Service } from "../axios/responseTypes";

export default defineComponent({
  components: {
    AddService,
    EnterMasterPassword,
    Modal,
    ServicesRow,
  },
  setup() {
    const services = ref<Service[]>([]);

    const open = ref(false);

    const isAuthenticated = computed(() => {
      const session = useSession();
      return Boolean(session.refresh.value.length);
    });

    const masterPassword = ref("");
    const action = ref("");

    const lock = ref(false);

    function openModal() {
      if (lock.value) return;
      open.value = true
    }

    async function showPasswords() {
      console.log(
        "showPasswords function, checking master password value",
        masterPassword.value
      );
      if (masterPassword.value)
        await decryptPasswords(masterPassword.value).then((password) => {
          services.value = services.value.map((service) => ({
            ...service,
            password: password.find(({ id }) => id === service.id)?.["password"] || service.password || "",
          }));
        });
      else {
        action.value = "show passwords";
        openModal();
      }
    }

    function addNewService() {
      action.value = "add service";
      openModal();
    }

    async function handleMasterPassword(password) {
      masterPassword.value = password;
      if (action.value !== "show passwords") return;
      open.value = false;
      await showPasswords();
    }

    onMounted(async () => {
      if (!isAuthenticated.value) useRouter().push("/");
      try {
        services.value = await fetchServices();
      } catch (err) {
        console.log("Error");
      }
    });

    return {
      open,
      services,
      showPasswords,
      masterPassword,
      addNewService,
      action,
      handleMasterPassword,
      lock,
    };
  },
});
</script>

<style>
.modal {
  transition: opacity 0.25s ease;
}
</style>
