<template>
  <div>
    <div>
      <div class="flex justify-between">
        <h3 class="text-gray-700 text-3xl font-medium">Passwords Dashboard</h3>

        <div class="flex space-x-2">
          <button
            @click="open = true"
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

      <div
        :class="`modal ${
          !open && 'opacity-0 pointer-events-none'
        } z-50 fixed w-full h-full top-0 left-0 flex items-center justify-center`"
      >
        <div
          class="modal-overlay absolute w-full h-full bg-gray-900 opacity-50"
        ></div>

        <div
          class="modal-container bg-white w-11/12 md:max-w-md mx-auto rounded shadow-lg z-50 overflow-y-auto"
        >
          <div
            class="modal-close absolute top-0 right-0 cursor-pointer flex flex-col items-center mt-4 mr-4 text-white text-sm z-50"
          >
            <svg
              class="fill-current text-white"
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 18 18"
            >
              <path
                d="M14.53 4.53l-1.06-1.06L9 7.94 4.53 3.47 3.47 4.53 7.94 9l-4.47 4.47 1.06 1.06L9 10.06l4.47 4.47 1.06-1.06L10.06 9z"
              />
            </svg>
            <span class="text-sm">(Esc)</span>
          </div>

          <!-- Add margin if you want to see some of the overlay behind the modal-->
          <div class="modal-content py-4 text-left px-6">
            <!--Title-->
            <div class="flex justify-between items-center pb-3">
              <p class="text-2xl font-bold">New service</p>
              <div class="modal-close cursor-pointer z-50" @click="open = false">
                <svg
                  class="fill-current text-black"
                  xmlns="http://www.w3.org/2000/svg"
                  width="18"
                  height="18"
                  viewBox="0 0 18 18"
                >
                  <path
                    d="M14.53 4.53l-1.06-1.06L9 7.94 4.53 3.47 3.47 4.53 7.94 9l-4.47 4.47 1.06 1.06L9 10.06l4.47 4.47 1.06-1.06L10.06 9z"
                  />
                </svg>
              </div>
            </div>

            <!--Body-->
            <div class="mt-4">
              <div class="p-6 bg-white rounded-md shadow-md">

                <form @submit.prevent="register">
                  <div class="grid grid-cols-3 sm:grid-cols-1 gap-10 mb-2">
                    <div>
                      <label class="text-gray-700" for="username">Username</label>
                      <input
                        class="form-input h-8 w-full mt-4 rounded-md border-2 focus:border-indigo-600"
                        type="text"
                        v-model="newService.username"
                      />
                    </div>

                    <div>
                      <label class="text-gray-700" for="password">Password</label>
                      <input
                        class="form-input h-8 w-full mt-4 rounded-md border-2 focus:border-indigo-600"
                        type="password"
                        v-model="newService.password"
                      />
                    </div>

                    <div>
                      <label class="text-gray-700" for="passwordConfirmation"
                        >Password Confirmation</label
                      >
                      <input
                        class="form-input h-8 w-full mt-4 rounded-lg border-2 focus:border-indigo-600"
                        type="password"
                        v-model="newService.confirm"
                      />
                    </div>
                  </div>
                </form>
              </div>
            </div>

            <!--Footer-->
            <div class="flex justify-end pt-2">
              <button
                @click="open = false"
                class="px-6 py-3 bg-transparent p-3 rounded-lg text-indigo-500 hover:bg-gray-100 hover:text-indigo-400 mr-2"
              >
                Close
              </button>
              <button
                @click="open = false"
                class="px-6 py-3 bg-indigo-600 rounded-md text-white font-medium tracking-wide hover:bg-indigo-500"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

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
                  URL
                </th>
                <th
                  class="px-6 py-2 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider"
                >
                  Username
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
                    {{ s.url }}
                  </div>
                </td>

                <td
                  class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
                >
                  <div class="text-sm leading-5 text-gray-900">
                    {{ s.username }}
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
import { defineComponent, ref, computed, onMounted } from "vue";
import { useSession } from "../hooks/useSession"
import { useRouter } from "vue-router";

interface Service {
  service: string;
  url: string,
  username: string,
  password: string;
}

interface NewService extends Service {
  confirmPassword: string;
}

export default defineComponent({
  setup() {
    const testService: Service = {
      service: "Google Cloud",
      url: "https://cloud.google.com/",
      username: "Vlad",
      password: "HASH"
    };

    const newService = ref<NewService>({
      service: "",
      url: "",
      username: "",
      password: "",
      confirmPassword: "",
    })

    const register = () => {
      const data = JSON.parse(JSON.stringify(newService.value));
      
    };

    const services = ref<Service[]>([...Array(9).keys()].map(() => testService));

    const open = ref(false);

    const isAuthenticated = computed(() => {
      const session = useSession();
      return Boolean(session.refresh.value.length)
    })

    onMounted(() => {
      if (!isAuthenticated.value) useRouter().push("/");
    })

    return {
      open,
      services,
      newService,
      register
    };
  },
});
</script>

<style>
.modal {
  transition: opacity 0.25s ease;
}
</style>
