/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * ProtocolModal.tsx is responsible for rendering a modal with an interface
 * to create a new protocol or modify an existing protocol.
 */
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import React from 'react'
import { useMutation, UseMutationResult } from '@tanstack/react-query'

import { protocolApi } from '../api'
import { BaseProtocol, ProtocolOut } from '../openapi/generated-client/protocol'
import { ModalPropsCreate, ModalPropsCreateModifyFromTemplate, ModalPropsModify } from '../interfaces/components.interface'
import NotificationContext from '../NotificationContext'


const formContent: {key: keyof BaseProtocol, label: string, placeholder: string, editForTemplates: boolean, required: boolean}[] = [
  { key: 'name', label: 'Protocol Name', placeholder: 'Name of the protocol', editForTemplates: true, required: true },
  { key: 'description', label: 'Description', placeholder: 'What is included in the examination', editForTemplates: true, required: true },
  { key: 'indication', label: 'Indication', placeholder: 'Why the examination is done', editForTemplates: false, required: false },
  { key: 'comment', label: 'Comment', placeholder: 'Any remarks about this specific execution of the examination', editForTemplates: false, required: false },
]


function ProtocolForm(props: ModalPropsCreate | ModalPropsModify<ProtocolOut> | ModalPropsCreateModifyFromTemplate<ProtocolOut>) {
  // The form is in this separate component to make sure that the state is reset after closing the modal

  const [, showNotification] = React.useContext(NotificationContext)

  const initialProtocol: BaseProtocol = props.modalType == 'modify' || props.modalType == 'createModifyFromTemplate' ?
    {...props.item, status: 'UPDATED'}
  :
    {
      patient_id: undefined,    // eslint-disable-line camelcase
      name: '',
      description: '',
      indication: undefined,
      comment: undefined,
      status: 'NEW',
      is_template: true,        // eslint-disable-line camelcase
    }

	const [protocol, setProtocol] = React.useState<BaseProtocol>(initialProtocol);

  let mutation: UseMutationResult<void, unknown, void, unknown>;
  if (props.modalType == 'modify') {
    mutation = useMutation({
      mutationFn: async () => {
        await protocolApi
        .updateProtocol(props.item!.id, protocol)   // props.item most not be and is not undefined here
        .then(() => {
          props.onSubmit()
          showNotification({message: 'Updated Protocol.', type: 'success'})
        })
      }
    })
  } else if (props.modalType == 'create') {
    mutation = useMutation({
      mutationFn: async () => {
        await protocolApi
        .createProtocol(protocol)
        .then(() => {
          props.onSubmit()
          showNotification({message: 'Created Protocol.', type: 'success'})
        })
      }
    })
  } else if (props.modalType == 'createModifyFromTemplate') {
    mutation = useMutation({
      mutationFn: async () => {
        await protocolApi
        .createProtocolFromTemplate(props.item.id, protocol)
        .then(() => {
          props.onSubmit()
          showNotification({message: 'Created Protocol from Template.', type: 'success'})
        })
      }
    })
  }

	let title = 'Default Protocol Modal';
  if (props.modalType == 'modify') title = 'Update Protocol';
  else if (props.modalType == 'create') title = 'Create New Protocol';
  else if (props.modalType == 'createModifyFromTemplate') title = 'Create Protocol From Template'

  return (
    <>
      <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
        {title}
      </Typography>

      <Stack spacing={1}>
        <Grid container rowSpacing={1.5} columnSpacing={5}>
          {formContent.map((entry, index) => (
            !protocol.is_template || entry.editForTemplates ?
              <Grid key={index} md={6}>
                <FormLabel>{entry.label}</FormLabel>
                <Input
                  name={entry.key}
                  onChange={(e) => setProtocol({ ...protocol, [e.target.name]: e.target.value })}
                  placeholder={entry.placeholder}
                  defaultValue={protocol[entry.key]?.toString()}
                  required={entry.required}
                />
              </Grid>
            :
              undefined
          ))}

          <Grid md={12} display="flex" justifyContent="flex-end">
            <Button
              size='sm'
              sx={{ width: 120 }}
              onClick={(event) => {
                event.preventDefault()
                if (protocol.name == '') {
                  showNotification({message: 'Name must not be empty.', type: 'warning'})
                } else if (protocol.description == '') {
                  showNotification({message: 'Description must not be empty.', type: 'warning'})
                } else if (!protocol.is_template && (protocol.indication == undefined || protocol.indication == '')) {
                  showNotification({message: 'Indication must not be empty.', type: 'warning'})
                } else {
                  mutation.mutate()
                  props.setOpen(false)
                }
              }}
            >
            Save
            </Button>
          </Grid>

        </Grid>
      </Stack>
    </>
  )
}


export default function ProtocolModal(props: ModalPropsCreate | ModalPropsModify<ProtocolOut> | ModalPropsCreateModifyFromTemplate<ProtocolOut>) {
  return (
    <Modal
      open={props.isOpen}   // open=False unmounts children, resetting the state of the form
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        sx={{ width: '70vw', borderRadius: 'md', p: 5 }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        <ProtocolForm {...props} />
      </ModalDialog>
    </Modal>
  )
}
