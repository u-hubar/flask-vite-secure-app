<template>
  <div
    :class="{
      'opacity-0 pointer-events-none': !open,
    }"
    class="modal z-50 fixed w-full h-full top-0 left-0 flex items-center justify-center"
  >
    <div
      class="modal-overlay absolute w-full h-full bg-gray-900 opacity-50"
    ></div>

    <div
      class="modal-container bg-white w-11/12 md:max-w-md mx-auto rounded shadow-lg z-50 overflow-y-auto"
    >
      <div class="modal-content py-4 text-left px-6">
        <!--Title-->
        <div class="flex justify-between items-center pb-3">
          <p class="text-2xl font-bold" v-text="title" />
          <div class="modal-close cursor-pointer z-50" @click="logMessage()">
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
        <slot />

        <!--Footer-->
        <div class="flex justify-end pt-2">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect } from "vue";

export default defineComponent({
  props: {
    open: Boolean,
    title: String,
  },
  emits: ['update:open'],
  setup(props, { emit }) {
    function logMessage() {
      emit("update:open", false);
    }
    return {
      logMessage,
    };
  },
});
</script>