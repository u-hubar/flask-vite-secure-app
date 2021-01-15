import { reactive, toRefs } from "vue";

const state = reactive({
  active: '',
});

export function useModal() {
  return {
    ...toRefs(state),
  };
}
