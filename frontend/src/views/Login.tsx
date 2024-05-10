import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import React from 'react';

import { loginApi } from '../api'
import { User } from '../generated-client/userlogin'


function Login(props: {onLogin: (token: string, user: User) => void}) {
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
        console.log("Login submitted.", {"User": event.currentTarget.username_input.value, 
                                         "Password": event.currentTarget.password_input.value})
/*
        fetch("http://localhost:8080/api/v1/userlogin/login",
              {
                method: "POST",
                mode: "cors",
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
                body: "grant_type=password&username=" + event.currentTarget.username_input.value + "&password=" + event.currentTarget.password_input.value
              })
        .then((response) => {
          if (!response.ok) {
            throw new Error('response not ok')
          }
          return response.json();
        })
*/
        loginApi.loginApiV1UserloginLoginPost(event.currentTarget.username_input.value, 
                                              event.currentTarget.password_input.value,
                                              "password",
                                              undefined, undefined, undefined,
                                              {})
        .then((result) => {
          props.onLogin(result.data["access_token"], result.data.user)
        })
        .catch((error) => {console.log("Error:", error)});
      }}>
        <Stack spacing={1}>
          <div>User:</div>
          <Input id="username_input" />
          <div>Password:</div>
          <Input type="password" id="password_input" />
          <Button type="submit" fullWidth={true}>
            Login
          </Button>
        </Stack>
      </form>
    </Box>
  )
}

export default Login;