/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * AcquisitionControl.tsx is responsible for rendering the acquisition trigger and process.
 */
import PlayCircleIcon from '@mui/icons-material/PlayCircle'
import StopCircleIcon from '@mui/icons-material/StopCircle';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import Box from '@mui/joy/Box'
import IconButton from '@mui/joy/IconButton'
import LinearProgress from '@mui/joy/LinearProgress'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'
import { useMutation } from '@tanstack/react-query'

import { workflowManagerApi } from '../api'
import { ItemStatus } from '../generated-client/exam'
import { ItemSelection } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


function AcquisitionControl({ itemSelection, openConfirmModal }: { 
  itemSelection: ItemSelection, openConfirmModal: (onConfirmed: () => void) => void
}){
  const [, showNotification] = React.useContext(NotificationContext)
  const hasTriggeredRef = React.useRef(false)

  const processTaskMutation = useMutation({
    mutationKey: ['workflowManagerProcessTask'],
    mutationFn: async () => {
      if (hasTriggeredRef.current) return
      hasTriggeredRef.current = true
      try {
        await workflowManagerApi.triggerTaskApiV1WorkflowmanagerTriggerTaskTaskIdPost(
          (itemSelection.itemId as string)
        )
        showNotification({message: 'Started task', type: 'success'})
      } catch {
        showNotification({message: 'Error at starting task.', type: 'warning'})
      } finally {
        hasTriggeredRef.current = false
      }
    },
  })

  let actionIcon = <PlayCircleIcon />
  if (itemSelection.status == ItemStatus.Started) actionIcon = <StopCircleIcon />
  if (itemSelection.status == ItemStatus.Finished) actionIcon = <CheckCircleIcon />

  return (
    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
      <IconButton 
        size='sm' 
        variant='plain' 
        color={'neutral'}
        disabled={processTaskMutation.isPending}
        onClick={() => {
          openConfirmModal(() => {
            // By now, only tasks can be executed
            if (itemSelection.itemId == undefined) {
              showNotification({message: 'No item selected!', type: 'warning'})
            } else if (itemSelection.type == 'DAG' || itemSelection.type == 'ACQUISITION') {
              if (!processTaskMutation.isPending){
                processTaskMutation.mutate()
              }
            } else {
              // TODO: Trigger acquisition start with selected exam (= workflow list) or single workflow
              showNotification({message: 'Acquisition trigger not implemented for this item type!', type: 'warning'})
            }
          })
        }}
      >
        {actionIcon}
      </IconButton>

      <Stack direction='column' sx={{ flex: 1 }}>
        <Typography level='title-sm'>
          {itemSelection.type ? 
            'Execute ' + itemSelection.type + ' "' + itemSelection.name + '"'
          : 
            'Select item to start...'}
        </Typography>
        <Typography level='body-xs'>{'ID: ' + itemSelection.itemId}</Typography>
        <LinearProgress 
          determinate value={itemSelection.progress}
          sx={{marginTop: 1}}
          color={itemSelection.status == ItemStatus.Finished ? 'success' : 'primary'}
        />
      </Stack>
    </Box>
  )
}

export default AcquisitionControl
