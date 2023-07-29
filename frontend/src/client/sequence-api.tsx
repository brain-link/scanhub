import baseUrls from './urls';

import { ApiService } from './abstract-query-client';
import { PlotData, MRISequence } from '../interfaces/mri-data.interface';


class MRISequenceApiService extends ApiService<MRISequence> {
    constructor() {
      super(baseUrls.mriSequenceService);
    }

    // Additional upload function is required for sequence upload
    // TODO: Needs to be tested
    async uploadFile(file: File, sequence_meta: Partial<MRISequence>): Promise<MRISequence> {
       
        const formData = new FormData();

        formData.append('file', file);
        Object.entries(sequence_meta).forEach(([key, value]) => {
            formData.append(key, value);
        });

        try {
            const response = await this.axiosInstance.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async getSequencePlot(seq_id: string): Promise<PlotData> {
        try {
            const response = await this.axiosInstance.get(`/mri-sequence-plot/${seq_id}`)
            return JSON.parse(response.data);
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async getSequenceMeta(seq_id: string): Promise<MRISequence> {
        try {
            const response = await this.axiosInstance.get(`/${seq_id}`)
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

}

const mriSequenceService = new MRISequenceApiService();
export default mriSequenceService;