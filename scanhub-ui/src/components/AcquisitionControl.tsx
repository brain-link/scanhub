/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionControl.tsx is responsible for rendering the acquisition trigger and process.
 */
import PlayCircleIcon from '@mui/icons-material/PlayCircle'
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { ItemSelection } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function AcquisitionControl({ itemSelection } : { itemSelection: ItemSelection }) {
  const [, showNotification] = React.useContext(NotificationContext)

  return (
    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
      <IconButton 
        size='sm' 
        variant='plain' 
        color='neutral'
        onClick={() => {
          if (itemSelection.itemId == undefined) {
            showNotification({message: 'No item selected!', type: 'warning'})
          } else {
            // TODO: Trigger acquisition start with selected exam (= workflow list) or single workflow
            showNotification({message: 'Acquisition trigger not implemented!', type: 'warning'})
          }
        }}
      >
        <PlayCircleIcon />
      </IconButton>

      <Stack direction='column' spacing={1} sx={{ flex: 1 }}>
        <Typography level='title-sm'>Execute: Exam</Typography>
        <LinearProgress determinate value={60} />
      </Stack>
    </Box>
  )
}

export default AcquisitionControl
