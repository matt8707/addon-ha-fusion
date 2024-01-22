#!/usr/bin/with-contenv bashio

HASS_URL=$(bashio::config 'hass_url')
export HASS_URL

echo "Starting Fusion..."

node server.js
