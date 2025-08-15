/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * LoginContext.tsx contains the user context.
 */
import React from 'react'
import { createContext } from 'react'

import { User } from './openapi/generated-client/userlogin'

const LoginContext = createContext<[User | null, React.Dispatch<React.SetStateAction<User | null>>]>([null, () => {}])

export default LoginContext
