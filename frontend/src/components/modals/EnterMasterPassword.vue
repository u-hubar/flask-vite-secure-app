<template>
  <form @submit.prevent="sendMasterPassword">
    <input-field
      class="mt-4"
      :input="{ label: 'Enter password', type: 'password' }"
      v-model:value="masterPassword"
    />
    <input-field
      class="mt-4"
      v-if="!hasMaster"
      :input="{ type: 'password', label: 'Confirm your password' }"
      v-model:value="confirmPassword"
    />
    <div class="mt-3 text-center">
      <span
        class="text-sm text-red-500"
        v-if="!hasMaster"
        v-text="'You cannot change master password so choose wisely'"
      />
      <button
        :disabled="!validate"
        type="submit"
        class="mt-2 py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
      >
        Submit master password {{ hasMaster }} {{ validate }}
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { computed, defineComponent, ref, onMounted } from "vue";
import { checkMaster } from "../../axios/requests";
import InputField from "../utils/InputField.vue";

export default defineComponent({
  components: { InputField },
  setup() {
    const masterPassword = ref("");
    const confirmPassword = ref("");

    function sendMasterPassword() {
      console.log("sendMasterPassword");
    }

    const hasMaster = ref(false);

    onMounted(async () => {
      hasMaster.value = await checkMaster();
    });

    const validate = computed(() => {

      const pass = masterPassword.value;
      const pass2 = confirmPassword.value;

      return hasMaster.value
        ? Boolean(pass)
        : (pass && pass2 && pass === pass2);
    });

    return {
      sendMasterPassword,
      confirmPassword,
      masterPassword,
      hasMaster,
      validate,
    };
  },
});
</script>