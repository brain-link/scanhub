import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import React, { useState } from 'react';

import { loginApi } from '../api'
import { User } from '../generated-client/userlogin'
import Alert from '@mui/joy/Alert';


const enum LoginErrorState {
  NoError,
  InvalidCredentials,
  EmptyUsernameOrPassword,
  OtherError
}

function Login(props: {onLogin: (user: User) => void}) {

  const [loginErrorState, setLoginErrorState] = useState<LoginErrorState>(LoginErrorState.NoError);
  const [loginRequestInProgress, setLoginRequestInProgress] = useState<boolean>(false);

  return (
    <Box sx={{width: "20%", height: "20%", margin: "auto"}}>
      <h1 style={{textAlign: "center"}}>
        Welcome to Scanhub!
      </h1>
      <h2>
        Login
      </h2>

      <form onSubmit={(event) => {
        event.preventDefault()  // do not reload the page
        if (event.currentTarget.username_input.value == "" || event.currentTarget.password_input.value == "") {
          setLoginErrorState(LoginErrorState.EmptyUsernameOrPassword)
          console.log("Username or password must not be empty.")
        }
        else {
          setLoginRequestInProgress(true)
          setLoginErrorState(LoginErrorState.NoError)
          console.log("Submit login.")
          
          // TODO consider sending a secure password hash like argon2 instead of the password itself
          // on the server this hash could be hashed again, just like if it were the password
          loginApi.loginApiV1UserloginLoginPost(event.currentTarget.username_input.value, 
                                                event.currentTarget.password_input.value,
                                                "password")
          .then((result) => {
            setLoginRequestInProgress(false)
            props.onLogin(result.data);
          })
          .catch((error) => {
            setLoginRequestInProgress(false)
            if (error?.response?.data?.detail == "Invalid authentication credentials") {
              console.log("Invalid authentication credentials");
              setLoginErrorState(LoginErrorState.InvalidCredentials)
            } else {
              console.log("Error at login:", error)
              setLoginErrorState(LoginErrorState.OtherError)
            }
          });
        }
      }}>
        <Stack spacing={1}>
          <div>User:</div>
          <Input id="username_input" />
          <div>Password:</div>
          <Input type="password" id="password_input" />
          <Button type="submit" loading={loginRequestInProgress} fullWidth={true}>
            Login
          </Button>
          {loginErrorState == LoginErrorState.InvalidCredentials ? <Alert color="warning">Invallid username or password.</Alert> : null}
          {loginErrorState == LoginErrorState.OtherError ? <Alert color="warning">Other error at login, please talk to the developer.</Alert> : null}
          {loginErrorState == LoginErrorState.EmptyUsernameOrPassword ? <Alert color="warning">Username or password must not be empty.</Alert> : null}
        </Stack>
      </form>
    </Box>
  )
}

export default Login;