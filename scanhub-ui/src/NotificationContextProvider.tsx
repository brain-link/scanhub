/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * NotificationContextProvider.tsx contains the context provider to display notifications to the user.
 */
import { PropsWithChildren, useState } from 'react'
import React from 'react'

import NotificationContext from './NotificationContext'
import { NotificationObject } from './NotificationContext'



export default function LoginContextProvider(props: PropsWithChildren) {
  const [notificationObject, setNotificationObject] = useState<NotificationObject>({message: '', type: 'warning', visible: false})

  function showNotification(notificationObject: NotificationObject) {
    if (notificationObject.type == 'warning') {
      console.log('Warning:', notificationObject.message);
    }
    else if (notificationObject.type == 'success') {
      console.log(notificationObject.message);
    }
    setNotificationObject(notificationObject);
  }

  return <NotificationContext.Provider value={[notificationObject, showNotification]}>{props.children}</NotificationContext.Provider>
}
