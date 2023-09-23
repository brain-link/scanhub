import axios from 'axios';
import { Job } from '../interfaces/data.interface';

import baseUrls from './urls';


class AcquisitionControlApi {
    async post(data: Job) {
        try {
            const response = await axios.post(`${baseUrls.acquisitionControlService}/start-scan`, data, {
                headers: {
                'Content-Type': 'application/json'
                }
            })
            return response.data;
        }
        catch (error) {
            if (axios.isAxiosError(error)) {
                console.log('Catched axios error: ', error)
            }
        }
    }
}

const AcquisitionControl = new AcquisitionControlApi();
export default AcquisitionControl;
