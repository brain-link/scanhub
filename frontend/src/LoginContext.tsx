import React from 'react';
import { createContext } from "react";

import { User } from './generated-client/userlogin';


const LoginContext = createContext<[User | null, React.Dispatch<React.SetStateAction<User | null>>]>([null, () => {}]);

export default LoginContext;