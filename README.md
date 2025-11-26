# 🌈 Vibecheck Bot

Ein freundlicher Mastodon-Bot, der mit sanften Erinnerungen über toxisches Social-Media-Verhalten aufklärt.

## 💭 Konzept

Der Bot postet 2-3x pro Woche kurze, liebevolle Nachrichten über problematische Online-Praktiken wie Engagement Bait, Rage Bait, Doomscrolling, Flamebaiting, Dogwhistling und mehr. Ziel ist Aufklärung ohne Moralpredigt – subtil, sympathisch und hilfreich.

## 🚀 Installation

```bash
# Repository klonen
git clone https://github.com/deinusername/vibecheck-bot.git
cd vibecheck-bot

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install Mastodon.py
```

## ⚙️ Konfiguration

1. **Mastodon App erstellen:**
   - Gehe zu Einstellungen → Entwicklung auf deiner Instanz
   - Erstelle neue Anwendung mit `write:statuses` Berechtigung
   - Kopiere das Access Token

2. **`.env` Datei erstellen:**
```bash
MASTODON_TOKEN=dein-access-token
MASTODON_INSTANCE=https://deine-instanz.social
```

3. **Nachrichten anpassen:**
   - Bearbeite `messages.csv` nach Belieben
   - Format: `id,category,text`

## 🤖 Verwendung

```bash
# Dry-Run (zeigt Nachricht ohne zu posten)
python mastodon_bot.py --dry-run

# Nachricht posten
python mastodon_bot.py
```

## ⏰ Automatisierung mit Cron

```bash
crontab -e

# 2-3x pro Woche posten (Mo 10:00, Mi 15:00, Fr 12:00)
0 10 * * 1 cd /pfad/zum/bot && /pfad/zum/bot/venv/bin/python mastodon_bot.py
0 15 * * 3 cd /pfad/zum/bot && /pfad/zum/bot/venv/bin/python mastodon_bot.py
0 12 * * 5 cd /pfad/zum/bot && /pfad/zum/bot/venv/bin/python mastodon_bot.py
```

## 📝 Nachrichten erweitern

Füge einfach neue Zeilen zu `messages.csv` hinzu:
```csv
101,neue_kategorie,"💡 Deine neue Nachricht hier (max 500 Zeichen)"
```

Der Bot wählt zufällig aus und trackt bereits gepostete Nachrichten in `bot_state.json`.

## 📂 Projektstruktur

```
.
├── mastodon_bot.py      # Bot-Script
├── messages.csv         # Nachrichten-Datenbank
├── .env                 # Konfiguration (nicht in Git!)
├── bot_state.json       # Tracking geposteter Nachrichten
└── README.md
```

## 🤝 Beitragen

Pull Requests für neue Nachrichten oder Verbesserungen sind willkommen! Besonders gesucht:
- Neue toxische Praktiken
- Kreative Formulierungen
- Übersetzungen

## 📜 Lizenz

GPL-3.0 License - siehe [LICENSE](LICENSE) für Details

## 👤 Autor

Michael Karbacher

---

*Keep the vibes positive! 💚*