FROM node:bullseye-slim AS BUILD_IMAGE

WORKDIR /app

COPY package.json yarn.lock ./

# install dependencies, network timeout flag for slow network connection
RUN yarn install --network-timeout 100000

# Update browsers list
RUN npx browserslist@latest --update-db

COPY . .

# TODO: remove unused dependencies - how to identify these?
# RUN rm -rf node_modules/rxjs/src/
# RUN rm -rf node_modules/rxjs/bundles/
# RUN rm -rf node_modules/rxjs/_esm5/
# RUN rm -rf node_modules/rxjs/_esm2015/
# RUN rm -rf node_modules/swagger-ui-dist/*.map
# RUN rm -rf node_modules/couchbase/src/

# Final stage
FROM node:bullseye-slim

WORKDIR /app

# copy from build image
COPY --from=BUILD_IMAGE /app/dist ./dist
COPY --from=BUILD_IMAGE /app/package.json .
COPY --from=BUILD_IMAGE /app/node_modules ./node_modules


EXPOSE 3000

# Start the app
CMD [ "yarn", "start" ]