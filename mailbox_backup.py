#!/usr/bin/env python3
import os
import tarfile
import shutil
from datetime import datetime
import logging
import argparse

# Konfiguration
MAILBOX_BASE = "/var/mail/vhosts"
BACKUP_BASE = "/backup/mail"
LOG_DIR = "/var/log/mailbackup"

# Sicherstellen, dass das Log-Verzeichnis existiert
os.makedirs(LOG_DIR, exist_ok=True)

# Aktueller Zeitstempel
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# Logger konfigurieren
log_filename = f"mailbackup_{time_str}.log"
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

def create_backup(mailbox_path, rel_path, backup_dir, dry_run=False):
    mailbox_name = rel_path.replace("/", "_")
    archive_name = f"{mailbox_name}_{time_str}.tar.gz"
    archive_path = os.path.join(backup_dir, archive_name)

    logging.info(f"📦 Backup von {rel_path} wird erstellt...")
    if dry_run:
        logging.info(f"🧪 [TROCKEN] Würde archivieren: {mailbox_path} -> {archive_path}")
        return

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(mailbox_path, arcname=os.path.basename(mailbox_path))
        logging.info(f"✅ Archiviert: {archive_path}")

        # Mailbox löschen
        shutil.rmtree(mailbox_path)
        logging.info(f"🗑️  Mailbox gelöscht: {mailbox_path}")
    except Exception as e:
        logging.error(f"❌ Fehler beim Verarbeiten von {mailbox_path}: {e}")

def main(dry_run=False):
    backup_dir = os.path.join(BACKUP_BASE, date_str)
    os.makedirs(backup_dir, exist_ok=True)

    for domain in os.listdir(MAILBOX_BASE):
        domain_path = os.path.join(MAILBOX_BASE, domain)
        if not os.path.isdir(domain_path):
            continue
        for user in os.listdir(domain_path):
            mailbox_path = os.path.join(domain_path, user)
            if os.path.isdir(mailbox_path):
                rel_path = f"{domain}/{user}"
                create_backup(mailbox_path, rel_path, backup_dir, dry_run=dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mailbox Backup und Lösch-Skript")
    parser.add_argument("--dry-run", action="store_true", help="Führe einen Trockentest durch (kein Backup, kein Löschen)")
    args = parser.parse_args()

    main(dry_run=args.dry_run)
