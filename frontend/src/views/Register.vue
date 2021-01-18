<template>
  <div class="flex justify-center items-center h-screen bg-gray-200 px-6">
    <div class="p-6 max-w-sm w-full bg-white shadow-md rounded-md">
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
        <span class="text-gray-700 font-semibold text-2xl">Password Manager</span>
      </div>

      <form class="mt-4" @submit.prevent="handleRegister">

        <input-field
          v-for="field in loginFieldElements"
          :key="field"
          :input="field"
          :error="fields.includes(field.key) && !credentials[field.key]"
          v-model:value="credentials[field.key]"
          @input="checkFieldsInput(field.key)"
        />
        <input-field
          :input="{type: 'password', label: 'Confirm password' }"
          :error="fields.includes('confirm') && !passwordConfirm"
          v-model:value="passwordConfirm"
          @input="checkFieldsInput('confirm')"
        />


          <div class="mt-4 text-xs" :class="credentials.password.length > 7 && passwordFeedback.score === 4 && passwordMatching ? 'text-green-500' : 'text-red-600'" v-if="Object.keys(passwordFeedback)" >
            <span v-text="passwordFeedback.warning" />
          </div>
        <div :class="!Object.keys(passwordFeedback) ? 'mt-10' : ''" class="mt-6">
          <button
            type="submit"
            class="py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
            :disabled="!validate"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { loginFieldElements } from '../assets/data';
import { register } from '../axios/requests';
import { Credentials } from '../axios/requestTypes';
import { defineComponent, ref, reactive, computed } from "vue";
import router from '../router';
import zxcvbn from "zxcvbn";

export default defineComponent({
  setup() {
    const credentials = reactive<Credentials>({
      email: "",
      password: "",
    })

    const passwordConfirm = ref(''); 

    const passwordFeedback = computed(() => {
      if (!credentials.password) return {}
      const { feedback, score } = zxcvbn(credentials.password)
      const obj = score < 4
        ? {...feedback, score}
        : {
          score, warning: credentials.password.length < 7
          ? 'Your password is too short'
          : "Your password is strong"
        };
      if (credentials.password.length === 1) obj.warning = 'Your password is too short'
      if (passwordConfirm.value && !passwordMatching.value) obj.warning = 'Passwords not matching'
      return obj
      })

    const fields = ref<String[]>([])

    function checkFieldsInput(
      value: string
    ){
      if (fields.value.includes(value)) return;
      fields.value.push(value)
    }

    const passwordMatching = computed(() => {
      return passwordConfirm.value === credentials.password
    })

    const validate = computed(() =>
      Object.values(credentials).every(value => value.length) && passwordMatching.value && credentials.password.length > 8 && passwordFeedback.value.score > 2
    )

    async function handleRegister() {
      if (!validate) return;
      await register(credentials).then(() => router.push({ name: 'login' }));
    }

    return {
      loginFieldElements,
      credentials,
      fields,
      checkFieldsInput,
      validate,
      handleRegister,
      passwordConfirm,
      passwordFeedback,
      passwordMatching
    };
  },
});
</script>
