<template>
  <form @submit.prevent="addService">
    <div class="grid grid-cols-3 sm:grid-cols-1 gap-10 mb-2">
      <div>
        <label class="text-gray-700" for="passwordConfirmation"
          v-text="'Master password'" />
        <input
          class="form-input h-8 w-full mt-4 rounded-lg border-2 focus:border-indigo-600"
          type="password"
          v-model="masterPassword"
        />

      <div class="mt-6">
        <button
          :disabled="!masterPassword.length"
          type="submit"
          class="py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
        >
          Submit master password
        </button>
      </div>
      </div>
    </div>
  </form>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  setup() {
    const masterPassword = ref("");
    function sendMasterPassword() {}

    return {
      sendMasterPassword,
      masterPassword
    };
  },
});
</script>