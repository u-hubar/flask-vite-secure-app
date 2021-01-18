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
      <span
        class="text-sm"
        v-if="counter && counter < 3"
        v-text="`You have ${3 - counter} tries left`"
      />
      <span v-else>
        <timer :deadline="time" @reset="resetTime" />
      </span>
      <div class="mt-4 text-xs" :class="masterPassword.length > 7 && passwordFeedback.score === 4 && passwordMatching ? 'text-green-500' : 'text-red-600'" v-if="Object.keys(passwordFeedback) && masterPassword.length && !hasMaster" >
        <span v-text="passwordFeedback.warning" />
      </div>
      <button
        :disabled="!validate || time"
        type="submit"
        class="mt-2 py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
      >
        Submit master password
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { computed, defineComponent, ref, onMounted, watch } from "vue";
import zxcvbn from "zxcvbn";
import { checkMaster, sendMaster } from "../../axios/requests";
import Timer from "../utils/Timer.vue";

export default defineComponent({
  components: { Timer },
  emits: ["success", "lock"],
  setup(props, { emit }) {
    const masterPassword = ref("");
    const confirmPassword = ref("");

    const counter = ref(0);
    const time = ref(0);

    watch(counter, (value) => {
      if (value !== 3) return;
      time.value = Date.now() + 5 * 60000 - 1000;
      emit("lock", true);
    });

    function resetTime(value: boolean) {
      counter.value = 0;
      time.value = 0;
      emit("lock", false);
    }

    async function sendMasterPassword() {
      const confirmed = await sendMaster(masterPassword.value);
      if (confirmed) emit("success", masterPassword.value);
      else counter.value += 1;
    }

    const hasMaster = ref(false);

   const passwordFeedback = computed(() => {
      if (!masterPassword.value) return {}
      const { feedback, score } = zxcvbn(masterPassword.value)
      const obj = score < 4
        ? {...feedback, score}
        : {
          score, warning: masterPassword.value.length < 7
          ? 'Your password is too short'
          : "Your password is strong"
        };
      if (masterPassword.value.length === 1) obj.warning = 'Your password is too short'
      if (confirmPassword.value && masterPassword.value !== confirmPassword.value) obj.warning = 'Passwords not matching'
      return obj
      })

    onMounted(async () => {
      hasMaster.value = await checkMaster();
    });

    const passwordMatching = computed(() => {
      return masterPassword.value === confirmPassword.value
    })

    const validate = computed(() => {
      const pass = masterPassword.value;
      const pass2 = confirmPassword.value;

      return hasMaster.value ? Boolean(pass) : pass && pass2 && pass === pass2;
    });

    return {
      sendMasterPassword,
      confirmPassword,
      masterPassword,
      hasMaster,
      validate,
      counter,
      time,
      resetTime,
      passwordFeedback,
      passwordMatching
    };
  },
});
</script>