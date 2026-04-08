#!/usr/bin/env bash
set -euo pipefail

SERVER_IP="${SERVER_IP:-192.168.50.3}"
FTP_USER="${FTP_USER:-telematico}"
FTP_PASS="${FTP_PASS:-Telemat1cos!}"
CA_CERT="${CA_CERT:-/vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt}"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y lftp openssl tshark

cat >/tmp/ftps_demo_payload.txt <<EOF
FTPS DEMO $(date -Iseconds)
Servidor ${SERVER_IP}
EOF

rm -f /tmp/ftps_demo_payload.downloaded.txt

echo "== Verificacion OpenSSL STARTTLS FTP =="
openssl s_client -connect "${SERVER_IP}:21" -starttls ftp -CAfile "${CA_CERT}" < /dev/null 2>/tmp/ftps_openssl.err \
    | tee /tmp/ftps_openssl.out \
    | egrep "subject=|issuer=|Verify return code" || true

echo
echo "== Operaciones FTPS con lftp =="
lftp -u "${FTP_USER},${FTP_PASS}" "ftp://${SERVER_IP}" <<EOF
set ssl:verify-certificate yes
set ssl:ca-file ${CA_CERT}
set ftp:ssl-force true
set ftp:ssl-auth TLS
set ftp:ssl-protect-data true
set ftp:passive-mode true
ls
put /tmp/ftps_demo_payload.txt -o upload/ftps_demo_payload.txt
get upload/ftps_demo_payload.txt -o /tmp/ftps_demo_payload.downloaded.txt
ls upload
bye
EOF

echo
echo "== Integridad del archivo transferido =="
sha256sum /tmp/ftps_demo_payload.txt /tmp/ftps_demo_payload.downloaded.txt

echo
echo "== Captura TLS FTPS =="
sudo timeout 12 tshark -i eth1 -f "tcp port 21 or tcp portrange 50000-50010" -w /tmp/ftps_tls_capture.pcapng >/tmp/ftps_tshark.log 2>&1 &
CAPTURE_PID=$!
sleep 2
lftp -u "${FTP_USER},${FTP_PASS}" "ftp://${SERVER_IP}" <<EOF
set ssl:verify-certificate yes
set ssl:ca-file ${CA_CERT}
set ftp:ssl-force true
set ftp:ssl-auth TLS
set ftp:ssl-protect-data true
set ftp:passive-mode true
put /tmp/ftps_demo_payload.txt -o upload/ftps_demo_payload_2.txt
bye
EOF
wait "${CAPTURE_PID}" || true

ls -lh /tmp/ftps_tls_capture.pcapng
if sudo grep -a "FTPS DEMO" /tmp/ftps_tls_capture.pcapng >/dev/null; then
    echo "ALERTA: se encontro texto plano en la captura."
else
    echo "OK: el contenido del archivo no aparece en texto plano dentro del pcap."
fi
