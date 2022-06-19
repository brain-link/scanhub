import { Link, useParams } from 'react-router-dom';
import { CContainer, CCol, CRow, CWidgetStatsF, CLink} from '@coreui/react';

import { useQuery } from 'react-query';
import { Procedure } from './Interfaces';

// import { CIcon } from '@coreui/icons-react';
// import { cilList } from '@coreui/icons';

export function Patient() {

  let params = useParams()

  const { data: procedures, isSuccess } = useQuery<Procedure[]>(`patients/${params.patientId}/procedures/`);

  if (!isSuccess) {
    return <div> Loading ... </div>
  }

  return (
    <>

      <CRow CRow className='m-2'>
        <h1> Patient { params.patientId } </h1> 
      </CRow>

      <CRow className='m-2'>
        <CCol xs={3}>
          {
            procedures?.map(procedure => (
              <CWidgetStatsF
                className="mb-3"
                color="primary"
                title={procedure.date}
                value={
                  <CLink to='test-procedure' component={ Link }> Procedure {procedure.id} </CLink>
                }
              />
            ))
          }
        </CCol>

        {/* <CCol md={9}>
          <CCard className='grow'>
            <Outlet />
          </CCard> 
        </CCol> */}

      </CRow>
    </>
  )
}