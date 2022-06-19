import { useParams } from 'react-router-dom';
import { 
  CListGroup,
  CListGroupItem,
  CBadge,
  CCol, 
  CRow, 
  CCard, 
  CCardHeader, 
  CCardBody} from '@coreui/react';

import { useQuery } from 'react-query';
import { Procedure, Patient } from './Interfaces';


export function PatientIndex() {

  let params = useParams()

  const { data: procedures, isSuccess: procedureSuccess } = useQuery<Procedure[]>(`patients/${params.patientId}/procedures/`);
  const { data: patient, isSuccess: patientSuccess } = useQuery<Patient>(`patients/${params.patientId}/`);
  
  if (!procedureSuccess || !patientSuccess) {
    return <div> Loading ... </div>
  }

  return (
    <>
      <CRow className="m-2">
        <CCol xs={4}>
          <CCard>
            <CCardHeader className="h5">Patient</CCardHeader>
            <CCardBody>
              <CListGroup>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>ID</h6>
                    {patient?.id}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Birthday</h6>
                    {patient?.birthday}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Sex</h6>
                    {patient?.sex}
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Number of Procedures</h6>
                    <CBadge color="primary" shape="rounded-pill">
                      {procedures.length}
                    </CBadge>
                  </div>
                </CListGroupItem>
                <CListGroupItem className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6>Concern</h6>
                    {patient?.concern}
                  </div>
                </CListGroupItem>
              </CListGroup>
            </CCardBody>
          </CCard>
        </CCol>

        <CCol xs={8}>
          <CCard>
            <CCardHeader className="h5">Procedures</CCardHeader>
            <CCardBody>
              <CListGroup>
                {
                  procedures?.map(procedure => (
                    <CListGroupItem component='a' href={`${patient.id}/${procedure.id}`}>
                      <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1">Procedure {procedure.id}</h5>
                        <small>{procedure.date}</small>
                      </div>
                      <p className="mb-1">
                        Description of the procedure, that contains information about the modalities, number of records, etc.
                      </p>
                      {/* <small>Donec id elit non mi porta.</small> */}
                    </CListGroupItem>
                  ))
                }
              </CListGroup>

              {/* <CRow className='m-2'>
                <CCol>
                  {
                    procedures?.map(procedure => (
                      <CWidgetStatsF
                        // className="mb-3"
                        color="primary"
                        title={procedure.date}
                        value={
                          <CLink to='test-procedure' component={ Link }> Procedure {procedure.id} </CLink>
                        }
                      />
                    ))
                  }
                </CCol>
              </CRow> */}

            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}