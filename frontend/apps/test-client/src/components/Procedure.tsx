import { Link, NavLink, Outlet, useParams } from 'react-router-dom'
import { range } from 'utils'
import { getModalityComponent } from './modalities'

export function ProcedureSidebar() {
  const { procedureId } = useParams()
  return (
    <section className='flex-col gap-2' style={{ minWidth: '20rem', width: '30%', maxWidth: '30rem' }}>
      <div className='flex gap-2'>
        <input type='search' className='grow' placeholder={`Search ${procedureId}`} />
        <button>
          <span className='fa fa-filter' />
        </button>
      </div>
      <div className='grow flex-col gap-2 pad-2 scroll-y'>
        {range(50).map(i => (
          <Link key={i} to={`mri-recording-${i}`}>
            <section className='flex gap-2'>
              <time dateTime='placeholder'>00:00</time>
              <img src={`https://picsum.photos/64?i=${i}`} loading='lazy' width={64} height={64} />
              <h1>MRI</h1>
              <p>Some description</p>
            </section>
          </Link>
        ))}
      </div>
      <div className='flex gap-2 justify-end'>
        <button><span className='fa fa-circle' /> REC</button>
        <button><span className='fa fa-plus' /> MRI</button>
        <button><span className='fa fa-plus' /> CT</button>
        <button><span className='fa fa-plus' /> EEG</button>
      </div>
    </section>
  )
}


export function ProcedureMainContentSwitcher() {
  return (
    <>
      <div className='flex gap-2'>
        <NavLink to='configure-mri'>Config</NavLink>
        <NavLink to='dicom'>DICOM</NavLink>
      </div>
      <Outlet />
    </>
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
    <div className='grow flex gap-3'>
      <ProcedureSidebar />
      <section className='grow'>
        <Outlet />
      </section>
    </div>
  )
}
