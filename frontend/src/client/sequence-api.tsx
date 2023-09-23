import baseUrls from './urls'

import { ApiService } from './abstract-query-client'
import { PlotData, MRISequence } from '../interfaces/mri-data.interface'

class MRISequenceApiService extends ApiService<MRISequence> {
  constructor() {
    super(baseUrls.mriSequenceService)
  }

  async uploadSequenceFile(sequence_data: Partial<MRISequence>): Promise<MRISequence> {
    const formData = new FormData()
    Object.entries(sequence_data).forEach(([key, value]) => {
      formData.append(key, value)
    })

    try {
      const response = await this.axiosInstance.post('/upload', sequence_data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  async getSequencePlot(seq_id: string): Promise<PlotData> {
    try {
      const response = await this.axiosInstance.get(`/mri-sequence-plot/${seq_id}`)
      return JSON.parse(response.data)
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }

  async getSequenceMeta(seq_id: string): Promise<MRISequence> {
    try {
      const response = await this.axiosInstance.get(`/${seq_id}`)
      return response.data
    } catch (error) {
      this.handleError(error)
      throw error
    }
  }
}

const mriSequenceService = new MRISequenceApiService()
export default mriSequenceService
