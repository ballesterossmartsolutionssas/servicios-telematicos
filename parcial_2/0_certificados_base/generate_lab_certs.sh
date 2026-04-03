#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-$(cd "$(dirname "$0")" && pwd)}"
COMMON_NAME="${COMMON_NAME:-servidor.ftps.local}"
SERVER_IP="${SERVER_IP:-192.168.50.3}"

mkdir -p "${OUT_DIR}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

cat >"${TMP_DIR}/server_ext.cnf" <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage=digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=@alt_names

[alt_names]
DNS.1=${COMMON_NAME}
IP.1=${SERVER_IP}
EOF

openssl genrsa -out "${OUT_DIR}/ca.key" 4096
openssl req -x509 -new -nodes -key "${OUT_DIR}/ca.key" -sha256 -days 3650 \
    -out "${OUT_DIR}/ca.crt" \
    -subj "/C=CO/ST=Valle/L=Cali/O=UAO/OU=ServiciosTelematicos/CN=UAO-CA"

openssl genrsa -out "${OUT_DIR}/server.key" 2048
openssl req -new -key "${OUT_DIR}/server.key" -out "${OUT_DIR}/server.csr" \
    -subj "/C=CO/ST=Valle/L=Cali/O=UAO/OU=ServiciosTelematicos/CN=${COMMON_NAME}"

openssl x509 -req -in "${OUT_DIR}/server.csr" -CA "${OUT_DIR}/ca.crt" -CAkey "${OUT_DIR}/ca.key" \
    -CAcreateserial -out "${OUT_DIR}/server.crt" -days 825 -sha256 -extfile "${TMP_DIR}/server_ext.cnf"

echo "Certificados generados en ${OUT_DIR}"
echo "CA: ${OUT_DIR}/ca.crt"
echo "Servidor: ${OUT_DIR}/server.crt"
echo "Clave: ${OUT_DIR}/server.key"
