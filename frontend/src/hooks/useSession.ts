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
  console.log('saved access and refresh tokens', state)
  localStorage.setItem('pswd_man', JSON.stringify(state))
}

export async function extendSession() {
  await refreshToken();
}

export function resetAccessToken() {
  state.access = '';
  localStorage.setItem('pswd_man', JSON.stringify(state))
}

export function resetTokens() {
  state.access = '';
  state.refresh = '';
  localStorage.setItem('pswd_man', '')
  localStorage.clear();
}
