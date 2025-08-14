FROM node:20-alpine
WORKDIR /app

# Use Yarn 4 pinned by "packageManager" in package.json
RUN corepack enable

# --- Install deps first for better layer caching -----------------------------
# If you use Yarn Berry, keep .yarn/ and .yarnrc.yml
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn/ .yarn/
RUN yarn install --immutable

# Install curl for health check
RUN apk add --no-cache curl

# Then copy the app (index.html, vite.config, src, etc.)
COPY . .

# Vite will listen on 0.0.0.0:3000 so nginx can reach it
EXPOSE 3000

# Reliable file watching when src is bind-mounted from host (optional)
ENV CHOKIDAR_USEPOLLING=true

# Choose dev or prod at build/run time via ARG/ENV (compose passes args.NOVE_ENV)
ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}

# If NODE_ENV=production -> build once and serve with vite preview on :3000
# Else -> run vite dev server on :3000 (HMR over WS works via nginx proxy)
CMD ["/bin/sh", "-lc", "\
  if [ \"$NODE_ENV\" = \"production\" ]; then \
    yarn build && yarn preview --host 0.0.0.0 --port 3000; \
  else \
    yarn dev --host 0.0.0.0 --port 3000; \
  fi \
"]
