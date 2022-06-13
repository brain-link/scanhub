import { Link } from 'react-router-dom'
import React from 'react'

import { Device } from './Interfaces'

import {
    CCard,
    CCardTitle,
    CCardSubtitle,
    CCardBody,
    CTable,
    CTableBody,
    CTableDataCell,
    CTableHead,
    CTableRow,
    CTableHeaderCell,
    CNavLink,
} from '@coreui/react'

export function DeviceTable() {
  
    let [loading, setLoading] = React.useState(true);
    let [devices, setDevices] = React.useState<Device[]>([]);

    React.useEffect(() => {
        setLoading(true);
        const fetchData = async () => {
            const response = await fetch("http://localhost:8000/devices/");
            const data = await response.json();
            setDevices(data);
            setLoading(false);
        };

        fetchData();
    }, []);

  return (
    <CCard className='m-4'>
        <CCardBody className='m-2'>
            <CCardTitle>List of all Devices</CCardTitle>
            <CCardSubtitle className="mb-4 text-medium-emphasis">
                Devices
            </CCardSubtitle>

            <CTable hover borderless>
                <CTableHead color='dark'>
                    <CTableRow>
                        <CTableHeaderCell scope="col">ID</CTableHeaderCell>
                        <CTableHeaderCell scope="col">Modality</CTableHeaderCell>
                        <CTableHeaderCell scope="col">Address</CTableHeaderCell>
                        <CTableHeaderCell scope="col">Site</CTableHeaderCell>
                    </CTableRow>
                </CTableHead>
                <CTableBody>
                    {
                        !loading ? devices.map(device => (
                            <CTableRow key={device.id}>
                                <CTableHeaderCell scope="row">
                                    <CNavLink to={`/devices/${device.id}`} component={Link}>{device.id}</CNavLink>
                                </CTableHeaderCell>
                                <CTableDataCell>{device.modality}</CTableDataCell>
                                <CTableDataCell>{device.address}</CTableDataCell>
                                <CTableDataCell>{device.site}</CTableDataCell>
                            </CTableRow>
                        )) : null
                    }
                </CTableBody>
            </CTable>
        </CCardBody>
    </CCard>
  );
}
