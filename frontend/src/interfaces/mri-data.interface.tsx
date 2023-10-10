// Collection of MRI modality related data interfaces
import Plotly from 'plotly.js'

export interface MRISequence {
  _id: string
  name: string
  description?: string | null
  sequence_type?: string | null
  created_at?: Date | null
  updated_at?: Date | null
  tags?: [string] | []
  file?: string | null
  file_extension?: string
}

export interface FileResponse {
  filename: string
  contentType: string
  content: Blob
}

export interface PlotData {
  layout: Plotly.Layout
  data: Plotly.Data[]
}
