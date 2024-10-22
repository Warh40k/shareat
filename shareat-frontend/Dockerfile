# Сборка фронтенда
FROM node:20.16-alpine AS build-node-env
RUN npm install -g http-server
WORKDIR /app
COPY ./package*.json /app
RUN npm ci
COPY ./ /app
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]