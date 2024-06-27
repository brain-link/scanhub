/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * NotificationContext.tsx contains a context to notify the user with some message.
 */
import { createContext } from 'react'

export type NotificationObject = {
    message: string, 
    type: 'warning' | 'success',
    visible?: boolean
}

const NotificationContext = createContext<[NotificationObject, (messageObj: NotificationObject) => void]>([{message: '', type: 'success', visible: true}, () => {}])

export default NotificationContext
