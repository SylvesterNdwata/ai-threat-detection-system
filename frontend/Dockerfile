FROM node:24-slim AS build

WORKDIR /build

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /build/dist /usr/share/nginx/html

EXPOSE 80