import { unrestricted, restricted } from "./config";
import { Credentials, NewService } from "./requestTypes";
import { setTokens, useSession, resetTokens } from "../hooks/useSession";
import { Service, ServicePassword, Logs } from "./responseTypes";

export const register = async (payload: Credentials): Promise<void> => {
  try {
    await unrestricted.post("register", payload);
  } catch (err) {
    throw err;
  }
};

export const checkMaster = async (): Promise<boolean> => {
  try {
    const response = await restricted.get("master");
    return response.status === 200;
  } catch (err) {
    return false;
  }
};

export const sendMaster = async (master: string): Promise<boolean> => {
  try {
    const { status } = await restricted.post("master", { master })
    return status >= 200 && status < 300
  } catch (err) {
    return false;
  }
};

export const fetchLogs = async (): Promise<Logs[]> => {
  try {
    const { data } = await restricted.get("logs");
    return data
  } catch (err) {
    throw err;
  }
};

export const addService = async (payload: NewService): Promise<boolean> => {
  try {
    const { status} = await restricted.post("service", payload);
    return status >= 200 && status < 300
  } catch (err) {
    throw err;
  }
};

export const fetchServices = async (): Promise<Service[]> => {
  try {
    const { data } = await restricted.get("service");
    return data
  } catch (err) {
    throw err;
  }
};

export const decryptPasswords = async (master: string): Promise<ServicePassword[]> => {
  try {
    const { data } = await restricted.post("passwords", { master });
    return data;
  } catch (err) {
    throw err;
  }
};

export const getTokens = async (payload: Credentials): Promise<void> => {
  try {
    const { data = {} } = await unrestricted.post("login", payload);
    setTokens(data);
  } catch (err) {
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
    resetTokens();
    throw err;
  }
};
