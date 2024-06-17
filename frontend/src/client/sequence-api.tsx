import axios from 'axios'

import { MRISequence, PlotData } from '../interfaces/mri-data.interface'
import { ApiService } from './abstract-query-client'
import baseUrls from './urls'

class MRISequenceApiService extends ApiService<MRISequence> {
  constructor() {
    super(baseUrls.mriSequenceService)
  }

  async uploadSequenceFile(sequenceData: Partial<MRISequence>): Promise<MRISequence> {
    const formData = new FormData()
    Object.entries(sequenceData).forEach(([key, value]) => {
      formData.append(key, value)
    })

    try {
      const response = await this.axiosInstance.post('/upload', sequenceData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return response.data
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        this.handleError(error)
      }
      throw error
    }
  }

  async getSequencePlot(seqId: string): Promise<PlotData> {
    try {
      const response = await this.axiosInstance.get(`/mri-sequence-plot/${seqId}`)
      return JSON.parse(response.data)
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        this.handleError(error)
      }
      throw error
    }
  }

  async getSequenceMeta(seqId: string): Promise<MRISequence> {
    try {
      const response = await this.axiosInstance.get(`/${seqId}`)
      return response.data
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        this.handleError(error)
      }
      throw error
    }
  }
}

const mriSequenceService = new MRISequenceApiService()
export default mriSequenceService
