<template>
  <div class="flex justify-center items-center h-screen bg-gray-200 px-6">
    <div class="p-6 max-w-md w-full bg-white shadow-md rounded-md">
      <div class="flex justify-center items-center">
        <svg
          class="h-10 w-10"
          viewBox="0 0 512 512"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M364.61 390.213C304.625 450.196 207.37 450.196 147.386 390.213C117.394 360.22 102.398 320.911 102.398 281.6C102.398 242.291 117.394 202.981 147.386 172.989C147.386 230.4 153.6 281.6 230.4 307.2C230.4 256 256 102.4 294.4 76.7999C320 128 334.618 142.997 364.608 172.989C394.601 202.981 409.597 242.291 409.597 281.6C409.597 320.911 394.601 360.22 364.61 390.213Z"
            fill="#4C51BF"
            stroke="#4C51BF"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M201.694 387.105C231.686 417.098 280.312 417.098 310.305 387.105C325.301 372.109 332.8 352.456 332.8 332.8C332.8 313.144 325.301 293.491 310.305 278.495C295.309 263.498 288 256 275.2 230.4C256 243.2 243.201 320 243.201 345.6C201.694 345.6 179.2 332.8 179.2 332.8C179.2 352.456 186.698 372.109 201.694 387.105Z"
            fill="white"
          />
        </svg>
        <span class="text-gray-700 font-semibold text-2xl"
          >Password Manager</span
        >
      </div>

      <form class="mt-4" @submit.prevent="login">
        <input-field
          v-for="field in loginFieldElements"
          :key="field"
          :input="field"
          v-model:value="credentials[field.key]"
        />

        <div class="mt-4 flex justify-between">
          <router-link
            to="/register"
            class="btn btn-link text-sm fontme text-indigo-700 hover:underline"
            >Register</router-link
          >
          
          <span class="text-sm" v-if="counter && counter < 5" v-text="`You have ${5 - counter} tries left`"/>
          <span v-else>
            <timer :deadline="time" @reset="resetTime" />
          </span>
        </div>

        <div class="mt-6">
          <button
            :disabled="Object.values(credentials).some((value) => !value) || counter > 4"
            type="submit"
            class="py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
          >
            Sign in
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { loginFieldElements } from "../assets/data";
import { getTokens } from "../axios/requests";
import { Credentials } from "../axios/requestTypes";
import { useSession } from "../hooks/useSession";

import { defineComponent, ref, reactive, watch, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import InputField from "../components/utils/InputField.vue";
import Timer from "../components/utils/Timer.vue";


export default defineComponent({
  components: { InputField, Timer },
  setup() {
    const router = useRouter();
    const counter = ref(0);
    const time = ref(0);

    const credentials = reactive<Credentials>({
      email: "",
      password: "",
    });

    const tokens = useSession();

    const isAuthenticated = computed(() => {
      return Boolean(tokens.refresh.value.length);
    });

    const timerReset = ref(false)


    watch(counter, value => {
      if (value === 5) time.value = Date.now() + 59000;
    })

    function resetTime(value: boolean) {
      counter.value = 0;
      time.value = 0;
      timerReset.value = true;
    }

    async function login() {
      try {
        await getTokens(credentials)
        const session = useSession();
        if (!session.access.value || !session.refresh.value) {
          counter.value += 1;
          return
        };
        router.push("/dashboard");
      } catch (err) {
        counter.value += 1;
      }
    }

    onMounted(async () => {
      if (isAuthenticated.value) useRouter().push("/dashboard");
    });

    return {
      loginFieldElements,
      login,
      credentials,
      counter,
      time,
      resetTime,
      timerReset
    };
  },
});
</script>
