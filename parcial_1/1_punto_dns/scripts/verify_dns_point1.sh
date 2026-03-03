#!/usr/bin/env bash
set -euo pipefail

MASTER_IP="192.168.50.3"
SLAVE_IP="192.168.50.2"

echo "== Direct resolution on slave =="
dig @"${SLAVE_IP}" maestro.empresa.local +short
dig @"${SLAVE_IP}" esclavo.empresa.local +short
dig @"${SLAVE_IP}" www.empresa.local +short

echo
echo "== AAAA and CNAME on slave =="
dig @"${SLAVE_IP}" maestro.empresa.local AAAA +short
dig @"${SLAVE_IP}" www.empresa.local CNAME +short

echo
echo "== Reverse resolution on slave =="
dig @"${SLAVE_IP}" -x "${MASTER_IP}" +short
dig @"${SLAVE_IP}" -x "${SLAVE_IP}" +short

echo
echo "== Unauthorized AXFR attempt from host should fail =="
if dig @"${MASTER_IP}" empresa.local AXFR +time=2 +tries=1 | grep -q "Transfer failed"; then
    echo "AXFR correctly blocked for unauthorized clients."
else
    echo "WARNING: AXFR command did not report explicit failure. Review output manually."
fi

echo
echo "== Recursion test on authoritative server should not resolve external domains =="
dig @"${SLAVE_IP}" google.com +short || true
