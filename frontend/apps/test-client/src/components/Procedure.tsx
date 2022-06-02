import { Link, NavLink, Outlet, useParams } from 'react-router-dom'
import { range } from 'utils'
import { getModalityComponent } from './modalities'

import {
  CCard,
  CCol,
  CRow,
  CCardBody,
  CCardImage,
  CCardText,
  CCardTitle,
  CNav,
  CNavItem,
  CNavLink
} from '@coreui/react'

async function startRecording() {
  await fetch(
    'http://localhost:81/api/TriggerAcquisition?cmd=MEAS_START',
    {
      mode: 'no-cors',
    }
  )
}

export function ProcedureSidebar() {
  const { procedureId } = useParams()
  return (
    <div className='grow flex-col scroll-y'>
      {range(50).map(i => (
        <Link key={i} to={`mri-recording-${i}`}>
          <section className='flex'>

            <CCard className='m-2' style={{ maxWidth: '500px' }}>
              <CRow className="g-0">

                <CCol md={4}>
                <CCardImage component="svg" orientation="top" width="100%" height="100" role="img" aria-label="Placeholder">
                  <title>Placeholder</title><rect width="100%" height="100%" fill="#868e96"></rect>
                </CCardImage>
                </CCol>
                <CCol md={8}>
                  <CCardBody>
                    <CCardTitle>MRI Exam {i+1}</CCardTitle>
                    <CCardText>Exam description</CCardText>
                  </CCardBody>
                </CCol>
              </CRow>
            </CCard>

            {/* <time dateTime='placeholder'>00:00</time>
            <img src={`https://picsum.photos/64?i=${i}`} loading='lazy' width={64} height={64} />
            <h1>MRI</h1>
            <p>Some description</p> */}
          </section>
        </Link>
      ))} 
    </div>
    
    // <section className='flex-col' style={{ minWidth: '20rem', width: '30%', maxWidth: '30rem' }}>
    //   <div className='flex'>
    //     <input type='search' className='grow' placeholder={`Search ${procedureId}`} />
    //     <button>
    //       <span className='fa fa-filter' />
    //     </button>
    //   </div>
    //   <div className='grow flex-col scroll-y'>
    //     {range(50).map(i => (
    //       <Link key={i} to={`mri-recording-${i}`}>
    //         <section className='flex'>

    //           <CCard className='m-2' style={{ maxWidth: '500px' }}>
    //             <CRow className="g-0">

    //               <CCol md={4}>
    //               <CCardImage component="svg" orientation="top" width="100%" height="120" role="img" aria-label="Placeholder">
    //                 <title>Placeholder</title><rect width="100%" height="100%" fill="#868e96"></rect>
    //               </CCardImage>
    //               </CCol>
    //               <CCol md={8}>
    //                 <CCardBody>
    //                   <CCardTitle>MRI Exam {i+1}</CCardTitle>
    //                   <CCardText>This is some information about the MRI exam.</CCardText>
    //                 </CCardBody>
    //               </CCol>
    //             </CRow>
    //           </CCard>

    //           {/* <time dateTime='placeholder'>00:00</time>
    //           <img src={`https://picsum.photos/64?i=${i}`} loading='lazy' width={64} height={64} />
    //           <h1>MRI</h1>
    //           <p>Some description</p> */}
    //         </section>
    //       </Link>
    //     ))}
    //   </div>
    //   <div className='flex gap-2 justify-end'>
    //     <button onClick={startRecording}><span className='fa fa-circle' /> REC</button>
    //     <button><span className='fa fa-plus' /> MRI</button>
    //     <button><span className='fa fa-plus' /> CT</button>
    //     <button><span className='fa fa-plus' /> EEG</button>
    //   </div>
    // </section>
  )
}


export function ProcedureMainContentSwitcher() {
  return (
    <>
      <CNav variant='pills' className='mb-2'>
        <CNavItem>
          <CNavLink to='configure-mri' component={NavLink}>Config</CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink to='dicom' component={NavLink}>View</CNavLink>
        </CNavItem>
      </CNav>
      <Outlet />
    </>

    // <>
    //   <div className='flex gap-2'>
    //     <NavLink to='configure-mri'>Config</NavLink>
    //     <NavLink to='dicom'>DICOM</NavLink>
    //   </div>
    //   <Outlet />
    // </>
  )
}

export function ProcedureMainContent() {
  const { recordingId, modality } = useParams()
  const Modality = getModalityComponent(modality ?? 'configure-mri')
  if (recordingId === undefined) {
    throw new Error(`Error in routing, recordingId is undefined.`)
  }
  return (
    <Modality recordingId={recordingId} />
  )
}

export function Procedure() {
  return (
   
    <CRow className='m-1 mt-4'>
      <CCol md={3}>
        <CCard>
          <ProcedureSidebar />
        </CCard>  
      </CCol>
      <CCol md={9}>
        <CCard className='grow p-3'>
          <Outlet />
        </CCard> 
      </CCol>
    </CRow>

    // <div className='grow flex gap-3'>
    //   <ProcedureSidebar />
    //   <section className='grow'>
    //     <Outlet />
    //   </section>
    // </div>
  )
}
