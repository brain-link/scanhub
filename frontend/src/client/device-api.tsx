import axios, { AxiosInstance } from 'axios';
import { Device } from '../interfaces/data.interface';

import baseUrls from './urls';

interface DeviceStatus {
    status: string;
}

class DeviceApi {

    async getAll(): Promise<Device[] | []> {
        try {
            const response = await axios.get<Device[] | []>(`${baseUrls.deviceService}/`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async delete(id: number): Promise<void> {
        try {
            await axios.delete(`/${id}`);
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async get(id: string): Promise<Device> {
        try {
            const response = await axios.get<Device>(`${baseUrls.deviceService}/${id}`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async getIp(id: string): Promise<string> {
        try {
            const response = await axios.get<string>(`${baseUrls.deviceService}/${id}/ip_address`);
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async getStatus(id: string): Promise<string> {
        try {
            const response = await axios.get<DeviceStatus>(`${baseUrls.deviceService}/${id}/status`);
            return response.data.status;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    protected handleError(error: any) {
        if (axios.isAxiosError(error)) {
            console.log('Catched axios error: ', error)
        }
    }

}

const DeviceService = new DeviceApi();
export default DeviceService;
