// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// Device.tsx is responsible for rendering a device item.

import * as React from 'react'
import Typography from '@mui/joy/Typography'
import Sheet from '@mui/joy/Sheet'
import Stack from '@mui/joy/Stack'
import Badge from '@mui/joy/Badge'

import { Device } from '../interfaces/data.interface'
import deviceClient from '../client/device-api'

interface DeviceItemProps {
  device: Device | undefined
}

function DeviceItem({ device }: DeviceItemProps) {
  const [status, setStatus] = React.useState('')

  React.useEffect(() => {
    if (device) {
      deviceClient.getStatus(device.id).then((response) => {
        setStatus(response)
      })
    }
  })

  const getStatusBadgeColor = () => {
    switch (status) {
      case 'connected':
        return 'success'
      case 'disconnected':
        return 'danger'
      default:
        return 'neutral'
    }
  }

  if (!device) {
    return <div>Device not found</div>
  }

  return (
    <React.Fragment>
      <Sheet
        sx={{
          bgcolor: 'background.level1',
          borderRadius: 'sm',
          p: 1.5,
          rowGap: 0,
          columnGap: 4,
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          '& > *:nth-child(odd)': {
            color: 'text.secondary',
          },
        }}
      >
        <Typography noWrap level='body-sm' fontWeight='lg'>
          {' '}
          Device{' '}
        </Typography>
        <Typography level='body-sm'>{device.name}</Typography>

        <Typography noWrap level='body-sm' fontWeight='lg'>
          {' '}
          Modality{' '}
        </Typography>
        <Typography level='body-sm'>{device.modality}</Typography>

        {/* <Typography level="body-md" fontWeight="lg"> Manufacturer </Typography>
                    <Typography>{ device.manufacturer }</Typography>

                    <Typography level="body-md" fontWeight="lg"> Site </Typography>
                    <Typography>{ device.site }</Typography> */}

        <Typography noWrap level='body-sm' fontWeight='lg'>
          {' '}
          Status{' '}
        </Typography>
        <Stack direction='row' gap={1.5}>
          <Badge size='sm' badgeInset='50%' color={getStatusBadgeColor()} sx={{ ml: 0.5 }} />
          <Typography noWrap level='body-sm'>
            {status}
          </Typography>
          {/* <Typography noWrap level="body-sm">{`(IP: ${device.ip_address})`}</Typography> */}
        </Stack>

        {/* Do display ip below status, add empty div before status serving as empty grid item */}
        <div></div>
        <Typography noWrap level='body-sm'>{`(IP: ${device.ip_address})`}</Typography>

        {/* <Typography level="body-sm" fontWeight="lg"> Created </Typography>
                    <Typography level="body-sm">{ `${new Date(device.datetime_created).toDateString()}` }</Typography> */}

        <Typography noWrap level='body-sm' fontWeight='lg'>
          {' '}
          Updated{' '}
        </Typography>
        <Typography noWrap level='body-sm'>{`${
          device.datetime_updated ? new Date(device.datetime_updated).toDateString() : '-'
        }`}</Typography>
      </Sheet>
    </React.Fragment>
  )
}

export default DeviceItem
