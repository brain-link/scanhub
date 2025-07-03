/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Urls.tsx contains the different urls of the backend services.
 */

const baseUrls = {
  patientService: 'https://localhost:8443',
  examService: 'https://localhost:8443',
  workflowManagerService: 'https://localhost:8443',
  userloginService: 'https://localhost:8443',
  deviceService: 'https://localhost:8443',
  nginxUrl: 'https://localhost:8443'
  // For production, you can uncomment the following lines and comment the above ones:
  // patientService: 'https://localhost',
  // examService: 'https://localhost',
  // workflowManagerService: 'https://localhost',
  // userloginService: 'https://localhost',
  // deviceService: 'https://localhost',
  // nginxUrl: 'https://localhost'
}

export default baseUrls
