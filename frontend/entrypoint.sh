#!/usr/bin/env sh

chown :node -R /var/frontend

mkdir -p /var/frontend/node_modules
chown node: -R /var/frontend/node_modules

su node -c '''
yarn \
  && yarn dev
'''
