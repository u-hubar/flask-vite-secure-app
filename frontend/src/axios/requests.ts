import { unrestricted, restricted } from "./config";
import { Credentials, NewService } from "./requestTypes";
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
    if (err && err.response) return false;
    throw err;
  }
};

export const sendMaster = async (master: string): Promise<void> => {
  try {
    await restricted.post("master", { master });
  } catch (err) {
    if (err && err.response) return err.response.data;
    throw err;
  }
};

export const addService = async (payload: NewService): Promise<void> => {
  try {
    await restricted.post("service", payload);
  } catch (err) {
      if (err && err.response) return err.response.data;
      throw err;
    }
};

export const fetchServices = async (): Promise<Service[]> => {
  try {
    await restricted.get("service");
  } catch (err) {
    if (err && err.reponse) return err.response.data;
    throw err;
  }
};

export const decryptPasswords = async (master: string): Promise<servicePassword[]> => {
  try {
    await restricted.post("passwords", { master });
  } catch (err) {
    if (err && err.response) return err.response.data;
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
