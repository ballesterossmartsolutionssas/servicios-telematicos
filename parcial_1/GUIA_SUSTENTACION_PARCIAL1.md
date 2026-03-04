# Guia Rapida de Sustentacion - Parcial 1

Estudiante: Juan Camilo Ballesteros Sierra  
Codigo: 2230721  
Profesor: Oscar Hernan Mondragon Martinez

## 1) Preparacion (2 minutos antes)

1. Abrir 3 ventanas:
- `CMD 1 (Host)` en `C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba`
- `CMD 2 (Servidor)` para `vagrant ssh servidor`
- `CMD 3 (Cliente)` para `vagrant ssh cliente`

2. En `CMD 1` verificar:
```bash
vagrant status
```

3. En `CMD 2` entrar al servidor:
```bash
vagrant ssh servidor
```

4. En `CMD 3` entrar al cliente:
```bash
vagrant ssh cliente
```

## 2) Punto 1 - DNS Maestro/Esclavo

En `CMD 3 (cliente)` mostrar:
```bash
dig @192.168.50.2 maestro.empresa.local +short
dig @192.168.50.2 -x 192.168.50.3 +short
dig @192.168.50.2 api2.empresa.local +short
```

Validar seguridad:
```bash
dig @192.168.50.3 empresa.local AXFR +time=2 +tries=1
dig @192.168.50.2 google.com +short
```

Prueba de failover (si te la piden):
- En `CMD 1`: `vagrant halt servidor -f`
- En `CMD 3`: repetir `dig` al esclavo (debe responder)
- En `CMD 1`: `vagrant up servidor --no-provision`

## 3) Punto 2 - Apache + Compresion

En `CMD 3 (cliente)`:
```bash
dig @192.168.50.2 parcial.juan-camilo.com +short
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -I http://parcial.juan-camilo.com/lorem.txt
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -I http://parcial.juan-camilo.com/logo.png
```

Comparacion trafico:
```bash
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: identity" -s http://parcial.juan-camilo.com/lorem.txt -o /tmp/plain.out && stat -c %s /tmp/plain.out
curl --resolve parcial.juan-camilo.com:80:192.168.50.3 -H "Accept-Encoding: gzip" -s http://parcial.juan-camilo.com/lorem.txt -o /tmp/gzip.out && stat -c %s /tmp/gzip.out
```

## 4) Punto 3 - Ngrok

En `CMD 2 (servidor)`:
```bash
bash /tmp/start_point3_ngrok_tunnel.sh
bash /tmp/verify_point3.sh
```

Si cambia URL, mostrar la nueva URL en:
`parcial_1/3_punto_ngrok/url_publica.txt`

## 5) Evidencias a mano para mostrar si preguntan

- `parcial_1/Evidencias_Parcial1_Juan_Camilo.pdf`
- `parcial_1/1_punto_dns/evidencia_punto1.txt`
- `parcial_1/2_punto_apache_compresion/evidencia_punto2_final.txt`
- `parcial_1/3_punto_ngrok/evidencia_punto3_final.txt`
- Capturas Wireshark en `parcial_1/5_evidencia_visual/`

## 6) Preguntas conceptuales tipicas (respuestas cortas)

1. Por que desactivar recursion en autoritativos?
- Para evitar open resolver y abuso en DDoS.

2. Por que restringir AXFR?
- Para evitar filtracion completa de zona a clientes no autorizados.

3. Que mejora hace gzip?
- Reduce bytes transmitidos y tiempo de carga para contenido texto.

4. Por que excluir imagenes/videos de compresion?
- Ya vienen comprimidos; recomprimir consume CPU y casi no mejora tamano.

