import axios from "axios";
import { QueryFunction } from "react-query";

export const query: QueryFunction = async ({ queryKey }) => {
    // TODO: Use the environment variable SERVER here (process.env.SERVER)
    const { data } = await axios.get(`http://localhost:8000/${queryKey[0]}`);
    return data;
};