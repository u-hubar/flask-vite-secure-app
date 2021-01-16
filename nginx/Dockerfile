FROM nginx:1.17-alpine

RUN apk upgrade --available
RUN apk add --no-cache openrc tini busybox-initscripts
RUN apk add logrotate nginx-mod-http-headers-more

COPY entrypoint.sh /usr/local/bin/
RUN ["chmod", "+x", "/usr/local/bin/entrypoint.sh"] 
ENTRYPOINT  [ "sh", "/usr/local/bin/entrypoint.sh" ]
