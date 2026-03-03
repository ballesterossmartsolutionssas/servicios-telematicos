#!/usr/bin/env bash
set -euo pipefail

ZONE_FILE="/etc/bind/db.empresa.local"
NEW_SERIAL="2026030302"

if ! sudo grep -Eq '^api2[[:space:]]+IN[[:space:]]+A[[:space:]]+192\.168\.50\.10$' "${ZONE_FILE}"; then
    echo "Adding api2 A record..."
    echo "api2                IN  A       192.168.50.10" | sudo tee -a "${ZONE_FILE}" >/dev/null
else
    echo "api2 record already present."
fi

sudo sed -i "s/2026030301/${NEW_SERIAL}/" "${ZONE_FILE}"
sudo named-checkzone empresa.local "${ZONE_FILE}"
sudo rndc reload empresa.local
sudo systemctl restart named

echo "Updated zone tail:"
sudo tail -n 10 "${ZONE_FILE}"
