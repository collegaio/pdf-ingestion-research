FROM node:20-alpine AS base

WORKDIR /app

COPY package.json .
COPY package-lock.json .

ENV VITE_APP_BACKEND_URL=https://communist-loise-collega-b748a8e9.koyeb.app

RUN npm ci

COPY . .

RUN npm run build

FROM nginx:latest as runner

COPY --from=base /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 5173/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
