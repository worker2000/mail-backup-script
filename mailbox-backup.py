#!/usr/bin/env python3
import os
import sys
import tarfile
import datetime
import shutil
import logging
import subprocess
import argparse
from pathlib import Path

try:
    import questionary
except ImportError:
    print("🚨 Das benötigte Modul 'questionary' ist nicht installiert.")
    print("📦 Bitte installiere es z. B. mit:")
    print("   pip install questionary")
    sys.exit(1)

# Verzeichnisse
MAIL_ROOT = Path("/var/mail/vhosts")
BACKUP_BASE = Path("/backup/mail")
LOG_DIR = Path("/var/log/mailbackup")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging vorbereiten
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logfile_path = LOG_DIR / f"mailbackup_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logfile_path),
        logging.StreamHandler(sys.stdout)
    ]
)

def list_domains():
    return sorted([d.name for d in MAIL_ROOT.iterdir() if d.is_dir()])

def list_mailboxes(domains):
    mailboxes = []
    for domain in domains:
        domain_path = MAIL_ROOT / domain
        if domain_path.exists():
            mailboxes += [domain + '/' + m.name for m in domain_path.iterdir() if m.is_dir()]
    return mailboxes

def create_backup(mailbox_path, backup_path, dry_run=False):
    mailbox_name = mailbox_path.relative_to(MAIL_ROOT).as_posix().replace('/', '_')
    filename = f"{mailbox_name}_{timestamp}.tar.gz"
    backup_file = backup_path / filename
    if dry_run:
        logging.info(f"[TEST] 📝 Backup würde erstellt: {backup_file}")
        return
    backup_path.mkdir(parents=True, exist_ok=True)
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(mailbox_path, arcname=mailbox_path.name)
    logging.info(f"✅ Archiviert: {backup_file}")

def delete_mailbox(mailbox_path, dry_run=False):
    if dry_run:
        logging.info(f"[TEST] 🧹 Mailbox würde gelöscht: {mailbox_path}")
        return
    shutil.rmtree(mailbox_path)
    logging.info(f"🗑️  Mailbox gelöscht: {mailbox_path}")

def prompt_days_old():
    return questionary.text(
        "📆 Wie alt müssen E-Mails mindestens sein, um gelöscht zu werden? (in Tagen)",
        default="90"
    ).ask()

def confirm_backup(mailboxes):
    return questionary.confirm(
        f"Sollen {len(mailboxes)} Postfächer jetzt verarbeitet werden?"
    ).ask()

def main():
    parser = argparse.ArgumentParser(description="📦 Mailbox-Backup-Tool")
    parser.add_argument("--dry-run", action="store_true", help="Nur testen, keine echten Backups löschen oder schreiben")
    parser.add_argument("--restore", metavar="PFAD", help="Ein Backup wiederherstellen")
    parser.add_argument("--search", metavar="BEGRIFF", help="In Backups suchen")
    args = parser.parse_args()

    logging.info(f"📋 Log-Datei: {logfile_path}")

    # Wiederherstellung
    if args.restore:
        path = Path(args.restore)
        if not path.exists():
            logging.error(f"❌ Backup-Datei nicht gefunden: {path}")
            return
        dest = MAIL_ROOT / path.stem.split('_')[0].replace('.', '/')
        if dest.exists():
            overwrite = questionary.confirm(f"⚠️ Zielverzeichnis {dest} existiert. Überschreiben?").ask()
            if not overwrite:
                logging.info("❌ Wiederherstellung abgebrochen.")
                return
            shutil.rmtree(dest)
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(path=dest.parent)
        logging.info(f"✅ Backup wiederhergestellt nach {dest}")
        return

    # Suche
    if args.search:
        search_term = args.search
        logging.info(f"🔍 Suche nach '{search_term}' in Backups...")
        for f in BACKUP_BASE.rglob("*.tar.gz"):
            if search_term in f.name:
                print(f"🔎 {f}")
        return

    # Auswahl der Domains
    all_domains = list_domains()
    selected_domains = questionary.checkbox(
        "Welche Domains sollen gesichert werden?",
        choices=all_domains
    ).ask()

    if not selected_domains:
        logging.info("❌ Keine Domains ausgewählt. Abbruch.")
        return

    logging.info(f"✅ Starte Backup für: {', '.join(selected_domains)}")

    # Alter der E-Mails
    days_old = prompt_days_old()
    try:
        days_old = int(days_old)
    except ValueError:
        logging.error("❌ Ungültige Eingabe. Bitte eine ganze Zahl angeben.")
        return

    mailboxes = list_mailboxes(selected_domains)
    if not mailboxes:
        logging.warning("⚠️ Keine Postfächer gefunden.")
        return

    if not confirm_backup(mailboxes):
        logging.info("🚫 Vorgang abgebrochen.")
        return

    # Backup-Ordner vorbereiten
    backup_folder = BACKUP_BASE / datetime.datetime.now().strftime("%Y-%m-%d")

    for box in mailboxes:
        box_path = MAIL_ROOT / box
        # Prüfung auf E-Mail-Alter: wir löschen nur, wenn Dateien älter als X Tage
        mtime = datetime.datetime.fromtimestamp(box_path.stat().st_mtime)
        if (datetime.datetime.now() - mtime).days < days_old:
            logging.info(f"⏩ Überspringe (zu neu): {box_path}")
            continue
        logging.info(f"📦 Backup von {box} wird erstellt...")
        create_backup(box_path, backup_folder, dry_run=args.dry_run)
        delete_mailbox(box_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
