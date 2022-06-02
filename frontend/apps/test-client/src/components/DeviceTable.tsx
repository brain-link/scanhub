import { NavLink } from 'react-router-dom'
import { graphql, useLazyLoadQuery } from 'react-relay'

import type { DeviceTableQuery } from './__generated__/DeviceTableQuery.graphql'

import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CBadge,
  CNavLink,
} from '@coreui/react'

const query = graphql`
  query DeviceTableQuery {
    allDevices {
      id,
      modality,
      address,
      site {
        name,
        city
      }
    }
  }
`

export function DeviceTable() {
  const { allDevices } = useLazyLoadQuery<DeviceTableQuery>(query, {}, {})
  return (
    <>
      <CTable hover borderless>
        <CTableHead color='dark'>
          <CTableRow>
            <CTableHeaderCell scope="col">ID</CTableHeaderCell>
            <CTableHeaderCell scope="col">Modality</CTableHeaderCell>
            <CTableHeaderCell scope="col">City</CTableHeaderCell>
            <CTableHeaderCell scope="col">Location</CTableHeaderCell>
            <CTableHeaderCell scope="col">Room</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {allDevices.map(device => (
            <CTableRow key={device.id}>
              <CTableHeaderCell scope="row">
              <CNavLink to={device.id} component={NavLink}>{device.id}</CNavLink>
              </CTableHeaderCell>
              <CTableDataCell>{device.modality}</CTableDataCell>
              {/* Device.site is possibly null -> need to be fixed in graphene/graphql query definition (server/scanhub/graphene) */}
              <CTableDataCell>{device.site.city}</CTableDataCell>
              <CTableDataCell>{device.site.name}</CTableDataCell>
              <CTableDataCell>{device.address}</CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </>
  )
}
