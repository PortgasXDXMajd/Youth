# ---- Dependencies Stage ----
FROM node:20-alpine AS deps

RUN npm config set ignore-scripts true
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# ---- Builder Stage ----
FROM node:20-alpine AS builder

ARG NEXT_PUBLIC_GOOGLE_CLIENT_ID
ARG NEXT_PUBLIC_API_URL

ENV NEXT_PUBLIC_GOOGLE_CLIENT_ID=$NEXT_PUBLIC_GOOGLE_CLIENT_ID
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ---- Production Stage ----
FROM node:20-alpine AS production

RUN apk --no-cache add dumb-init && rm -rf /var/cache/apk/* /tmp/*
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN find / -perm /6000 -type f -exec chmod a-s {} + || true

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder --chown=appuser:appgroup /app/.next/standalone ./
COPY --from=builder --chown=appuser:appgroup /app/.next/static ./.next/static

USER appuser

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

LABEL org.opencontainers.image.source="https://github.com/yourorg/youth"
LABEL org.opencontainers.image.description="Youth Frontend"
