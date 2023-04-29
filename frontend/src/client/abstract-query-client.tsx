import axios, { AxiosInstance } from 'axios';


// TODO:
// - id's are currently of type number and should become of type uuid
// - maybe extend error handling


export abstract class ApiService<T> {
    private readonly axiosInstance: AxiosInstance;

    constructor(private readonly baseURL: string) {
        this.axiosInstance = axios.create({
            baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }

    async getAll(parent_id?: number): Promise<T[] | []> {
        try {
            // Parent id parameter is optional, if provided it is used in an "/all/<parent_id>"" endpoint
            // Otherwise the default case endpoint "/" is used
            const queryUrl = parent_id ? `/all/${parent_id}` : '/';

            const response = await this.axiosInstance.get<T[]>(queryUrl);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async get(id: number): Promise<T> {
        try {
            const response = await this.axiosInstance.get<T>(`/${id}`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async create(data: T): Promise<T> {
        try {
            const response = await this.axiosInstance.post<T>('/', data);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async update(id: number, data: T): Promise<T> {
        try {
            const response = await this.axiosInstance.put<T>(`/${id}`, data);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async delete(id: number): Promise<void> {
        try {
            await this.axiosInstance.delete(`/${id}`);
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    private handleError(error: any) {
        if (axios.isAxiosError(error)) {
            console.log("Catched axios error: ", error)
        }
    }
}
