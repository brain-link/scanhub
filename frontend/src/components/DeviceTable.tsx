import { Link } from 'react-router-dom'
import React from 'react'

import { useQuery } from "react-query";
import { Device } from './Interfaces'

import {
    CCard,
    CCardTitle,
    CCardSubtitle,
    CSpinner,
    CCardHeader,
    CCardBody,
    CTable,
    CTableBody,
    CTableDataCell,
    CTableHead,
    CTableRow,
    CTableHeaderCell,
    CNavLink,
    CContainer,
} from '@coreui/react'

export function DeviceTable() {
  
    const { data: devices, isSuccess } = useQuery<Device[]>("devices/");

    if (!isSuccess) {
        // return <div> Loading... </div>;
        return (
            <CContainer>
                <CSpinner variant="grow"/>
            </CContainer>
        )
    }

    return (
        <CCard className='m-4'>
            <CCardHeader className="h5">Devices</CCardHeader>
            <CCardBody className='m-2'>

                {/* <CCardTitle>List of all Devices</CCardTitle>
                <CCardSubtitle className="mb-4 text-medium-emphasis">
                    Devices
                </CCardSubtitle> */}

                <CTable hover>
                    <CTableHead color='secondary'>
                        <CTableRow>
                            <CTableHeaderCell scope="col">ID</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Modality</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Address</CTableHeaderCell>
                            <CTableHeaderCell scope="col">Site</CTableHeaderCell>
                        </CTableRow>
                    </CTableHead>
                    <CTableBody>
                        {
                            devices?.map(device => (
                                <CTableRow align="middle" key={device.id}>
                                    <CTableHeaderCell scope="row">
                                        <CNavLink to={`/devices/${device.id}`} component={Link}>{device.id}</CNavLink>
                                    </CTableHeaderCell>
                                    <CTableDataCell>{device.modality}</CTableDataCell>
                                    <CTableDataCell>{device.address}</CTableDataCell>
                                    <CTableDataCell>{device.site}</CTableDataCell>
                                </CTableRow>
                            ))
                        }
                    </CTableBody>
                </CTable>
            </CCardBody>
        </CCard>
        );
    }
