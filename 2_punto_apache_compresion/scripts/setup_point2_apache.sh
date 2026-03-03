#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 curl

sudo mkdir -p /var/www/parcial

cat <<'EOF' | sudo tee /var/www/parcial/index.html >/dev/null
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Parcial Servicios Telematicos</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <main>
    <h1>Punto 2 y Punto 3 - Servicios Telematicos</h1>
    <p>Servidor Apache con compresion gzip habilitada por mod_deflate.</p>
    <p>Dominio local: parcial.juan-camilo.com</p>
    <img src="/logo.png" alt="logo demo" width="120">
    <script src="/app.js"></script>
  </main>
</body>
</html>
EOF

cat <<'EOF' | sudo tee /var/www/parcial/styles.css >/dev/null
body { font-family: Arial, sans-serif; margin: 2rem; background: #f5f7fa; color: #1f2937; }
h1 { color: #0f172a; }
p { line-height: 1.5; }
main { max-width: 900px; background: #fff; padding: 1.5rem; border: 1px solid #d1d5db; }
EOF

cat <<'EOF' | sudo tee /var/www/parcial/app.js >/dev/null
document.addEventListener("DOMContentLoaded", () => {
  console.log("Sitio de parcial cargado correctamente.");
});
EOF

# Small static image placeholder (already compressed-like binary).
sudo bash -c 'head -c 40960 /dev/urandom > /var/www/parcial/logo.png'

# Large text file to compare compressed vs non-compressed traffic.
sudo bash -c 'yes "Este es un archivo de prueba para compresion HTTP en Apache. " | head -n 12000 > /var/www/parcial/lorem.txt'

cat <<'EOF' | sudo tee /etc/apache2/sites-available/parcial.conf >/dev/null
<VirtualHost *:80>
    ServerName parcial.juan-camilo.com
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/parcial

    <Directory /var/www/parcial>
        AllowOverride None
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/parcial_error.log
    CustomLog ${APACHE_LOG_DIR}/parcial_access.log combined
</VirtualHost>
EOF

cat <<'EOF' | sudo tee /etc/apache2/conf-available/parcial-compression.conf >/dev/null
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/css text/javascript application/javascript application/json application/xml text/xml image/svg+xml
</IfModule>

<IfModule mod_headers.c>
    Header append Vary Accept-Encoding
</IfModule>

# Exclude already compressed or binary-heavy formats.
SetEnvIfNoCase Request_URI "\.(?:gif|jpe?g|png|webp|avif|mp4|avi|mkv|mov|zip|gz|bz2|7z|rar|pdf)$" no-gzip dont-vary
EOF

sudo a2enmod deflate headers
sudo a2enconf parcial-compression
sudo a2ensite parcial
sudo a2dissite 000-default || true
sudo apache2ctl configtest
sudo systemctl enable --now apache2
sudo systemctl restart apache2
sudo systemctl --no-pager --full status apache2 | sed -n '1,10p'
