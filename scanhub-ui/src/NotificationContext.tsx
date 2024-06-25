/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * NotificationContext.tsx contains a context to notify the user with some message.
 */
import { createContext } from 'react'

export type MessageObject = {
    message: string, 
    type: 'warning' | 'success',
    open: boolean
}

const NotificationContext = createContext<[MessageObject, (messageObj: MessageObject) => void]>([{message: '', type: 'success', open: true}, () => {}])

export default NotificationContext
