<template>
  <label class="block">
    <span v-if="label" v-text="label" class="text-gray-700 text-sm" />
    <input
      :type="type"
      v-model="value"
      class="form-input mt-1 block w-full px-3 outline-none ring-2 ring-blue-500 rounded-md focus:border-indigo-600"
      :class="error ? 'ring-red-500':'ring-blue-500'"
      maxlength="32"
    />
    <slot></slot>
  </label>
</template>


<script lang="ts">
import { computed, defineComponent, PropType } from "vue";
import { loginFieldElements } from "../../assets/data"


export default defineComponent({
  emits: ["update:value"],
  props: {
    value: String,
    input: Object as PropType<Record<string, string>>,
    error: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const value = computed({
      get: () => props.value,
      set: (newValue) => emit("update:value", newValue),
    });
    const type = computed(() => props.input.type)
    const label = computed(() => props.input.label)
    return {
      value,
      type,
      label
    }
  },
});
</script>