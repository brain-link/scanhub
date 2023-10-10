// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
// Definition of global variables
import { CButton, CCloseButton, CModal, CModalBody, CModalHeader, CModalTitle } from '@coreui/react'
import axios from 'axios'
import { useState } from 'react'
import React from 'react'
import { Link, useParams } from 'react-router-dom'

export function DeleteWarning(contextURL) {
  const [visible, setVisible] = useState(false)

  const deletePost = async () => {
    console.log(contextURL.contextURL)
    // return await axios.delete(`http://localhost:8000/patients/${params.patientId}/${params.procedureId}/records/${params.recordingId}/`);
    return await axios.delete(contextURL.contextURL)
  }

  return (
    <>
      <CCloseButton onClick={() => setVisible(!visible)} />
      <CModal visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Delete Record</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <p>You are about to delete this entry, are you sure that you want to proceed?</p>
          <CButton
            color='danger'
            variant='outline'
            onClick={() => {
              deletePost()
              setVisible(false)
            }}
          >
            {' '}
            Confirm Delete{' '}
          </CButton>
        </CModalBody>
      </CModal>
    </>
  )
}
