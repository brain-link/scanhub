/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * NotificationContextProvider.tsx contains the context provider to display notifications to the user.
 */
import { PropsWithChildren, useState } from 'react'
import React from 'react'

import NotificationContext from './NotificationContext'
import { MessageObject } from './NotificationContext'



export default function LoginContextProvider(props: PropsWithChildren) {
  const [messageObject, setMessageObject] = useState<MessageObject>({message: '', type: 'warning', open: false})

  return <NotificationContext.Provider value={[messageObject, setMessageObject]}>{props.children}</NotificationContext.Provider>
}
