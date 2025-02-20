/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ConfirmDeleteModal.tsx is responsible for rendering a modal with an interface
 * to confirm the deletion of some item.
 */
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import * as React from 'react'

import { ModalPropsModify } from '../interfaces/components.interface'


function ConfirmDeleteForm(props: ModalPropsModify<string>) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        Are you sure you want to delete user "{props.item}"?
      </Typography>
      <Stack direction='row' spacing={3}>
        <Button
          size='sm'
          color='danger'
          sx={{  }}
          onClick={(event) => {
            props.onSubmit()
            props.setOpen(false)
          }}
        >
          Delete Now
        </Button>

        <Button
          size='sm'
          sx={{  }}
          onClick={(event) => {
            props.setOpen(false)
          }}
        >
          No, take me back...
        </Button>
      </Stack>
    </>
  )
}


export default function ConfirmDeleteModal(props: ModalPropsModify<string>) {
  return (
    <Modal
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        <ConfirmDeleteForm {...props} />
      </ModalDialog>
    </Modal>
  )
}
