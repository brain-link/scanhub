import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import React from 'react';

import { loginApi } from '../api'
import { User } from '../generated-client/userlogin'


function Login(props: {onLogin: (user: User) => void}) {
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
        console.log("Login submitted.")
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
        
        // TODO consider sending a secure password hash like argon2 instead of the password itself
        // on the server this hash could be hashed again, just like if it were the password
        loginApi.loginApiV1UserloginLoginPost(event.currentTarget.username_input.value, 
                                              event.currentTarget.password_input.value,
                                              "password")
        .then((result) => {
          props.onLogin(result.data);
        })
        .catch((error) => {
          if (error?.response?.data?.detail == "Invalid authentication credentials") {
            console.log("Invalid authentication credentials");
          } else {
            console.log("Error at login:", error)
          }
        });
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