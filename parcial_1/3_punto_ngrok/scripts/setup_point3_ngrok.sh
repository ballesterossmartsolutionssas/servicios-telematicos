#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y curl tar jq

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

ARCH="amd64"
URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-${ARCH}.tgz"

curl -fsSL "${URL}" -o "${TMP_DIR}/ngrok.tgz"
tar -xzf "${TMP_DIR}/ngrok.tgz" -C "${TMP_DIR}"
sudo install -m 0755 "${TMP_DIR}/ngrok" /usr/local/bin/ngrok

sudo mkdir -p /var/www/parcial
cat <<'EOF' | sudo tee /var/www/parcial/pagina_personalizada.html >/dev/null
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pagina Personalizada Parcial</title>
</head>
<body>
  <h1>Parcial Servicios Telematicos - Punto 3</h1>
  <p>Esta es la pagina personalizada publicada por tunel ngrok.</p>
</body>
</html>
EOF

if ! grep -q "pagina_personalizada.html" /var/www/parcial/index.html 2>/dev/null; then
  cat <<'EOF' | sudo tee /var/www/parcial/index.html >/dev/null
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Parcial Servicios Telematicos</title>
</head>
<body>
  <h1>Servidor web del parcial</h1>
  <p>Dominio local: parcial.juan-camilo.com</p>
  <p>Prueba remota ngrok: <a href="/pagina_personalizada.html">pagina_personalizada.html</a></p>
</body>
</html>
EOF
fi

sudo systemctl restart apache2
ngrok version
