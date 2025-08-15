FROM node:20-alpine
WORKDIR /app

# Use Yarn 4 via Corepack (no local .yarn needed)
RUN corepack enable && corepack prepare yarn@4.9.2 --activate

# Copy only what we actually have
COPY package.json yarn.lock .yarnrc.yml ./

# Install deps (immutable = respect lockfile)
RUN yarn install --immutable

# Install curl for health check
RUN apk add --no-cache curl

# Now copy the rest of the app
COPY . .

EXPOSE 3000
ENV CHOKIDAR_USEPOLLING=true
ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

CMD ["/bin/sh","-lc","\
  if [ \"$NODE_ENV\" = \"production\" ]; then \
    yarn build && yarn preview --host 0.0.0.0 --port 3000; \
  else \
    yarn dev --host 0.0.0.0 --port 3000; \
  fi \
"]
