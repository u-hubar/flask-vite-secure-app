import { unrestricted, restricted } from './config';
import { NewCredentials, Credentials } from './requestTypes';
import { setTokens } from '../hooks/useSession';
import { Tokens } from './responseTypes';

export const register = async (payload: NewCredentials): Promise<void> => {
    try {
        
        await unrestricted.post('register', payload);
    } catch (err) {
        if (err && err.response) return err.response.data;
        throw err;
    }
};

export const getTokens = async (payload: Credentials): Promise<Tokens> => {
    try {
      const { data } = await unrestricted.post('login', payload);
      
      setTokens(data);
    } catch (err) {
        if (err && err.response) return err.response.data;
        throw err;
    }
  };
  
  export const refreshToken = async (refresh: string): Promise<string> => {
    try {
      const {
        data: { access },
      } = await unrestricted.post('token_refresh', { refresh });
      return access;
    } catch (err) {
        if (err && err.response) return err.response.data;
        throw err;
    }
  };
  