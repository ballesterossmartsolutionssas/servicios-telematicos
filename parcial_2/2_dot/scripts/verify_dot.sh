#!/usr/bin/env bash
set -euo pipefail

DOT_DOMAIN_1="${DOT_DOMAIN_1:-openai.com}"
DOT_DOMAIN_2="${DOT_DOMAIN_2:-uao.edu.co}"
DOT_DOMAIN_3="${DOT_DOMAIN_3:-github.com}"
PLAIN_DNS_SERVER="${PLAIN_DNS_SERVER:-8.8.8.8}"
PLAIN_DOMAIN="${PLAIN_DOMAIN:-example.net}"

echo "== Estado actual de DoT =="
resolvectl status | sed -n '1,80p'

echo
echo "== Consultas con DoT activo =="
resolvectl query "${DOT_DOMAIN_1}"
resolvectl query "${DOT_DOMAIN_2}"
resolvectl query "${DOT_DOMAIN_3}"

echo
echo "== Captura de DNS sobre TLS (853/tcp) =="
sudo timeout 12 tshark -i any -f "tcp port 853" -w /tmp/dot_853.pcapng >/tmp/dot_853.log 2>&1 &
DOT_CAPTURE_PID=$!
sleep 2
resolvectl query "${DOT_DOMAIN_1}" >/tmp/dot_query.txt
wait "${DOT_CAPTURE_PID}" || true
ls -lh /tmp/dot_853.pcapng

echo
echo "== Captura de DNS convencional (53) =="
sudo timeout 12 tshark -i any -f "udp port 53 or tcp port 53" -w /tmp/dns_53.pcapng >/tmp/dns_53.log 2>&1 &
PLAIN_CAPTURE_PID=$!
sleep 2
dig @"${PLAIN_DNS_SERVER}" "${PLAIN_DOMAIN}" +short
wait "${PLAIN_CAPTURE_PID}" || true
ls -lh /tmp/dns_53.pcapng

echo
echo "== Informacion visible en DNS sin cifrar =="
tshark -r /tmp/dns_53.pcapng -Y "dns.qry.name" -T fields -e frame.number -e ip.dst -e dns.qry.name 2>/dev/null | head -n 10 || true
