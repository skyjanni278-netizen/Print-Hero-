import json
import os
from player import Character

SAVE_FILE = "savegame.json"

def save_game(player):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "min_attack": player.min_attack,
        "armor": player.armor,
        "level": player.level,
        "xp": player.xp,
        "xp_to_level_up": player.xp_to_level_up,
        "energy": player.energy,
        "max_energy": player.max_energy,
        "inventory": player.inventory,
        "equipment": player.equipment,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("💾 Spielstand gespeichert!")

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
    player = Character(data["name"], data["max_hp"], data["attack"])
    player.hp           = data["hp"]
    player.min_attack   = data["min_attack"]
    player.armor        = data["armor"]
    player.level        = data["level"]
    player.xp           = data["xp"]
    player.xp_to_level_up = data["xp_to_level_up"]
    player.energy       = data["energy"]
    player.max_energy   = data["max_energy"]
    player.equipment    = data["equipment"]
    # Migration: fehlender head-Slot in alten Saves
    if "head" not in player.equipment:
        player.equipment["head"] = {"name": "Kein Helm", "armor": 0}

    inv = data["inventory"]

    # Migration: altes "Healing Potions" -> neues Format
    if "Consumables" not in inv:
        old = inv.pop("Healing Potions", 0)
        inv["Consumables"] = {"Healing Potion": old} if old > 0 else {}

    # Migration: altes loses Junk (Altes Seil / Lumpen direkt im inv) -> Junk-Dict
    if "Junk" not in inv:
        inv["Junk"] = {}
    for junk_key in ("Altes Seil", "Lumpen", "Knochen", "Schleimklumpen", "Goblinzahn"):
        if junk_key in inv:
            inv["Junk"][junk_key] = inv["Junk"].get(junk_key, 0) + inv.pop(junk_key)

    player.inventory = inv
    print("📂 Spielstand geladen!")
    return player

def save_exists():
    return os.path.exists(SAVE_FILE)
