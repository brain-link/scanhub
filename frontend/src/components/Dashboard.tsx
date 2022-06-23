import {
    CCard,
    CCardHeader,
    CCardBody,
    CCardTitle
} from "@coreui/react"


export function Dashboard() {
    return (
        <>
            <CCard className='m-4'>
                <CCardHeader className="h5">Dashboard</CCardHeader>
                <CCardBody className='m-2 text-center'>
                    <img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="400" height="200" alt="ScanHub"/>
                </CCardBody>
            </CCard>
        </>
    );
}