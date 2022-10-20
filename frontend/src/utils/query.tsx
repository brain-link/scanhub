import axios from 'axios';
import { QueryFunction } from 'react-query';
import config from './config';

export const query: QueryFunction = async ({ queryKey }) => {
    // TODO: Use the environment variable SERVER here (process.env.SERVER)
    const { data } = await axios.get(`${config.baseURL}${queryKey[0]}`);
    return data;
};