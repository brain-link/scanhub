# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.8
# FROM mcr.microsoft.com/azure-functions/python:4-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

#ENV AzureWebJobsStorage="UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://host.docker.internal"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot