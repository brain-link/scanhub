import * as React from 'react'
import Input from '@mui/joy/Input'
import Modal from '@mui/joy/Modal'
import ModalClose from '@mui/joy/ModalClose'
import ModalDialog from '@mui/joy/ModalDialog'
import Stack from '@mui/joy/Stack'
import Typography from '@mui/joy/Typography'
import Button from '@mui/joy/Button'
import FormLabel from '@mui/joy/FormLabel'
import Grid from '@mui/joy/Grid'
import { useMutation } from 'react-query'
import { userApi } from '../api'
import { ModalComponentProps } from '../interfaces/components.interface'
import { User } from '../generated-client/userlogin'
import LoginContext from '../LoginContext'
import { setDefaultViewport } from 'cornerstone-core'



// User form items, order is row wise
const createUserFormContent = [
  { key: 'username',    label: 'Username',  placeholder: 'Username' },
  { key: 'first_name',   label: 'First name', placeholder: 'First name' },
  { key: 'last_name',    label: 'Last name', placeholder: 'Last name' },
  { key: 'email',       label: 'e-Mail',    placeholder: 'e-Mail' },
  { key: 'access_token', label: 'Password',  placeholder: 'At least 12 characters.' },
]


export default function UserCreateModal(props: ModalComponentProps<User>) {

  const [currentuser, ] = React.useContext(LoginContext)
  const [user, setUser] = React.useState({username: '', first_name: '', last_name: '', email: '', password: '', token_type: 'password', access_token: ''})

  // Post a new record and refetch records table
  const mutation = useMutation({
    mutationKey: ['users'],
    mutationFn: async () => {
      await userApi.createUserApiV1UserloginCreateuserPost(user, {headers: {Authorization: 'Bearer ' + currentuser?.access_token}})
      .then((_) => {
        props.onSubmit(user)
        if (props.setAlert) { props.setAlert(null) } 
      })
      .catch((err) => { 
        let error_message = null;
        if (err?.response?.data?.detail) {
          error_message = "Error at creating new user. Detail: " + err.response.data.detail
        }
        else {
          error_message = "Error at creating new user."
        }
        console.log(error_message)
        if (props.setAlert) {
          props.setAlert(error_message)
        }
      })
    }
  })

  return (
    <Modal
      keepMounted
      open={props.isOpen}
      color='neutral'
      onClose={() => props.setOpen(false)}
      sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
    >
      <ModalDialog
        aria-labelledby='basic-modal-dialog-title'
        aria-describedby='basic-modal-dialog-description'
        size='sm'
        sx={{
          width: '50vw', 
          borderRadius: 'md', 
          p: 5
        }}
      >
        <ModalClose
          sx={{
            top: '10px',
            right: '10px',
            borderRadius: '50%',
            bgcolor: 'background.body',
          }}
        />
        <Typography id='basic-modal-dialog-title' component='h2' level='inherit' fontSize='1.25em' mb='0.25em'>
          Create New User
        </Typography>

        <form
          onSubmit={(event) => {
            event.preventDefault()
            mutation.mutate()
            props.setOpen(false)
          }}
        >
          <Stack spacing={5}>
            <Grid container rowSpacing={1.5} columnSpacing={5}>
              {createUserFormContent.map((item, index) => (
                <Grid key={index} md={6}>
                  <FormLabel>{item.label}</FormLabel>
                  <Input
                    name={item.key}
                    onChange={(e) => setUser({ ...user, [e.target.name]: e.target.value })}
                    placeholder={item.placeholder}
                    required
                  />
                </Grid>
              ))}
            </Grid>
            <Button size='sm' type='submit' sx={{ maxWidth: 100 }}>
              Submit
            </Button>
          </Stack>
        </form>
      </ModalDialog>
    </Modal>
  )
}