# Guia de Contingencia - Sustentacion Parcial 1

Estudiante: Juan Camilo Ballesteros Sierra  
Codigo: 2230721  
Profesor: Oscar Hernan Mondragon Martinez

Objetivo: tener comandos listos para resolver en caliente cualquier ajuste o falla durante la sustentacion.

## 0) Ventanas recomendadas

1. `CMD 1 (Host)` en `.../Servicios telematicos/prueba`
2. `CMD 2 (Servidor)` con `vagrant ssh servidor`
3. `CMD 3 (Cliente)` con `vagrant ssh cliente`

## 1) Comandos base de estado

En `CMD 1`:
```bash
vagrant status
```

En `CMD 2 (servidor)`:
```bash
hostname
ip -4 a show eth1
sudo systemctl is-active named
sudo systemctl is-active apache2
```

En `CMD 3 (cliente)`:
```bash
hostname
ip -4 a show eth1
sudo systemctl is-active named
```

## 2) Punto 1 DNS - Validacion rapida

En `cliente`:
```bash
dig @192.168.50.2 maestro.empresa.local +short
dig @192.168.50.2 -x 192.168.50.3 +short
dig @192.168.50.2 api2.empresa.local +short
dig @192.168.50.2 parcial.juan-camilo.com +short
```

Seguridad:
```bash
dig @192.168.50.3 empresa.local AXFR +time=2 +tries=1
dig @192.168.50.2 google.com +short
```

Esperado:
- AXFR no autorizado: `Transfer failed`
- Recursion externa: vacio/no resuelve

## 3) Punto 1 DNS - Si algo falla

### A) named caido
Servidor o cliente:
```bash
sudo systemctl restart named
sudo systemctl status named --no-pager -n 30
```

### B) Error de configuracion BIND
```bash
sudo named-checkconf
sudo named-checkzone empresa.local /etc/bind/db.empresa.local
sudo named-checkzone 50.168.192.in-addr.arpa /etc/bind/db.192.168.50
sudo named-checkzone juan-camilo.com /etc/bind/db.juan-camilo.com
```

### C) Esclavo no sincroniza zona
En `cliente`:
```bash
sudo rndc retransfer empresa.local
sudo rndc retransfer 50.168.192.in-addr.arpa
sudo rndc retransfer juan-camilo.com
sudo journalctl -u named --since "20 minutes ago" --no-pager | tail -n 80
```

### D) Cambio en maestro no se refleja
En `servidor`:
```bash
sudo named-checkzone empresa.local /etc/bind/db.empresa.local
sudo rndc reload empresa.local
sudo systemctl restart named
```

En `cliente`:
```bash
dig @192.168.50.2 empresa.local SOA +short
```

## 4) Punto 2 Apache + gzip - Validacion rapida

En `cliente`:
```bash
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -I http://parcial.juan-camilo.com/lorem.txt
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -I http://parcial.juan-camilo.com/logo.png
```

Esperado:
- `lorem.txt`: `Content-Encoding: gzip`
- `logo.png`: SIN `Content-Encoding`

Comparacion de tamano:
```bash
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: identity" -s http://parcial.juan-camilo.com/lorem.txt -o /tmp/plain.out && stat -c %s /tmp/plain.out
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -s http://parcial.juan-camilo.com/lorem.txt -o /tmp/gzip.out && stat -c %s /tmp/gzip.out
```

## 5) Punto 2 Apache - Si algo falla

### A) Apache caido o error de sitio
En `servidor`:
```bash
sudo apache2ctl configtest
sudo systemctl restart apache2
sudo systemctl status apache2 --no-pager -n 40
```

### B) Gzip no aparece
```bash
sudo apache2ctl -M | egrep "deflate|headers"
sudo cat /etc/apache2/conf-available/parcial-compression.conf
sudo a2enmod deflate headers
sudo a2enconf parcial-compression
sudo systemctl reload apache2
```

### C) Host llega a otro vhost / 404 raro
```bash
ls -l /etc/apache2/sites-enabled
sudo a2dissite 000-default miotrositio.com servicios.com 2>/dev/null || true
sudo a2ensite parcial
sudo systemctl reload apache2
```

## 6) Wireshark - filtro y contingencia

Filtros utiles:
```text
http && ip.addr == 192.168.50.3
ip.addr == 192.168.50.3 && tcp.port == 80
```

Si `logo.png` sale 304:
- usar URL con query para forzar nueva respuesta:
```text
http://parcial.juan-camilo.com/logo.png?x=12346
```

## 7) Punto 3 ngrok - Validacion rapida

En `servidor`:
```bash
bash /tmp/start_point3_ngrok_tunnel.sh
bash /tmp/verify_point3.sh
```

Si `/tmp` se limpio tras reinicio:
```bash
SRC=/vagrant/parcial1_entrega/parcial_1/3_punto_ngrok/scripts
[ -f "$SRC/start_point3_ngrok_tunnel.sh" ] || SRC=/vagrant/scripts
tr -d '\r' < "$SRC/start_point3_ngrok_tunnel.sh" > /tmp/start_point3_ngrok_tunnel.sh
tr -d '\r' < "$SRC/verify_point3.sh" > /tmp/verify_point3.sh
chmod +x /tmp/start_point3_ngrok_tunnel.sh /tmp/verify_point3.sh
```

Si ngrok no conecta:
```bash
tail -n 60 /tmp/ngrok_http80.log
curl -s http://127.0.0.1:4040/api/tunnels | jq .
```

## 8) Failover DNS (demo instantanea)

En `CMD 1`:
```bash
vagrant halt servidor -f
```

En `cliente`:
```bash
dig @192.168.50.2 maestro.empresa.local +short
dig @192.168.50.2 -x 192.168.50.3 +short
```

Reactivar maestro:
```bash
vagrant up servidor --no-provision
```

## 9) Preguntas conceptuales (respuesta corta)

1. Por que `recursion no` en autoritativos?
- Evita open resolver y abuso en ataques DDoS.

2. Por que restringir AXFR?
- Para evitar que cualquiera descargue la zona completa.

3. Por que gzip mejora rendimiento?
- Reduce bytes en texto (HTML/CSS/JS/TXT), mejora transferencia.

4. Por que excluir imagenes y video?
- Ya suelen estar comprimidos; recomprimir consume CPU y aporta poco.

5. Diferencia maestro/esclavo?
- Maestro edita zona; esclavo replica por transferencia (AXFR/IXFR).

## 10) Archivos que debes tener abiertos

1. `parcial_1/Evidencias_Parcial1_Juan_Camilo.pdf`
2. `parcial_1/GUIA_SUSTENTACION_PARCIAL1.pdf`
3. `parcial_1/3_punto_ngrok/url_publica.txt`
4. Repo: `https://github.com/ballesterossmartsolutionssas/servicios-telematicos`

