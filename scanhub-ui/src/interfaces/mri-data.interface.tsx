// Collection of MRI modality related data interfaces
import Plotly from 'plotly.js'

// export interface MRISequence {    // replaced with definition from generated client
//   _id: string
//   name: string
//   description?: string | null
//   sequence_type?: string | null
//   created_at?: Date | null
//   updated_at?: Date | null
//   tags?: [string] | []
//   file?: File | null
//   file_extension?: string
// }

export interface FileResponse {
  filename: string
  contentType: string
  content: Blob
}

export interface PlotData {
  layout: Plotly.Layout
  data: Plotly.Data[]
}
