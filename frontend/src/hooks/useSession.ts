import { reactive, toRefs } from "vue";
import { Tokens } from "../axios/responseTypes"
import { refreshToken } from "../axios/requests"

const state = reactive(<Tokens>{
  access: '',
  refresh: '',
});

export function useSession() {
  return {
    ...toRefs(state),
  };
}

export async function setTokens({ access, refresh }: Tokens) {
  state.access = access;
  state.refresh = refresh;
  
}


export async function extendSession() {
  state.access = await refreshToken(state.refresh);
}

export function resetAccessToken() {
  state.access = '';
}

export function resetTokens() {
  state.access = '';
  state.refresh = '';
}
