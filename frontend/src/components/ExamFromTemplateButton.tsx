
import * as React from 'react'
import { useContext } from 'react';
import { useParams } from 'react-router-dom'
import { useMutation } from 'react-query'

import IconButton from '@mui/joy/IconButton'
import AddSharpIcon from '@mui/icons-material/AddSharp'
import Modal from '@mui/joy/Modal'
import ModalDialog from '@mui/joy/ModalDialog'
import ModalClose from '@mui/joy/ModalClose'
import DialogTitle from '@mui/material/DialogTitle'
import List from '@mui/joy/List'
import ListItemButton from '@mui/joy/ListItemButton';

import ExamTemplateItem from './ExamTemplateItem'

import { useQuery } from 'react-query'
import { ExamOut } from '../generated-client/exam';
import { examApi } from '../api'

import { CreateInstanceModalInterface } from '../interfaces/components.interface'
import LoginContext from '../LoginContext';


export default function ExamFromTemplateButton(props: CreateInstanceModalInterface) {

  const params = useParams()

  const [user, setUser] = useContext(LoginContext);
  const [modalOpen, setModalOpen] = React.useState(false)

  // const {data: exams, isLoading, isError} = useQuery<ExamOut[]>({
  const {data: exams} = useQuery<ExamOut[]>({
    queryKey: ['exams'],
    queryFn: async () => {
      return await examApi.getAllExamTemplatesApiV1ExamTemplatesAllGet(
        {headers: {Authorization: 'Bearer ' + user?.access_token}}
      )
      .then((result) => {return result.data})
    }
  })

  const mutation = useMutation(async (id: string) => {
    await examApi.createExamFromTemplateApiV1ExamPost(
      Number(params.patientId), 
      id, 
      {headers: {Authorization: 'Bearer ' + user?.access_token}}
    )
    .then(() => { props.onSubmit() })
    .catch((err) => { console.log(err) })
  })

  return (
    <>
      <IconButton 
        variant='soft'
        onClick={() => {setModalOpen(true)}}
      >
        <AddSharpIcon />
      </IconButton>

      <Modal
          open={modalOpen}
          onClose={() => {setModalOpen(false)}}
        >
          <ModalDialog sx={{width: '50vw', p: 5}}>
            <ModalClose />
            <DialogTitle>Exam Templates</DialogTitle>
            <List
              sx={{
                overflow: 'scroll',
                mx: 'calc(-1 * var(--ModalDialog-padding))',
                px: 'var(--ModalDialog-padding)',
              }}
            >
              {
                exams && exams.map((exam, idx) => (
                  <ListItemButton
                    key={idx}
                    onClick={() => {
                      mutation.mutate(exam.id)
                      setModalOpen(false)
                    }}
                  >
                    <ExamTemplateItem
                      item={exam}
                      onClicked={() => {}}
                    />
                  </ListItemButton>
                ))
              }
            </List>
          </ModalDialog>
        </Modal>
    </>
  )
}