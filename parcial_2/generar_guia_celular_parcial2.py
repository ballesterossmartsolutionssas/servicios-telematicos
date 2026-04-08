#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "GUIA_CELULAR_PARCIAL2.pdf"


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")


def add_cmd(story, text: str, style) -> None:
    story.append(Paragraph(esc(text), style))
    story.append(Spacer(1, 0.12 * cm))


def add_line(story, text: str, style) -> None:
    story.append(Paragraph(esc(text), style))


def add_bullet(story, text: str, style) -> None:
    story.append(Paragraph(f"- {esc(text)}", style))


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=1.3 * cm,
        rightMargin=1.3 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
        title="Guia Celular Parcial 2",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleX",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=8,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0b2e59"),
        spaceBefore=8,
        spaceAfter=5,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#184c8c"),
        spaceBefore=5,
        spaceAfter=4,
    )
    p = ParagraphStyle(
        "P",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        spaceAfter=3,
    )
    bullet = ParagraphStyle(
        "BulletX",
        parent=p,
        leftIndent=0.3 * cm,
        spaceAfter=2,
    )
    mono = ParagraphStyle(
        "Mono",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.3,
        leading=9.8,
        textColor=colors.HexColor("#202020"),
        backColor=colors.HexColor("#f4f7fb"),
        borderPadding=4,
        borderColor=colors.HexColor("#d8e2ee"),
        borderWidth=0.4,
    )

    story = []
    story.append(Paragraph("Guia Celular - Parcial 2", title))
    add_line(story, "Ruta del PDF grande: C:\\Users\\USUARIO\\Desktop\\UAO 2026 SEMESTRE 1\\Servicios telematicos\\prueba\\parcial1_entrega\\parcial_2\\GUIA_SUSTENTACION_PARCIAL2_COMPLETA.pdf", p)
    add_line(story, "Topologia: cliente 192.168.50.2 | servidor 192.168.50.3", p)
    add_line(story, "Orden: FTPS -> DoT -> SFTP -> comparacion final", p)
    story.append(Spacer(1, 0.15 * cm))

    story.append(Paragraph("1. Antes De Entrar", h1))
    add_bullet(story, "Abre 3 terminales: Host, Servidor y Cliente.", bullet)
    add_bullet(story, "Deja abierto este PDF y Wireshark con 06_dot_853, 07_dns_53 y 10_sftp_22_ok.", bullet)
    add_bullet(story, "No uses 08_ftps_tls ni 09_sftp_22 porque quedaron vacios.", bullet)
    add_line(story, "Host Windows:", h2)
    add_cmd(story, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(story, "vagrant status", mono)
    add_line(story, "Servidor:", h2)
    add_cmd(story, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(story, "vagrant ssh servidor", mono)
    add_line(story, "Cliente:", h2)
    add_cmd(story, r'cd "C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba"', mono)
    add_cmd(story, "vagrant ssh cliente", mono)

    story.append(Paragraph("2. Inicio Rapido", h1))
    add_line(story, "Host:", h2)
    add_cmd(story, "vagrant status", mono)
    add_line(story, "Servidor:", h2)
    add_cmd(story, "hostnamectl", mono)
    add_cmd(story, "ip -brief addr", mono)
    add_cmd(story, "sudo ufw status verbose", mono)
    add_line(story, "Cliente:", h2)
    add_cmd(story, "hostnamectl", mono)
    add_cmd(story, "ip -brief addr", mono)
    add_cmd(story, "ping -c 2 192.168.50.3", mono)
    add_bullet(story, "Qué decir: tengo cliente y servidor Ubuntu; el servidor está protegido por UFW.", bullet)

    story.append(Paragraph("3. Punto 1 - FTPS + UFW", h1))
    add_line(story, "Servidor primero:", h2)
    add_cmd(story, "sudo cat /etc/vsftpd.conf", mono)
    add_cmd(story, "sudo ls -l /etc/ssl/telematicos", mono)
    add_cmd(story, "sudo ufw status verbose", mono)
    add_bullet(story, "Qué decir: FTPS usa 21 para control, 50000 a 50010 para datos pasivos y 22 para SSH.", bullet)
    add_line(story, "Demostracion de bloqueo:", h2)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh close", mono)
    add_line(story, "Cliente prueba fallida:", h2)
    add_cmd(story, "openssl s_client -connect 192.168.50.3:21 -starttls ftp -CAfile /vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt < /dev/null", mono)
    add_bullet(story, "Qué decir: con 21 cerrado, el canal de control FTPS no negocia.", bullet)
    add_line(story, "Reabrir y validar:", h2)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh open", mono)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/verify_ftps_ufw.sh", mono)
    add_bullet(story, "Qué decir: Verify return code 0 valida el certificado; luego se hace ls, put y get.", bullet)
    add_bullet(story, "Qué decir: los hashes iguales prueban integridad y el contenido no aparece en texto plano.", bullet)

    story.append(Paragraph("4. Punto 2 - DNS Over TLS", h1))
    add_line(story, "Cliente:", h2)
    add_cmd(story, "sudo cat /etc/systemd/resolved.conf", mono)
    add_cmd(story, "resolvectl status | sed -n '1,80p'", mono)
    add_cmd(story, "resolvectl query openai.com", mono)
    add_cmd(story, "resolvectl query uao.edu.co", mono)
    add_cmd(story, "resolvectl query github.com", mono)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/verify_dot.sh", mono)
    add_bullet(story, "Qué decir: aquí DNSOverTLS=yes y los DNS públicos compatibles están configurados.", bullet)
    add_bullet(story, "Qué decir: por 853 veo TLS/Application Data; por 53 sí veo el dominio en texto claro.", bullet)
    add_line(story, "Wireshark mostrar:", h2)
    add_bullet(story, "06_dot_853.pcapng: tráfico TLS sobre 853.", bullet)
    add_bullet(story, "07_dns_53.pcapng: se ve example.net en claro.", bullet)

    story.append(Paragraph("5. Punto 3 - SFTP + UFW", h1))
    add_line(story, "Servidor:", h2)
    add_cmd(story, "sudo cat /etc/ssh/sshd_config", mono)
    add_cmd(story, "sudo systemctl --no-pager --full status ssh | sed -n '1,12p'", mono)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh close", mono)
    add_bullet(story, "Qué decir: SFTP funciona sobre SSH y usa un único puerto, el 22.", bullet)
    add_line(story, "Cliente prueba fallida:", h2)
    add_cmd(story, "sshpass -p 'Telemat1cos!' sftp -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no telematico@192.168.50.3", mono)
    add_bullet(story, "Si aparece sftp>, salir con bye.", bullet)
    add_line(story, "Servidor reabre:", h2)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh open", mono)
    add_line(story, "Cliente valida:", h2)
    add_cmd(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/verify_sftp_ufw.sh", mono)
    add_bullet(story, "Qué decir: aquí se hace ls, put y get dentro del canal SSH.", bullet)
    add_bullet(story, "Qué decir: los hashes iguales prueban integridad y Wireshark muestra paquetes SSH cifrados.", bullet)
    add_line(story, "Wireshark mostrar:", h2)
    add_bullet(story, "10_sftp_22_ok.pcapng con filtro tcp.port == 22.", bullet)
    add_bullet(story, "Frase: no se ven credenciales ni contenido del archivo en texto plano.", bullet)

    story.append(Paragraph("6. Comparacion FTPS vs SFTP", h1))
    add_cmd(story, "cat /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/TABLA_COMPARATIVA_FTPS_VS_SFTP.md", mono)
    add_bullet(story, "FTPS: FTP + TLS, usa 21 y rango pasivo.", bullet)
    add_bullet(story, "SFTP: SSH, usa solo 22.", bullet)
    add_bullet(story, "Conclusión: SFTP es mejor para firewall estricto porque usa un único puerto y es más simple de administrar.", bullet)

    story.append(Paragraph("7. Si Te Enredas", h1))
    add_bullet(story, "Si ves vagrant@cliente:~$ o vagrant@servidor:~$, estás en shell normal.", bullet)
    add_bullet(story, "Si ves sftp>, ahí no pegues comandos bash; usa ls o bye.", bullet)
    add_bullet(story, "Si algo raro pasa, en Host: vagrant reload servidor o vagrant reload cliente.", bullet)

    story.append(Paragraph("8. Cierre", h1))
    add_bullet(story, "Mostré FTPS con TLS explícito protegido por UFW.", bullet)
    add_bullet(story, "Mostré DNS over TLS con systemd-resolved.", bullet)
    add_bullet(story, "Mostré SFTP sobre OpenSSH protegido por UFW.", bullet)
    add_bullet(story, "Validé funcionamiento real, cifrado y comparación final entre FTPS y SFTP.", bullet)

    doc.build(story)
    print(f"PDF generado: {OUT_PDF}")


if __name__ == "__main__":
    main()
