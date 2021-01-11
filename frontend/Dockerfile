FROM node:current-alpine3.10

WORKDIR /var/frontend

COPY package*.json yarn.lock entrypoint.sh ./

RUN ["chmod", "+x", "/var/frontend/entrypoint.sh"] 
ENTRYPOINT  [ "sh", "/var/frontend/entrypoint.sh" ]
