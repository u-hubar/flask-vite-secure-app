#!/usr/bin/env sh

service crond start;
nginx -g "daemon off;";
exec "$@";
