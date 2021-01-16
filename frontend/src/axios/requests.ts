import { unrestricted, restricted } from "./config";
import { Credentials, MasterCredentials, NewService } from "./requestTypes";
import { setTokens, useSession } from "../hooks/useSession";
import { Tokens, Service, servicePassword } from "./responseTypes";

export const register = async (payload: Credentials): Promise<void> => {
  try {
    await unrestricted.post("register", payload);
  } catch (err) {
    if (err && err.response) return err.response.data;
    throw err;
  }
};

export const checkMaster = async (): Promise<boolean> => {
  try {
    const { status } = await restricted.get("master");
    return status === 200; 
  } catch (err) {
    if (err && err.response) return err.sponse.data;
    throw err;
  }
};

export const sendMaster = async (payload: MasterCredentials): Promise<void> => {
  try {
    await restricted.post("master", payload);
  } catch (err) {
    if (err && err.response) return err.sponse.data;
    throw err;
  }
};

export const addService = async (payload: NewService): Promise<void> => {
  try {
    await restricted.post("service", payload);
  } catch (err) {
      if (err && err.response) return err.sponse.data;
      throw err;
    }
};

export const fetchServices = async (): Promise<Service[]> => {
  try {
    await unrestricted.get("service");
  } catch (err) {
    if (err && err.reponse) return err.sponse.data;
    throw err;
  }
};

export const decryptPasswords = async (payload: MasterCredentials): Promise<servicePassword[]> => {
  try {
    await restricted.post("passwords", payload);
  } catch (err) {
    if (err && err.response) return err.sponse.data;
    throw err;
  }
};

export const getTokens = async (payload: Credentials): Promise<Tokens> => {
  try {
    const { data = {} } = await unrestricted.post("login", payload);
    setTokens(data);
  } catch (err) {
    if (err && err.response) return err.response.data;
    throw err;
  }
};

export const refreshToken = async (): Promise<string> => {
  const session = useSession();
  const refresh = session.refresh.value;
  try {
    const {
      data: { access },
    } = await unrestricted.post("token_refresh", { refresh });
    setTokens({ access, refresh });
    return access;
  } catch (err) {
    if (err && err.response) return err.response.data;
    throw err;
  }
};
