# NGINX Configuration Overview

This file configures NGINX as a reverse proxy for the ScanHub application ecosystem. It handles HTTP to HTTPS redirection, SSL termination, health checks, static file serving, and routing of API requests to various backend services.

---

## HTTP Server Block

**Purpose:** Redirect all HTTP traffic to HTTPS for secure communication.

**Configuration:**
- `listen 8080;` — Listens for incoming HTTP requests on port 8080.
For production, the default port 80 could be used for http requests.
- `server_name localhost;` — Responds to requests for `localhost`.
- `location /` — Redirects all requests to the HTTPS version of the site.
  - `return 301 https://localhost:8443;` — Issues a permanent redirect to HTTPS.
- `location /health` — Provides a simple health check endpoint.
  - Returns HTTP 200 with the body `ok`.

---

## HTTPS Server Block

**Purpose:** Handles all secure (HTTPS) traffic, SSL termination, and reverse proxying to backend services.

**Configuration:**
- `listen 8443 ssl;` — Listens for HTTPS requests on port 8443.
For production, the default port 443 could be used for http requests.
Using a custom port simplifies the setup with a remote connection, as port forwarding works seamlessly with 8443.
- `server_name localhost;` — Responds to requests for `localhost`.
- `ssl_certificate` and `ssl_certificate_key` — Paths to SSL certificate and private key.
- `ssl_protocols` and `ssl_ciphers` — Enforces secure TLS protocols and strong ciphers.
- `root /etc/nginx/html;` — Sets the root directory for static files (not used for proxied locations).
- `client_max_body_size 100M;` — Allows uploads up to 100 MB.

### Health Check

- `location /health` — Returns HTTP 200 with `ok` for health monitoring.

### UI Frontend

- `location /` — Proxies all root requests to the ScanHub UI frontend.
- `proxy_pass http://scanhub-ui:3000/;` — Forwards requests to the UI service.
When running the UI seperately (i.e. not using docker), this needs to be replaced by `proxy_pass http://host.docker.internal:3000/;`.

### API Routing

Routes API requests to the appropriate backend microservices:

#### Workflow Manager
- `/api/v1/workflowmanager` → `workflow-manager:8000/api/v1/workflowmanager`
- `/api/v1/workflowmanager/login` → `user-login-manager:8000/api/v1/userlogin/login`

#### Device Manager
- `/api/v1/device` → `device-manager:8000/api/v1/device`
- `/api/v1/device/login` → `user-login-manager:8000/api/v1/userlogin/login`
- `/api/v1/device/ws` → `device-manager:8000/api/v1/device/ws`
(Special handling for WebSocket upgrade headers.)

#### Exam Manager
- `/api/v1/exam` → `exam-manager:8000/api/v1/exam`
- `/api/v1/exam/login` → `user-login-manager:8000/api/v1/userlogin/login`

#### User Login Manager
- `/api/v1/userlogin` → `user-login-manager:8000/api/v1/userlogin`

#### Patient Manager
- `/api/v1/patient` → `patient-manager:8100/api/v1/patient`
- `/api/v1/patient/login` → `user-login-manager:8000/api/v1/userlogin/login`

---

## WebSocket Support

For `/api/v1/device/ws`, the configuration includes:
- `proxy_http_version 1.1;`
- `proxy_set_header Upgrade $http_upgrade;`
- `proxy_set_header Connection "Upgrade";`
- `proxy_set_header Host $host;`

These directives enable proper WebSocket proxying.

---

## Summary Table

| Path                              | Proxied To                                 | Purpose                |
|------------------------------------|--------------------------------------------|------------------------|
| `/`                               | `scanhub-ui:3000/`                         | UI frontend            |
| `/api/v1/workflowmanager`         | `workflow-manager:8000/api/v1/workflowmanager` | Workflow API      |
| `/api/v1/workflowmanager/login`   | `user-login-manager:8000/api/v1/userlogin/login` | Auth for workflow |
| `/api/v1/device`                  | `device-manager:8000/api/v1/device`        | Device API             |
| `/api/v1/device/login`            | `user-login-manager:8000/api/v1/userlogin/login` | Auth for device   |
| `/api/v1/device/ws`               | `device-manager:8000/api/v1/device/ws`     | Device WebSocket       |
| `/api/v1/exam`                    | `exam-manager:8000/api/v1/exam`            | Exam API               |
| `/api/v1/exam/login`              | `user-login-manager:8000/api/v1/userlogin/login` | Auth for exam     |
| `/api/v1/userlogin`               | `user-login-manager:8000/api/v1/userlogin` | User login API         |
| `/api/v1/patient`                 | `patient-manager:8100/api/v1/patient`      | Patient API            |
| `/api/v1/patient/login`           | `user-login-manager:8000/api/v1/userlogin/login` | Auth for patient  |
| `/health`                         | N/A (handled by NGINX)                     | Health check           |

---

## Notes

- All `/login` endpoints are routed to the user login manager for centralized authentication.
- The configuration assumes all backend services are accessible by their Docker service names.
- WebSocket support is explicitly enabled for device communication.
- Health checks are available on both HTTP and HTTPS.

---

This configuration ensures secure, organized, and efficient routing of all frontend and backend traffic for the ScanHub platform.