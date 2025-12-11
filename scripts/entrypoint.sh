#!/bin/bash

# Start TOR
tor -f /app/config/torrc &

# Wait for TOR to bootstrap
sleep 20

# Get the onion address
if [ -f /var/lib/tor/hidden_service/hostname ]; then
    ONION_ADDR=$(cat /var/lib/tor/hidden_service/hostname)
    echo "TOR Hidden Service Onion Address: http://$ONION_ADDR"
else
    echo "Failed to generate onion address"
fi

# Start Flask
cd /app
python3 src/app.py