<template>
  <form @submit.prevent="addService()">
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
          v-model="confirmPassword"
        />
      </div>

      <div class="mt-6">
        <button
          :disabled="!validate"
          type="submit"
          class="py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
        >
          Add new service
        </button>
      </div>
    </div>
  </form>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import { NewService } from "../../axios/requestTypes";

export default defineComponent({
  setup() {
    const confirmPassword = ref("");
    const newService = reactive<NewService>({
      service: "",
      url: "",
      username: "",
      password: "",
    });

    const validate = computed(() => {
      const values = Object.values(newService);
      const everyValueSet = values.every((value) => value.length);
      const matching = confirmPassword.value === newService.password;
      return everyValueSet && matching;
    });

    function addService() {
      console.log("Placeholder for adding service");
    }

    return {
      addService,
      newService,
      confirmPassword,
      validate,
    };
  },
});
</script>