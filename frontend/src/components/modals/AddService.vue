<template>
  <form @submit.prevent="addNewService">

        <input-field
          v-for="field in serviceFieldElements"
          :key="field"
          :input="field"
          v-model:value="service[field.key]"
        />

        <input-field
          :input="{type: 'password', label: 'Confirm password'}"
          v-model:value="confirmPassword"
        />


      <div class="mt-6">
        <button
          :disabled="!validate"
          type="submit"
          class="py-2 px-4 text-center disabled:bg-indigo-300 disabled:cursor-not-allowed bg-indigo-600 rounded-md w-full text-white text-sm hover:bg-indigo-500"
        >
          Add new service
        </button>
      </div>
  </form>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import { NewService } from "../../axios/requestTypes";
import { serviceFieldElements } from "../../assets/data";
import { addService } from "../../axios/requests";

export default defineComponent({
  emits: ["sync"],
  setup(props, { emit }) {
    const confirmPassword = ref("");
    const service = reactive<NewService>({
      service: "",
      url: "",
      username: "",
      password: "",
    });

    const validate = computed(() => {
      const values = Object.values(service);
      const everyValueSet = values.every((value) => value.length);
      const matching = confirmPassword.value === service.password;
      return everyValueSet && matching;
    });

    async function addNewService() {
      const confirmed = await addService(service);
      if (!confirmed) return;
      emit("sync", service)
    }

    return {
      addNewService,
      service,
      confirmPassword,
      validate,
      serviceFieldElements,
    };
  },
});
</script>