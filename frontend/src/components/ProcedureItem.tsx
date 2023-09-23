// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// ProcedureItem.tsx is responsible for rendering a single procedure item in the procedure list of the patient view.

import * as React from 'react'
import { Link as RouterLink } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'react-query'

// Mui joy components
import Box from '@mui/joy/Box'
import Typography from '@mui/joy/Typography'
import ListItem from '@mui/joy/ListItem'
import ListItemButton from '@mui/joy/ListItemButton'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import IconButton from '@mui/joy/IconButton'
import MoreHorizIcon from '@mui/icons-material/MoreHoriz'
import DescriptionSharpIcon from '@mui/icons-material/DescriptionSharp'
import ProcedureModal from '../components/ProcedureModal'

// Interfaces and api service
import { Procedure } from '../interfaces/data.interface'
import { ComponentProps } from '../interfaces/components.interface'
import client from '../client/exam-tree-queries'

function ProcedureItem({
  data: procedure,
  refetchParentData,
  isSelected,
}: ComponentProps<Procedure>) {
  const params = useParams()
  const navigate = useNavigate()

  // Context: Delete and edit options, anchor for context location
  const [contextOpen, setContextOpen] = React.useState<number | null>(null)
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null)
  const [procedureModalOpen, setProcedureModaalOpen] = React.useState(false)

  const handleContextClose = () => {
    setAnchorEl(null)
    setContextOpen(null)
  }

  const handleContextOpen = (e, procedureId) => {
    e.preventDefault()
    setAnchorEl(e.currentTarget)
    setContextOpen(procedureId)
  }

  const deleteProcedure = useMutation(async () => {
    await client.procedureService.delete(procedure.id).then(() => {
      navigate(`/patients/${params.patientId}/${params.examId}`)
      refetchParentData()
    })
  })

  const updateProcedure = useMutation(async (data: Procedure) => {
    console.log('Updating procedure... ', data)
    await client.procedureService
      .update(data.id, procedure)
      .then(() => {
        refetchParentData()
      })
      .catch((err) => {
        console.log('Error on procedure update: ', err)
      })
  })

  return (
    <ListItem>
      <ListItemButton
        id='procedure-item'
        component={RouterLink}
        // If procedureId exists, we redirect to this procedure id, otherwise procedure id is appended
        to={`/patients/${params.patientId}/${params.examId}/${procedure.id}`}
        selected={isSelected}
        variant={isSelected || procedure.id === contextOpen ? 'soft' : 'plain'}
      >
        <ListItemDecorator sx={{ align: 'center', justify: 'center' }}>
          <DescriptionSharpIcon />
        </ListItemDecorator>

        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
            <Typography>{procedure.name}</Typography>
            <IconButton
              variant='plain'
              sx={{ '--IconButton-size': '25px' }}
              onClick={(e) => handleContextOpen(e, procedure.id)}
            >
              <MoreHorizIcon />
            </IconButton>
          </Box>

          <Typography level='body-sm' textColor='text.tertiary'>{`Created: ${new Date(
            procedure.datetime_created,
          ).toDateString()}`}</Typography>
          <Typography level='body-sm' textColor='text.tertiary'>{`Updated: ${
            procedure.datetime_updated ? new Date(procedure.datetime_updated).toDateString() : '-'
          }`}</Typography>
        </Box>

        <Menu
          id='context-menu'
          variant='plain'
          anchorEl={anchorEl}
          open={procedure.id === contextOpen}
          onClose={() => handleContextClose()}
          sx={{ zIndex: 'snackbar' }}
        >
          <MenuItem
            key='edit'
            onClick={() => {
              setProcedureModaalOpen(true)
            }}
          >
            Edit
          </MenuItem>

          <MenuItem
            key='delete'
            onClick={() => {
              deleteProcedure.mutate()
            }}
          >
            Delete
          </MenuItem>
        </Menu>

        <ProcedureModal
          data={procedure}
          dialogOpen={procedureModalOpen}
          setDialogOpen={setProcedureModaalOpen}
          handleModalSubmit={(data: Procedure) => {
            updateProcedure.mutate(data)
          }}
        />
      </ListItemButton>
    </ListItem>
  )
}

export default ProcedureItem
