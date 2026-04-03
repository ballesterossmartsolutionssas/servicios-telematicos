#!/usr/bin/env bash
set -euo pipefail

SERVER_IP="${SERVER_IP:-192.168.50.3}"
SFTP_USER="${SFTP_USER:-telematico}"
SFTP_PASS="${SFTP_PASS:-Telemat1cos!}"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-client sshpass tshark

cat >/tmp/sftp_demo_payload.txt <<EOF
SFTP DEMO $(date -Iseconds)
Servidor ${SERVER_IP}
EOF

cat >/tmp/sftp_batch.txt <<EOF
ls
put /tmp/sftp_demo_payload.txt upload/sftp_demo_payload.txt
get upload/sftp_demo_payload.txt /tmp/sftp_demo_payload.downloaded.txt
ls upload
bye
EOF

echo "== Sesion SFTP batch =="
sshpass -p "${SFTP_PASS}" sftp -oBatchMode=no -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no "${SFTP_USER}@${SERVER_IP}" < /tmp/sftp_batch.txt | tee /tmp/sftp_session.log

echo
echo "== Integridad del archivo transferido =="
sha256sum /tmp/sftp_demo_payload.txt /tmp/sftp_demo_payload.downloaded.txt

echo
echo "== Captura SSH/SFTP en puerto 22 =="
sudo timeout 12 tshark -i eth1 -f "tcp port 22" -w /tmp/sftp_22_capture.pcapng >/tmp/sftp_tshark.log 2>&1 &
CAPTURE_PID=$!
sleep 2
sshpass -p "${SFTP_PASS}" sftp -oBatchMode=no -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no "${SFTP_USER}@${SERVER_IP}" < /tmp/sftp_batch.txt >/tmp/sftp_second_run.log
wait "${CAPTURE_PID}" || true

ls -lh /tmp/sftp_22_capture.pcapng
if sudo grep -a "SFTP DEMO" /tmp/sftp_22_capture.pcapng >/dev/null; then
    echo "ALERTA: se encontro texto plano en la captura."
else
    echo "OK: el contenido del archivo no aparece en texto plano dentro del pcap."
fi
