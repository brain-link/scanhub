# FROM node:bullseye-slim AS BUILD_IMAGE
FROM node:20.5.0-slim AS BUILD_IMAGE

# Install python, required for node-gyp
# RUN apt-get update || : && apt-get install python -y

# RUN apt-get --no-cache python3 g++ make

RUN apt-get update || : && apt-get install -y python3 build-essential \
    && apt-get clean

WORKDIR /app
COPY package.json yarn.lock ./

# RUN apt update && apk --no-cache --virtual build-dependencies add \
#     python3 \
#     make \
#     g++

# Install dependencies, network timeout flag for slow network connection
# Without frozen lockfile
# RUN yarn install --network-timeout 100000
# With frozen lockfile
RUN yarn install --frozen-lockfile --network-timeout 100000

# Use argument to specify development or production state
# ARG NODE_ENV=development
# ENV NODE_ENV=$NODE_ENV
# RUN set -ex; \
#     if [ "$NODE_ENV" = "production" ]; then \
#         yarn install --frozen-lockfile --production --network-timeout 100000; \
#         # yarn install --no-cache --frozen-lockfile --production --network-timeout 100000; \
#     elif [ "$NODE_ENV" = "development" ]; then \
#         yarn install --frozen-lockfile --network-timeout 100000; \
#     fi;

# Update browsers list
RUN npx browserslist@latest --update-db
COPY . .

# Clear yarn cache to save memory
# RUN yarn cache clean


# Final stage
# FROM node:bullseye-slim
FROM node:20.5.0-slim

WORKDIR /app

# copy from build image
COPY --from=BUILD_IMAGE /app /app
EXPOSE 3000

# Start the app
CMD [ "yarn", "start" ]
