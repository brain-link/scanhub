===================
Notes on Deployment
===================

Deployment was not testet yet! The following list gives an indication about some of the steps needed to deploy scanhub productively:

- Get a server (either on-site or in a datacenter/cloud)
- Get a domain name (e.g. scanhub.yourinstitution.com)
- Create a new private key (e.g. with openSSL). Keep this key private! Make sure not to commit it to the repository during development!
- Replace the default private key in secrets/privatekey.pem with your new private key
- Get a server certificate for your domain name (likely from the place where you got your domain name)
- Replace the default certificate in secrets/certificate.pem with your new certificate
- Change the default usernames and default passwords in all the configuration files in the folder secrets/
- In infrastructure/nginx_config.conf put your domain name as server_name in place of localhost (line 5 and line 21)
- In infrastructure/nginx_config.conf put your domain name in place of localhost as redirect target from http to https (line 8)
- In scanhub-ui/src/utils/Urls.tsx put your domain name in place of localhost
- In services/device-manager/app/main.py in the list of allowed origins, replace localhost with your domain name
- In services/protocol-manager/app/main.py in the list of allowed origins, replace localhost with your domain name
- In services/mri/sequence-manager/app/main.py in the list of allowed origins, replace localhost with your domain name
- In services/patient-manager/app/main.py in the list of allowed origins, replace localhost with your domain name
- In services/user-login-manager/app/main.py in the list of allowed origins, replace localhost with your domain name
- Build the Scanhub Containers as described in section "Installation + Start & Stop"
- Set up a service to automatically start Scanhub when booting the system
- Consider setting up monitoring of the servers resources etc.
- Consider limiting the number of connections, configure multiple workers/servers, load-balancing, etc.
- Consider removing the --reload option in the uvicorn commands in docker-compose.yml (6 occurances)
- Check for memory leaks when running the application over several days, consider automatic reboots
- Maybe put some development effort in the commented code in scanhub-ui/Dockerfile with the production flag