
# Mailbox Backup Script

Dieses Skript dient zum Erstellen von Backups von E-Mail-Postfächern auf einem Server, zur Archivierung und zum Löschen alter E-Mails. Es unterstützt mehrere Domains und Postfächer und bietet eine Vielzahl von Funktionen zur Verwaltung von E-Mail-Daten.

## Funktionen

- **Backup erstellen**: Sichert E-Mail-Postfächer in Archivdateien.
- **E-Mails löschen**: Löscht E-Mails, die älter sind als eine festgelegte Anzahl von Tagen.
- **Wiederherstellung von Backups**: Erlaubt das Wiederherstellen von Backups für Postfächer.
- **Suche innerhalb von Backups**: Ermöglicht das Suchen von E-Mails innerhalb der Backups.
- **Datenbankabgleich**: Bietet eine interaktive Benutzeroberfläche zur Auswahl von Domains und Postfächern.

## Installation

### 1. Python-Module installieren

Das Skript benötigt das `questionary` Modul, das für die interaktive Auswahl der Domains und Postfächer verantwortlich ist. Falls das Modul nicht installiert ist, wird es automatisch bei der ersten Ausführung installiert.

```bash
pipx install questionary
```

Alternativ kann das Modul auch systemweit mit `pip` installiert werden:

```bash
pip install questionary
```

### 2. Anforderungen

Das Skript setzt Python 3.x voraus. Falls auf deinem System noch kein Python 3 installiert ist, kannst du es wie folgt installieren:

```bash
sudo apt install python3
```

## Verwendung

### 1. Backup erstellen

Führe das Skript aus, um ein vollständiges Backup der ausgewählten Domains und Postfächer zu erstellen.

```bash
python3 mailbox-backup.py
```

- Das Skript fragt nach den Domains, für die Backups erstellt werden sollen.
- Danach fragt es nach der Anzahl der Tage, ab denen E-Mails gelöscht werden sollen (optional).
- Es zeigt alle verfügbaren Postfächer an und fragt, welche gesichert werden sollen.
- Es erstellt eine Archivdatei für jedes Postfach und löscht die E-Mails, wenn das Backup abgeschlossen ist.

### 2. Trockentest (Dry Run)

Wenn du zuerst testen möchtest, wie das Skript funktioniert, ohne Änderungen vorzunehmen, kannst du den Trockentest ausführen:

```bash
python3 mailbox-backup.py --dry-run
```

### 3. Wiederherstellung eines Backups

Um ein Backup wiederherzustellen, kannst du das Skript mit dem `--restore`-Befehl ausführen:

```bash
python3 mailbox-backup.py --restore
```

Das Skript fragt nach der zu wiederherstellenden Domain und Postfach und stellt das Backup wieder her.

### 4. Suche innerhalb eines Backups

Um innerhalb eines Backups nach bestimmten E-Mails zu suchen, kannst du den `--search`-Befehl verwenden:

```bash
python3 mailbox-backup.py --search
```

Das Skript fragt nach der zu durchsuchenden Domain und dem Postfach.

## Abkürzungen

- **tar**: Ein Archivformat, das verwendet wird, um E-Mail-Postfächer zu speichern.
- **dry-run**: Eine Testausführung des Skripts, die keine Änderungen vornimmt, sondern nur die zu erwartenden Aktionen anzeigt.
- **restore**: Wiederherstellung eines zuvor erstellten Backups.
- **search**: Suchen von E-Mails in einem Backup.

## Verzeichnisstruktur

Das Skript erstellt Backups im folgenden Verzeichnis:

```bash
/backup/mail/2025-04-04/
```

Die Backups werden als `.tar.gz`-Archivdateien gespeichert, wobei der Name der Datei die Domain, das Postfach und das Datum sowie die Uhrzeit der Erstellung beinhaltet.

## Logging

Das Skript protokolliert alle Aktivitäten in einer Log-Datei, die im folgenden Verzeichnis gespeichert wird:

```bash
/var/log/mailbackup/
```

Die Log-Dateien werden nach Datum und Uhrzeit benannt, z.B.:

```bash
mailbackup_2025-04-04_10-07-02.log
```

## Automatische Installation von Modulen

Wenn das benötigte Modul `questionary` nicht installiert ist, fragt das Skript automatisch, ob es installiert werden soll. Falls der Benutzer zustimmt, wird das Modul automatisch heruntergeladen und installiert.

## Lizenz

Dieses Skript ist unter der MIT-Lizenz veröffentlicht. Du kannst es nach Belieben verwenden und anpassen.
