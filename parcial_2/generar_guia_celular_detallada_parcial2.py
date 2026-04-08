#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "GUIA_CELULAR_PARCIAL2_DETALLADA.pdf"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def add_p(story, text: str, style) -> None:
    story.append(Paragraph(esc(text), style))


def add_cmd(story, text: str, style) -> None:
    story.append(Paragraph(esc(text), style))
    story.append(Spacer(1, 0.10 * cm))


def add_bullet(story, text: str, style) -> None:
    story.append(Paragraph(f"- {esc(text)}", style))


def add_gap(story, h: float = 0.14) -> None:
    story.append(Spacer(1, h * cm))


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=1.2 * cm,
        rightMargin=1.2 * cm,
        topMargin=1.1 * cm,
        bottomMargin=1.1 * cm,
        title="Guia Celular Parcial 2 Detallada",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleX",
        parent=styles["Title"],
        fontSize=17,
        leading=20,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=6,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor("#0b2e59"),
        spaceBefore=7,
        spaceAfter=4,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=10.8,
        leading=13,
        textColor=colors.HexColor("#184c8c"),
        spaceBefore=5,
        spaceAfter=3,
    )
    p = ParagraphStyle(
        "P",
        parent=styles["Normal"],
        fontSize=9.4,
        leading=12,
        spaceAfter=2,
    )
    bullet = ParagraphStyle(
        "BulletX",
        parent=p,
        leftIndent=0.25 * cm,
    )
    mono = ParagraphStyle(
        "Mono",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.1,
        leading=9.4,
        textColor=colors.HexColor("#202020"),
        backColor=colors.HexColor("#f3f6fa"),
        borderPadding=3.5,
        borderColor=colors.HexColor("#d8e2ee"),
        borderWidth=0.35,
    )

    s = []
    add_p(s, "Guia Celular Detallada - Parcial 2", title)
    add_p(s, "Usa esta guia literal. Dice qué terminal usar, qué comando va ahí y qué decir.", p)
    add_p(s, r"PDF grande: C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba\parcial1_entrega\parcial_2\GUIA_SUSTENTACION_PARCIAL2_COMPLETA.pdf", p)
    add_gap(s)

    add_p(s, "1. Qué Debe Estar Abierto", h1)
    add_bullet(s, "Terminal 1: Host Windows en la carpeta prueba.", bullet)
    add_bullet(s, "Terminal 2: servidor por vagrant ssh servidor.", bullet)
    add_bullet(s, "Terminal 3: cliente por vagrant ssh cliente.", bullet)
    add_bullet(s, "Wireshark con 11_ftps_tls_ok.pcapng, 06_dot_853.pcapng, 07_dns_53.pcapng y 10_sftp_22_ok.pcapng.", bullet)
    add_bullet(s, "No uses 08_ftps_tls.pcapng ni 09_sftp_22.pcapng porque quedaron vacíos.", bullet)
    add_gap(s)

    add_p(s, "2. Preparar Las 3 Terminales", h1)
    add_p(s, "Terminal 1 - Host Windows", h2)
    add_cmd(s, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(s, "vagrant status", mono)
    add_p(s, "Qué decir: aquí verifico que cliente y servidor están corriendo.", p)

    add_p(s, "Terminal 2 - Servidor", h2)
    add_cmd(s, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(s, "vagrant ssh servidor", mono)
    add_cmd(s, "hostnamectl", mono)
    add_cmd(s, "ip -brief addr", mono)
    add_cmd(s, "sudo ufw status verbose", mono)
    add_p(s, "Qué decir: el servidor tiene la IP 192.168.50.3 y está protegido por UFW.", p)

    add_p(s, "Terminal 3 - Cliente", h2)
    add_cmd(s, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(s, "vagrant ssh cliente", mono)
    add_cmd(s, "hostnamectl", mono)
    add_cmd(s, "ip -brief addr", mono)
    add_cmd(s, "ping -c 2 192.168.50.3", mono)
    add_p(s, "Qué decir: el cliente tiene la IP 192.168.50.2 y alcanza al servidor.", p)

    add_p(s, "3. Punto 1 - FTPS + UFW", h1)
    add_p(s, "Terminal 2 - Servidor", h2)
    add_cmd(s, "sudo cat /etc/vsftpd.conf", mono)
    add_cmd(s, "sudo ls -l /etc/ssl/telematicos", mono)
    add_cmd(s, "sudo ufw status verbose", mono)
    add_p(s, "Qué decir:", p)
    add_bullet(s, "vsftpd está configurado en FTPS con TLS explícito.", bullet)
    add_bullet(s, "El certificado del servidor y la CA están cargados.", bullet)
    add_bullet(s, "UFW solo permite 21 para control, 50000:50010 para datos pasivos y 22 para SSH.", bullet)

    add_p(s, "Demostración de bloqueo del puerto 21", h2)
    add_p(s, "Terminal 2 - Servidor", p)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh close", mono)
    add_p(s, "Qué decir: ahora cierro temporalmente 21/tcp para demostrar que el firewall bloquea FTPS.", p)

    add_p(s, "Terminal 3 - Cliente", p)
    add_cmd(s, "openssl s_client -connect 192.168.50.3:21 -starttls ftp -CAfile /vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt < /dev/null", mono)
    add_p(s, "Qué decir: con 21 cerrado, el canal de control FTP no negocia y la conexión falla.", p)

    add_p(s, "Reabrir y validar FTPS", h2)
    add_p(s, "Terminal 2 - Servidor", p)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh open", mono)
    add_p(s, "Terminal 3 - Cliente", p)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/verify_ftps_ufw.sh", mono)
    add_p(s, "Qué decir:", p)
    add_bullet(s, "Verify return code 0 indica que el certificado fue validado correctamente.", bullet)
    add_bullet(s, "Luego se hace ls, put y get sobre FTPS.", bullet)
    add_bullet(s, "Los sha256 iguales demuestran integridad.", bullet)
    add_bullet(s, "El contenido del archivo no aparece en texto plano.", bullet)
    add_p(s, "Wireshark para FTPS:", p)
    add_bullet(s, "Abre 11_ftps_tls_ok.pcapng.", bullet)
    add_bullet(s, "Qué señalar: Response 220, Request AUTH TLS, Response 234 Proceed with negotiation.", bullet)
    add_bullet(s, "Luego señalar Client Hello, Server Hello y después Application Data.", bullet)
    add_bullet(s, "Qué decir: aquí se ve el canal de control por 21 y luego el tráfico queda cifrado por TLS.", bullet)

    add_p(s, "4. Punto 2 - DNS Over TLS", h1)
    add_p(s, "Terminal 3 - Cliente", h2)
    add_cmd(s, "sudo cat /etc/systemd/resolved.conf", mono)
    add_cmd(s, "resolvectl status | sed -n '1,80p'", mono)
    add_cmd(s, "resolvectl query openai.com", mono)
    add_cmd(s, "resolvectl query uao.edu.co", mono)
    add_cmd(s, "resolvectl query github.com", mono)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/verify_dot.sh", mono)
    add_p(s, "Qué decir:", p)
    add_bullet(s, "systemd-resolved quedó con DNSOverTLS=yes.", bullet)
    add_bullet(s, "Los DNS configurados son 1.1.1.1 y 8.8.8.8, con fallback compatibles.", bullet)
    add_bullet(s, "Las consultas funcionan y salen por transporte cifrado.", bullet)

    add_p(s, "Wireshark para DoT", h2)
    add_bullet(s, "Abre 06_dot_853.pcapng.", bullet)
    add_bullet(s, "Qué señalar: puerto 853, TLSv1.2 o Application Data.", bullet)
    add_bullet(s, "Qué decir: aquí el tráfico DNS va cifrado sobre TLS.", bullet)
    add_bullet(s, "Abre 07_dns_53.pcapng.", bullet)
    add_bullet(s, "Qué señalar: protocolo DNS y dominio example.net visible en claro.", bullet)
    add_bullet(s, "Qué decir: aquí sí se expone el nombre consultado.", bullet)

    add_p(s, "5. Punto 3 - SFTP + UFW", h1)
    add_p(s, "Terminal 2 - Servidor", h2)
    add_cmd(s, "sudo cat /etc/ssh/sshd_config", mono)
    add_cmd(s, "sudo systemctl --no-pager --full status ssh | sed -n '1,12p'", mono)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh close", mono)
    add_p(s, "Qué decir: SFTP corre sobre OpenSSH y usa solo el puerto 22.", p)

    add_p(s, "Terminal 3 - Cliente", h2)
    add_cmd(s, "sshpass -p 'Telemat1cos!' sftp -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no telematico@192.168.50.3", mono)
    add_p(s, "Qué decir: con 22 cerrado, la sesión SFTP falla porque todo depende del canal SSH.", p)
    add_bullet(s, "Si aparece sftp>, salir con bye.", bullet)

    add_p(s, "Terminal 2 - Servidor", h2)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh open", mono)

    add_p(s, "Terminal 3 - Cliente", h2)
    add_cmd(s, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/verify_sftp_ufw.sh", mono)
    add_p(s, "Qué decir:", p)
    add_bullet(s, "Aquí se hace ls, put y get usando SFTP.", bullet)
    add_bullet(s, "Los hashes iguales demuestran integridad.", bullet)
    add_bullet(s, "La captura muestra tráfico SSH cifrado.", bullet)

    add_p(s, "Wireshark para SFTP", h2)
    add_bullet(s, "Abre 10_sftp_22_ok.pcapng.", bullet)
    add_bullet(s, "Filtro: tcp.port == 22.", bullet)
    add_bullet(s, "Qué señalar: protocolo SSH y líneas Server: Encrypted packet / Client: Encrypted packet.", bullet)
    add_bullet(s, "Qué decir: todo viaja dentro de SSH y no se ve ni la clave ni el archivo en texto plano.", bullet)

    add_p(s, "6. Punto 19 - Comparación FTPS vs SFTP", h1)
    add_p(s, "Terminal 3 o 2", h2)
    add_cmd(s, "cat /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/TABLA_COMPARATIVA_FTPS_VS_SFTP.md", mono)
    add_p(s, "Qué decir:", p)
    add_bullet(s, "FTPS: FTP + TLS, usa 21 y rango pasivo.", bullet)
    add_bullet(s, "SFTP: SSH, usa solo 22.", bullet)
    add_bullet(s, "FTPS necesita coordinar mejor servicio y firewall.", bullet)
    add_bullet(s, "SFTP es más simple para firewalls estrictos porque concentra todo en 22.", bullet)

    add_p(s, "7. Si Te Bloqueas", h1)
    add_bullet(s, "Si ves vagrant@cliente:~$ o vagrant@servidor:~$, puedes correr bash normal.", bullet)
    add_bullet(s, "Si ves sftp>, solo usa ls o bye.", bullet)
    add_bullet(s, "Si una VM se daña, en Host: vagrant reload servidor o vagrant reload cliente.", bullet)

    add_p(s, "8. Cierre Final", h1)
    add_bullet(s, "Mostré FTPS protegido con UFW y validado con TLS.", bullet)
    add_bullet(s, "Mostré DNS over TLS y su comparación con DNS sin cifrar.", bullet)
    add_bullet(s, "Mostré SFTP protegido por UFW y tráfico SSH cifrado.", bullet)
    add_bullet(s, "Concluí que SFTP es más adecuado para un firewall estricto por usar un solo puerto.", bullet)

    doc.build(s)
    print(f"PDF generado: {OUT_PDF}")


if __name__ == "__main__":
    main()
