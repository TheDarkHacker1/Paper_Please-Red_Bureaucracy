"""
PAPERS, PLEASE — TERMINAL REMAKE (Python Terminal Version)
Single-file, deeply immersive bureaucracy simulation
"""

import sys
import os
import time
import json
import random
import argparse
from datetime import datetime, timedelta
from termcolor import colored
import pycountry
from faker import Faker

# Optional AI imports (high-end mode)
try:
    from transformers import pipeline
    import torch
    AI_ENABLED = True
except ImportError:
    AI_ENABLED = False

# Game constants
GAME_TITLE = "PAPERS, PLEASE — TERMINAL REMAKE"
MINISTRY_NAME = "Ministry of Bureaucratic Affairs"
START_DATE = datetime(2000, 1, 1, 6, 0)
END_DATE = datetime(2025, 1, 1, 20, 0)
WORK_START = 6
WORK_END = 20

# Command-line flags
parser = argparse.ArgumentParser(description=GAME_TITLE)
parser.add_argument('--lowend', action='store_true', help='Disable AI and animations')
parser.add_argument('--skipboot', action='store_true', help='Skip boot sequence')
parser.add_argument('--debug', action='store_true', help='Enable verbose debug logs')
parser.add_argument('--lang', type=str, default='en', choices=['en', 'jp', 'ru', 'vn'], help='Language toggle')
args = parser.parse_args()

# Faker for city names
fake = Faker()

# Sound FX (textual)
def sfx(text):
    print(colored(f"[{text}]", "cyan"), end=' ', flush=True)
    time.sleep(0.2)

def typewriter(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Boot sequence
def boot_sequence():
    sfx('BOOT')
    typewriter(f"{MINISTRY_NAME} BIOS v2.5 Initializing...")
    sfx('CLUNK')
    typewriter("Loading security modules...")
    sfx('BEEP')
    typewriter("Verifying Ministry credentials...")
    sfx('CLUNK')
    typewriter("System integrity: OK")
    sfx('BEEP')
    typewriter("Welcome, Inspector.")
    time.sleep(0.5)

# Main menu
def main_menu():
    print(colored(f"\n=== {GAME_TITLE} ===", "green"))
    print("1. Start New Game")
    print("2. Load Game")
    print("3. Config")
    print("4. Credits")
    print("5. Exit")
    choice = input("Select option: ").strip()
    return choice

# Country and city data
def get_countries_and_cities():
    countries = list(pycountry.countries)
    country_data = {}
    for country in countries:
        cities = [fake.city() for _ in range(4)]
        country_data[country.name] = cities
    return country_data

# Save system (simple XOR obfuscation)
def xor_encrypt(data, key='ministry'):  # Not secure, just obfuscation
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def save_game(slot, state):
    data = json.dumps(state)
    obfuscated = xor_encrypt(data)
    with open(f'save_slot_{slot}.sav', 'w', encoding='utf-8') as f:
        f.write(obfuscated)

def load_game(slot):
    try:
        with open(f'save_slot_{slot}.sav', 'r', encoding='utf-8') as f:
            obfuscated = f.read()
        data = xor_encrypt(obfuscated)
        return json.loads(data)
    except Exception:
        return None

# Context-sensitive help/manual
def show_help(context=None):
    print(colored("\n=== Ministry Manual ===", "yellow"))
    if context == 'document':
        print("- scan passport: Inspect passport details")
        print("- inspect seal: Check for forgery")
        print("- compare photo: Match photo to entrant")
        print("- check expiry: Validate document date")
        print("- cross-check name: Compare names across docs")
        print("- audit fingerprint: Check biometric data")
        print("- body scan: (Unlocked Day 90)")
    else:
        print("- Type commands to inspect documents and interview NPCs.")
        print("- Type 'help' anytime for tips.")

# End-of-day report
def end_of_day_report(state):
    print(colored("\n=== End of Day Report ===", "magenta"))
    print(f"Date: {state['date'].strftime('%Y-%m-%d')}")
    print(f"Earnings: ${state['money']}")
    print(f"Mistakes: {state['mistakes']}")
    print(f"Faction Influence: {state['faction']}")
    print(f"Family Status: {state['family']}")
    print(f"Ministry Approval: {state['approval']}%")
    print(f"XP: {state['xp']}")
    print(f"Stress: {state['stress']}")

# Main game loop (stub)
def game_loop(state, country_data):
    current_time = state['date']
    while current_time.hour < WORK_END:
        # HUD
        hud = f"Time: {current_time.strftime('%H:%M')} | XP: {state['xp']} | Stress: {state['stress']} | Approval: {state['approval']}% | Money: ${state['money']}"
        print(colored(hud, "blue"))
        # Entrant generation
        entrant = generate_entrant(country_data)
        print(colored(f"\nEntrant from {entrant['country']} ({entrant['city']})", "white"))
        print(f"Documents: {', '.join(entrant['documents'])}")
        print(f"Personality: {entrant['personality']}")
        print(f"Mood: {entrant['mood']}")
        # Command prompt
        cmd = input(colored("\n> ", "green")).strip().lower()
        if cmd == 'help':
            show_help('document')
        elif cmd == 'exit':
            break
        else:
            # Document inspection stub
            print(colored("[Inspection not yet implemented]", "red"))
        # Advance time
        current_time += timedelta(minutes=random.randint(10, 30))
        state['date'] = current_time
    end_of_day_report(state)

# Entrant generation (stub)
def generate_entrant(country_data):
    country = random.choice(list(country_data.keys()))
    city = random.choice(country_data[country])
    documents = random.sample([
        'Passport', 'Entry Permit', 'Work Pass', 'Diplomatic Papers',
        'Refugee Documents', 'Biometric Card', 'Body Scan Report', 'Fingerprint Record'
    ], k=random.randint(2, 4))
    personality = random.choice([
        'INTJ (Strategist)', 'ESFP (Performer)', 'INFJ (Advocate)', 'ESTP (Entrepreneur)',
        'Anxious', 'Manipulative', 'Warm', 'Deceptive', 'Nervous', 'Cunning', 'Angry', 'Calm'
    ])
    mood = random.choice([':|', '>:[' , '^_^', 'ಠ_ಠ'])
    return {
        'country': country,
        'city': city,
        'documents': documents,
        'personality': personality,
        'mood': mood
    }

# Initial game state
def initial_state():
    return {
        'date': START_DATE,
        'money': 30,
        'mistakes': 0,
        'faction': 'Neutral',
        'family': 'Stable',
        'approval': 50,
        'xp': 0,
        'stress': 10
    }

# Main entry point
def main():
    if not args.skipboot:
        boot_sequence()
    country_data = get_countries_and_cities()
    while True:
        choice = main_menu()
        if choice == '1':
            state = initial_state()
            game_loop(state, country_data)
        elif choice == '2':
            slot = input("Enter save slot number: ").strip()
            state = load_game(slot)
            if state:
                game_loop(state, country_data)
            else:
                print(colored("No save found.", "red"))
        elif choice == '3':
            print(colored("Config not yet implemented.", "yellow"))
        elif choice == '4':
            print(colored("Created by The Ministry. Inspired by Papers, Please.", "cyan"))
        elif choice == '5':
            print(colored("Exiting. Glory to the Ministry.", "red"))
            break
        else:
            print(colored("Invalid option.", "red"))

if __name__ == '__main__':
    main()
