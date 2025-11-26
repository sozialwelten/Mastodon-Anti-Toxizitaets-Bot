#!/usr/bin/env python3
"""
Mastodon Bot gegen toxisches Verhalten
Postet 2-3x pro Woche freundliche Erinnerungen über toxische Social-Media-Praktiken
"""

import csv
import random
import json
from datetime import datetime
from mastodon import Mastodon
import os
from pathlib import Path

# .env Datei laden
def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# Konfiguration
MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE", "https://deine-instanz.social")
ACCESS_TOKEN = os.getenv("MASTODON_TOKEN")
MESSAGES_FILE = "messages.csv"
STATE_FILE = "bot_state.json"

class ToxicityBot:
    def __init__(self):
        """Initialisiert den Bot"""
        self.mastodon = Mastodon(
            access_token=ACCESS_TOKEN,
            api_base_url=MASTODON_INSTANCE
        )
        self.messages = self.load_messages()
        self.state = self.load_state()
    
    def load_messages(self):
        """Lädt alle Nachrichten aus der CSV-Datei"""
        messages = []
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    messages.append(row)
            print(f"✓ {len(messages)} Nachrichten geladen")
        except FileNotFoundError:
            print(f"✗ Fehler: {MESSAGES_FILE} nicht gefunden!")
            print(f"Bitte erstelle die Datei mit den Nachrichten.")
            exit(1)
        return messages
    
    def load_state(self):
        """Lädt den Bot-Status (bereits gepostete IDs)"""
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"posted_ids": []}
    
    def save_state(self):
        """Speichert den Bot-Status"""
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_random_message(self):
        """Wählt eine zufällige, noch nicht gepostete Nachricht"""
        available = [m for m in self.messages 
                    if m['id'] not in self.state['posted_ids']]
        
        # Wenn alle durch, reset
        if not available:
            print("♻️  Alle Nachrichten gepostet, starte von vorne")
            self.state['posted_ids'] = []
            available = self.messages
        
        return random.choice(available)
    
    def post_message(self):
        """Postet eine zufällige Nachricht"""
        msg = self.get_random_message()
        
        try:
            self.mastodon.status_post(
                msg['text'],
                visibility='public'
            )
            self.state['posted_ids'].append(msg['id'])
            self.state['last_post'] = datetime.now().isoformat()
            self.save_state()
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            print(f"✓ [{timestamp}] Gepostet: {msg['category']} (ID: {msg['id']})")
            print(f"  {msg['text'][:80]}...")
        except Exception as e:
            print(f"✗ Fehler beim Posten: {e}")


if __name__ == "__main__":
    import sys
    
    if not ACCESS_TOKEN:
        print("✗ Fehler: MASTODON_TOKEN Umgebungsvariable nicht gesetzt!")
        print("Setze sie mit: export MASTODON_TOKEN='dein-token'")
        exit(1)
    
    bot = ToxicityBot()
    
    # Prüfe ob --dry-run flag gesetzt ist
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        msg = bot.get_random_message()
        print("\n🧪 Dry-Run Modus - würde folgende Nachricht posten:\n")
        print(f"Kategorie: {msg['category']}")
        print(f"ID: {msg['id']}")
        print(f"Text ({len(msg['text'])} Zeichen):\n{msg['text']}")
    else:
        bot.post_message()