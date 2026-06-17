/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ExamItem.tsx is responsible for rendering a single protocol item.
 */
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useMutation } from '@tanstack/react-query'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import FolderIcon from '@mui/icons-material/Folder';
import Dropdown from '@mui/joy/Dropdown'
import Menu from '@mui/joy/Menu'
import MenuButton from '@mui/joy/MenuButton'
import IconButton from '@mui/joy/IconButton'
import MenuItem from '@mui/joy/MenuItem'

// Sub-components, interfaces, client
import { ProtocolOut } from '../openapi/generated-client/exam'
import { RefetchableItemInterface, SelectableItemInterface } from '../interfaces/components.interface'
import Box from '@mui/joy/Box'
import { examApi } from '../api'
import ExamModal from './ExamModal'
import Button from '@mui/joy/Button'


export default function ExamItem({ item: protocol, selection, onClick }: SelectableItemInterface<ProtocolOut>) {

  return (
    <Button
      sx={{
        width: '100%',
        p: 0.5,
        display: 'flex',
        justifyContent: 'flex-start'
      }}
      variant={(selection.type == 'protocol' && selection.itemId == protocol.id) ? 'outlined' : 'plain'}
      onClick={onClick}
    >
      <FolderIcon fontSize='small' />
      <Box
        sx={{
          marginLeft: 0.5,
          p: 0.5,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'start',
        }}
      >
        <Typography level='body-xs' textColor='text.tertiary'>
          PROTOCOL
        </Typography>

        <Typography level='title-sm'>
          {protocol.name}
        </Typography>

        <Typography level='body-xs' textColor='text.tertiary'>
          {`Created: ${new Date(protocol.datetime_created).toDateString()}`}
        </Typography>
      </Box>
    </Button>
  )
}


export function ExamMenu({ item: protocol, refetchParentData }: RefetchableItemInterface<ProtocolOut>) {

  const [examModalOpen, setExamModalOpen] = React.useState(false)

  const deleteProtocol = useMutation({
    mutationFn: async () => {
      await examApi
        .protocolDeleteApiV1ExamExamIdDelete(protocol.id)
        .then(() => {
          refetchParentData()
        })
    }
  })

  return (
    <>
      <Dropdown>
        <MenuButton slotProps={{ root: { size: 'sm', variant: 'plain' } }} sx={{ aspectRatio: '1 / 1', minWidth: 0, p: 0.5 }} slots={{ root: IconButton }}>
          <MoreHorizIcon fontSize='small' />
        </MenuButton>
        <Menu id='context-menu' variant='plain' sx={{ zIndex: 'snackbar' }}>
          <MenuItem key='edit' onClick={() => setExamModalOpen(true)}>
            Edit
          </MenuItem>
          <MenuItem
            key='delete'
            onClick={() => {
              deleteProtocol.mutate()
            }}
          >
            Delete
          </MenuItem>
        </Menu>
      </Dropdown>

      <ExamModal
        item={protocol}
        isOpen={examModalOpen}
        setOpen={setExamModalOpen}
        onSubmit={refetchParentData}
        modalType='modify'
      />
    </>
  )
}
