#!/usr/bin/env bash
set -euo pipefail

DOMAIN="parcial.juan-camilo.com"
DNS_SERVER="192.168.50.2"
WEB_IP="192.168.50.3"

echo "== DNS resolution via slave =="
dig @"${DNS_SERVER}" "${DOMAIN}" +short

echo
echo "== Apache headers with gzip accepted (text file) =="
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: gzip" -I "http://${DOMAIN}/lorem.txt"

echo
echo "== Apache headers for excluded binary file (png) =="
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: gzip" -I "http://${DOMAIN}/logo.png"

echo
echo "== Bandwidth comparison compressed vs uncompressed =="
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: identity" -o /tmp/lorem_plain.out -s -w "identity size_download=%{size_download} bytes time_total=%{time_total}s\n" "http://${DOMAIN}/lorem.txt"
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: gzip" -o /tmp/lorem_gzip.out -s -w "gzip     size_download=%{size_download} bytes time_total=%{time_total}s\n" "http://${DOMAIN}/lorem.txt"

echo
echo "== Packet capture sample with tshark (sniffer evidence) =="
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tshark >/dev/null
sudo timeout 8 tshark -i eth1 -f "tcp port 80 and host ${WEB_IP}" -w /tmp/parcial_http_capture.pcapng >/tmp/tshark_live.log 2>&1 &
sleep 1
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: identity" -s "http://${DOMAIN}/lorem.txt" -o /dev/null
curl --resolve "${DOMAIN}:80:${WEB_IP}" -H "Accept-Encoding: gzip" -s "http://${DOMAIN}/lorem.txt" -o /dev/null
wait || true

echo "Capture file:"
ls -lh /tmp/parcial_http_capture.pcapng
echo "HTTP response content-encoding fields from capture:"
tshark -r /tmp/parcial_http_capture.pcapng -Y "http.response" -T fields -e http.response.code -e http.content_encoding -e frame.len 2>/dev/null | head -n 20
