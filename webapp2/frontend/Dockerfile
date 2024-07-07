FROM node:20-alpine AS base

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm ci

COPY . .

ENV NODE_ENV=production
RUN npm run build
RUN npm install -g serve

EXPOSE 5173/tcp
CMD [ "serve", "-p", "5173", "-s", "dist" ]

# FROM nginx:latest as runner

# COPY --from=base /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/nginx.conf

# EXPOSE 5173/tcp

# CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
