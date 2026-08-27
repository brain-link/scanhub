/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ProtocolInfo.tsx is responsible for rendering additional information of a protocol item.
 */
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
import React from 'react'

import { ProtocolOut } from '../openapi/generated-client/protocol'


function ProtocolInfo({ protocol }: { protocol: ProtocolOut }) {

  const datetime_created = new Date(protocol.datetime_created)
  const datetime_updated = protocol.datetime_updated ? new Date(String(protocol.datetime_updated)) : undefined

  return (
    <Box sx={{display: 'flex', alignItems: 'stretch'}}>
      <Box
        sx={{
          rowGap: 0.4,
          columnGap: 4,
          p: 2,
          display: 'grid',
          gridTemplateColumns: 'auto 1fr',
          '& > *:nth-of-type(odd)': {
            color: 'text.secondary',
          },
        }}
      >
        <Typography fontSize='sm'>Name</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.name}
        </Typography>

        <Typography fontSize='sm'>Description</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.description}
        </Typography>

        <Typography fontSize='sm'>Indication</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.indication ? String(protocol.indication) : '-'}
        </Typography>

        <Typography fontSize='sm'>Comment</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.comment ? String(protocol.comment) : '-'}
        </Typography>

        <Typography fontSize='sm'>Status</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.status}
        </Typography>

        <Typography fontSize='sm'>Is Template</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.is_template ? 'True' : 'False'}
        </Typography>

        <Typography fontSize='sm'>ID</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.id}
        </Typography>

        <Typography fontSize='sm'>Creator</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {protocol.creator}
        </Typography>

        <Typography level='body-sm'>Last update</Typography>
        <Typography level='body-sm' textColor='text.primary'>
          {
            datetime_updated ? datetime_updated.toLocaleDateString() + ', ' + datetime_updated.toLocaleTimeString()
            : datetime_created.toLocaleDateString() + ', ' + datetime_created.toLocaleTimeString()
          }
        </Typography>
      </Box>
    </Box>
  )
}

export default ProtocolInfo
