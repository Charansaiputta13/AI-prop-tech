# Build Stage
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Build the app
COPY . .
RUN npm run build

# Production Stage
FROM node:20-slim AS runner

WORKDIR /app

# Copy necessary files from builder
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

ENV NODE_ENV production
EXPOSE 3000

CMD ["npm", "start"]
