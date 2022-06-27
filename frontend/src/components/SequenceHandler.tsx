import { useMutation, useQuery } from "react-query"
import React, {useState, useEffect} from "react"
import axios from "axios"
import { useParams } from "react-router-dom"
import { CFormInput, CInputGroup, CCol, CInputGroupText, CButton, CRow } from "@coreui/react"
import Plot from 'react-plotly.js';
import { PlotData, Parameter } from "./Interfaces"


// This should be returned from backend via sequence id
const sequenceParameters = [
    {
        id: "tr",
        label: "Repetition Time (TR) in [ms]",
        value: 10
    },
    {
        id: "te",
        label: "Echo Time (TE) in [ms]",
        value: 5
    },
    {
        id: "n_ro",
        label: "Number of readouts",
        value: 256
    },
    {
        id: "n_pe",
        label: "Number of phase encoding steps",
        value: 128
    }
]

export function SequenceForm() {
    
    let params = useParams()

    const { data: plotData, isSuccess: isPlotData } = useQuery<PlotData[]>(`test_sequence/`)

    const mutation = useMutation(async(data: Parameter[]) => {
        return await axios.post(`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/${params.recordingId}/sequence/`, data)
    })

    if (mutation.isLoading && !isPlotData) {
        return <div> Loading... </div>
    }
    else {
        return (
            <CCol>
                
                <CRow className="me-2">
                    <Plot 
                        data={plotData} 
                        layout={{
                            margin: { l: 50, r: 50, t: 10, b: 50 },
                            autosize: true,
                            xaxis: {
                                ticks: 'outside',
                                title: "Time [ms]",
                                rangeslider: { autorange: true }
                            },
                            yaxis: { domain: [0.0, 0.15] },
                            yaxis2: { domain: [0.2, 0.35] },
                            yaxis3: { domain: [0.4, 0.55] },
                            yaxis4: { domain: [0.6, 0.75] },
                            yaxis5: { domain: [0.8, 0.95] }
                        }}
                    />
                </CRow>
                {
                    sequenceParameters.map(parameter => (
                        <CInputGroup className="mb-2">
                            <CInputGroupText>{parameter.label}</CInputGroupText>
                            <CFormInput 
                                type={parameter.id}
                                defaultValue={parameter.value}
                                onChange={e => {parameter.value = Number(e.target.value)}}
                            />
                        </CInputGroup>
                    ))
                }

                <CButton 
                    color="primary"
                    onClick={ () => { mutation.mutate(sequenceParameters) } }
                >
                    Submit
                </CButton>

            </CCol>
        )
    }
}