FROM node:20.10-alpine as builder

WORKDIR /builder

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .
RUN npx prisma generate
RUN npm run build

##### Production image:
FROM node:20.10-alpine as app

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm ci

COPY --from=builder /builder/build ./build
COPY --from=builder /builder/prisma ./prisma
COPY --from=builder /builder/node_modules/.prisma ./node_modules/.prisma

EXPOSE 3000
CMD ["npm", "run", "start"]
