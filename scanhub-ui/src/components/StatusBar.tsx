/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Navigation.tsx is responsible for rendering the navigation bar at the top of the page.
 */
import React from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'

import Box from '@mui/joy/Box'
import Chip from '@mui/joy/Chip'
import LinkIcon from '@mui/icons-material/Link';
import IconButton from '@mui/joy/IconButton'
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Typography from '@mui/joy/Typography'
import Tooltip from '@mui/joy/Tooltip'
import { ClickAwayListener } from '@mui/base';

import { deviceApi } from '../api'
import { DeviceOut } from '../openapi/generated-client/device/api'
import Sheet from '@mui/joy/Sheet'
import { useManagerHealthCheck } from '../hooks/useManagerHealthCheck'
import {
  patientManagerHealthApi,
  examManagerHealthApi,
  workflowManagerHealthApi,
  userLoginManagerHealthApi,
  deviceManagerHealthApi
} from '../api'
import CircularProgress from '@mui/joy/CircularProgress'
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';



// Device all health cheks
const healthChecks = [
  {
    name: 'Patient Manager',
    useHook: () => useManagerHealthCheck(
      'patientManagerHealthCheck',
      () => patientManagerHealthApi.readinessApiV1PatientHealthReadinessGet({ timeout: 1000 }).then(r => r.data),
      'patient-manager'
    )
  },
  {
    name: 'Exam Manager',
    useHook: () => useManagerHealthCheck(
      'examManagerHealthCheck',
      () => examManagerHealthApi.readinessApiV1ExamHealthReadinessGet({ timeout: 1000 }).then(r => r.data),
      'exam-manager'
    )
  },
    {
    name: 'Workflow Manager',
    useHook: () => useManagerHealthCheck(
      'workflowManagerHealthCheck',
      () => workflowManagerHealthApi.readinessApiV1WorkflowmanagerHealthReadinessGet({ timeout: 1000 }).then(r => r.data),
      'workflow-manager'
    )
  },
    {
    name: 'User Login Manager',
    useHook: () => useManagerHealthCheck(
      'userLoginManagerHealthCheck',
      () => userLoginManagerHealthApi.readinessApiV1UserloginHealthReadinessGet({ timeout: 1000 }).then(r => r.data),
      'user-login-manager'
    )
  },
  {
    name: 'Device Manager',
    useHook: () => useManagerHealthCheck(
      'deviceManagerHealth',
      () => deviceManagerHealthApi.readinessApiV1DeviceHealthReadinessGet({ timeout: 1000 }).then(r => r.data),
      'device-manager'
    )
  } 
]

function ManagerStatus() {

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: '1fr auto', // left column flexible, right column auto-sized
        rowGap: 1,                       // vertical spacing between rows
        columnGap: 2,                    // horizontal spacing
        alignItems: 'center',            // vertical centering per row
        p: 2
      }}
    >
      {
        healthChecks.map(({ name, useHook }, index) => {
          const { isHealthy, isLoading } = useHook();
          return (
            <React.Fragment key={`manager-healt-check-${index}`}>
              <Typography level='body-xs'>{name}</Typography>
              {
                isLoading ? <CircularProgress /> :
                  <Chip
                    size="sm"
                    color={isHealthy ? 'success' : 'danger'}
                    variant="solid"
                    sx={{ mr: 1 }}
                  >
                    {isHealthy ? 'Healthy' : 'Unhealthy'}
                  </Chip>
              }
            </React.Fragment>
          );
        })
      }
    </Box>
  )
}

export default function StatusBar() {

  const queryClient = useQueryClient()

  const [tooltipHovered, setTooltipHovered] = React.useState(false);
  const [tooltipPinned, setTooltipPinned] = React.useState(false);
  const tooltipOpen = tooltipHovered || tooltipPinned

  const anyUnhealthy = healthChecks.map(({ useHook }) => useHook()).some(r => !r.isLoading && !r.isHealthy)

  const selectedDeviceId = queryClient.getQueryData<string | null>(['selectedDeviceId'])
  const setSelectedDeviceId = (id: string | null) => queryClient.setQueryData(['selectedDeviceId'], id)

  // Get list of all devices
  const { data: devices } = useQuery<DeviceOut[]>({
    queryKey: ['devices'],
    queryFn: async () => {
      const result = await deviceApi.getDevicesApiV1DeviceGet()
      return result.data
    },
  })

  // Poll only the selected device, but more frequently to get updated device status
  const { data: deviceStatus } = useQuery<DeviceOut>({
    queryKey: ['deviceStatus', selectedDeviceId], // depends on selected device
    queryFn: async () => {
      if (!selectedDeviceId) throw new Error('No device selected')
      // Call your API to get this device’s latest status
      const result = await deviceApi.getDeviceApiV1DeviceDeviceIdGet(selectedDeviceId)
      return result.data
    },
    enabled: !!selectedDeviceId,     // only run when a device is selected
    refetchInterval: 1000,         // poll every second
    refetchIntervalInBackground: true,
  })

  return (
    <Sheet
      variant='solid'
      color='primary'
      sx={{
        height: 'var(--Status-height)',
        gap: 0,
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingRight: 2,
        paddingLeft: 2,
        alignItems: 'center',
        position: 'sticky', // or "fixed" if you always want it visible
        bottom: 0,  // stick to the bottom instead of top
        zIndex: 'snackbar', // keep above main content, below snackbar
      }}
    >
      {
        devices && <Select
          variant='solid'
          color='primary'
          value={selectedDeviceId || null}
          onChange={(_, newValue) => setSelectedDeviceId(newValue)}
          placeholder="Select a device..."
          renderValue={(selected) => {
            if (!selected) return '-'
            const device = devices?.find(d => d.id === selected.value)
            return device ? `${device.name}: ${deviceStatus?.status ?? device.status ?? '-'}` : '-'
          }}
          sx={{
            minHeight: 0,
            height: 'var(--Status-height)',
            fontSize: 'sm',
          }}
          slotProps={{
            listbox: {
              variant: 'outlined',
              color: 'neutral',
            },
            indicator: {
              sx: {
                order: -1, // move indicator to the start
                marginRight: '0.5rem',
                marginLeft: '-0.5rem'
              },
            },
          }}
        >
          {
            devices.map((device) => (
              <Option key={device.id} value={device.id} variant='plain' color='neutral'>
                {device.name}
              </Option>
            ))
          }
        </Select>
      }

      <ClickAwayListener onClickAway={() => { if (tooltipPinned) setTooltipPinned(false) }}>
        <Tooltip
          placement='bottom'
          variant='outlined'
          describeChild={false}
          arrow
          title={<ManagerStatus/>}
          open={tooltipOpen}
          modifiers={[
            { name: 'preventOverflow', options: { padding: 10 } }, // skidding=8 (down), distance=20 (further right)
          ]}
        >
          <IconButton
            variant='solid'
            color='primary'
            sx={{
              minHeight: 0,
              height: 'var(--Status-height)',
              ml: 'auto'
            }}
            onClick={() => setTooltipPinned(prev => !prev)}
            onMouseEnter={() => setTooltipHovered(true)}
            onMouseLeave={() => setTooltipHovered(false)}
          >
            {
              anyUnhealthy ? <ErrorOutlineIcon sx={{ fontSize: 'var(--Status-height)' }}/> :
                <LinkIcon sx={{ fontSize: 'var(--Status-height)' }} />
            }
          </IconButton>
        </Tooltip>
      </ClickAwayListener>
    </Sheet>
  )
}
