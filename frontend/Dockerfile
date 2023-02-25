FROM node:bullseye-slim AS BUILD_IMAGE

WORKDIR /app
COPY package.json yarn.lock ./
# install dependencies, network timeout flag for slow network connection
RUN yarn install --network-timeout 100000
# Update browsers list
RUN npx browserslist@latest --update-db
COPY . .


# Final stage
FROM node:bullseye-slim
WORKDIR /app
# copy from build image
COPY --from=BUILD_IMAGE /app /app
EXPOSE 3000
# Start the app
CMD [ "yarn", "start" ]
