FROM node:18

WORKDIR /src
ADD . /src

RUN yarn install
WORKDIR /src/apps/test-client
CMD yarn start