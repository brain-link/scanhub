# FROM node:bullseye-slim AS BUILD_IMAGE
FROM node:20.5.0-slim AS BUILD_IMAGE

# Install python, required for node-gyp
# RUN apt-get update || : && apt-get install python -y

# RUN apt-get --no-cache python3 g++ make

RUN apt-get update || : && apt-get install -y \
    python3 \
    build-essential

WORKDIR /app
COPY package.json yarn.lock ./

# RUN apt update && apk --no-cache --virtual build-dependencies add \
#     python3 \
#     make \
#     g++

RUN yarn install --network-timeout 100000

# install dependencies, network timeout flag for slow network connection
# RUN yarn install --production --network-timeout 100000 \


# Update browsers list
RUN npx browserslist@latest --update-db
COPY . .


# Final stage
# FROM node:bullseye-slim
FROM node:20.5.0-slim

WORKDIR /app

# copy from build image
COPY --from=BUILD_IMAGE /app /app
EXPOSE 3000

# Start the app
CMD [ "yarn", "start" ]
