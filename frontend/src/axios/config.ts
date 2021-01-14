import Axios, { AxiosError, AxiosRequestConfig } from 'axios';
import { useSession, extendSession, resetTokens, resetAccessToken } from "../hooks/useSession"

const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Cache-Control': 'no-cache',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Origin': '*',
};

export const unrestricted = Axios.create({
  baseURL: `https://${window.location.hostname}/api/`,
  responseType: 'json',
  headers,
});


export const restricted = Axios.create({
  baseURL: `https://${window.location.hostname}/api/`,
  responseType: 'json',
  headers,
});

const addAccessToken = (config: AxiosRequestConfig) => {
  const { access } = useSession();
  return { ...config, headers: { Authorization: `Bearer ${access.value}` } };
};

export const interceptRequests = (config: AxiosRequestConfig) => {
  const { access } = useSession();
  return access.value ? addAccessToken(config) : config
};
export const interceptRequestErrors = (error: AxiosError) => Promise.reject(error);

export const interceptResponseErrors = async (error: AxiosError) => {
  if (error.response?.status !== 401) return Promise.reject(error);
  resetAccessToken();

  const { config: originalRequest } = error;

  try {
    await extendSession();
    if (!access.value) return Promise.reject(error);
    originalRequest.headers.Authorization = `Bearer ${access.value}`;
  } catch (err) {
    resetTokens();
    Promise.reject(err);
  }
  return restricted(originalRequest);
};

restricted.interceptors.request.use(interceptRequests, interceptRequestErrors);
restricted.interceptors.response.use((config: any) => config, interceptResponseErrors);
