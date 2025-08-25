/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * DagsterUIModal.tsx is responsible for rendering the Dagster UI with an overview of the latest task result.
 */
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import React from 'react'
import IconButton from '@mui/joy/IconButton'
import OpenInNew from '@mui/icons-material/OpenInNew'
import { ModalPropsItem } from '../interfaces/components.interface'


export default function DagsterUIModal(props: ModalPropsItem<string>) {

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
        sx={{ width: '90vw', height: 'calc(98vh - 2 * var(--Navigation-height))', borderRadius: 'md', p: 2}}
      >
        <Stack direction='row' gap={2} sx={{ alignItems: 'center'}}>
          <Typography component='h5' level='inherit'>Dagster</Typography>
          <IconButton
            variant="plain"
            component="a"
            href={props.item}
            target="_blank"
            rel="noreferrer"
            title="Open in new tab"
            sx={{width: 20}}
          >
            <OpenInNew />
          </IconButton>
        </Stack>

        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        
        <div style={{ height: '95%', width: '100%' }}>
          <iframe
            title="Dagster"
            src={props.item}
            style={{ width: '100%', height: '100%', border: 0 }}
            allow="clipboard-read; clipboard-write"
          />
        </div>
      </ModalDialog>
    </Modal>
  )
}
