import { useMutation } from "react-query"
import React, {useState, useEffect} from "react"
import axios from "axios"
import { useParams } from "react-router-dom"
import { CFormInput, CInputGroup, CCol, CInputGroupText, CButton } from "@coreui/react"

interface Parameter {
    id: string,
    label: string,
    value: number
}

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

    const mutation = useMutation(async(data: Parameter[]) => {
        return await axios.post(`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/${params.recordingId}/sequence/`, data)
    })

    if (mutation.isLoading) {
        return <div> Loading... </div>
    }
    else {
        return (
            <CCol>
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