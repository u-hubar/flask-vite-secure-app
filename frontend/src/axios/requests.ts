import { api } from './config';
import { NewCredentials } from './requestTypes';

export const register = async (payload: NewCredentials): Promise<void> => {
    try {
        await api.post('/api/register', payload);
    } catch (err) {
        if (err && err.response) return err.response.data;
        throw err;
    }
};
