import { Link, useParams } from 'react-router-dom';
import { CContainer, CCol, CRow, CWidgetStatsF, CLink} from '@coreui/react';

// import { CIcon } from '@coreui/icons-react';
// import { cilList } from '@coreui/icons';

export function Patient() {
  let params = useParams()
  return (
    <>

      <CRow CRow className='m-2'>
        <h1> Patient { params.patientId } </h1> 
      </CRow>

      <CRow className='m-2'>
        <CCol xs={3}>
          <CWidgetStatsF
            className="mb-3"
            color="primary"
            // icon={<CIcon icon={cilList} height={24} />}
            title="Procedure"
            value={
              <CLink to='test-procedure' component={ Link }> Procedure 1 </CLink>
            }
          />
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