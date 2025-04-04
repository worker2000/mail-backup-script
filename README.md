# Mailbox Backup Script

Ein Python-Skript zum Archivieren und Löschen von großen Mailboxen auf einem Mailserver. Nützlich für Systeme mit `/var/mail/vhosts` Struktur.

## Funktionen
- Archiviert jede Mailbox als `.tar.gz` mit Zeitstempel
- Legt Backups nach Datum in `/backup/mail/YYYY-MM-DD` ab
- Löscht Mailboxinhalt nach erfolgreicher Sicherung
- Unterstützt Live-Logging und Trockentest-Modus
- Log-Dateien unter `/var/log/mailbackup/`

## Nutzung

```bash
sudo python3 /usr/local/bin/mailbox_backup.py
```

Trockentest-Modus (zeigt nur an, was gemacht würde):

```bash
sudo python3 /usr/local/bin/mailbox_backup.py --dry-run
```

## Beispiel-Ausgabe

```text
📦 Backup von familieflessing.de/domains wird erstellt...
✅ Archiviert: /backup/mail/2025-04-04/familieflessing.de_domains_2025-04-04_08-00-00.tar.gz
🗑️  Mailbox gelöscht: /var/mail/vhosts/familieflessing.de/domains
```
