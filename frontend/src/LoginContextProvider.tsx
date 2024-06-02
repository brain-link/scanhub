import { useState, PropsWithChildren } from 'react';
import React from 'react';

import LoginContext from './LoginContext';
import { User } from './generated-client/userlogin';


export default function LoginContextProvider(props: PropsWithChildren) {
  const [user, setUser] = useState<User | null>(null);     // null when the user is not logged in

  return (
    <LoginContext.Provider value={[user, setUser]}>
      {props.children}
    </LoginContext.Provider>
  )
}

