import random


# Alle Consumables mit ihren Effekten und Verkaufspreisen
CONSUMABLE_DEFS = {
    "Healing Potion":   {"effect": "heal",    "value": 10, "emoji": "🧪", "desc": "Heilt 10 HP",                  "sell": 7},
    "Großes Heiltrank": {"effect": "heal",    "value": 25, "emoji": "🍶", "desc": "Heilt 25 HP",                  "sell": 17},
    "Elixier":          {"effect": "heal",    "value": 40, "emoji": "✨", "desc": "Heilt 40 HP",                  "sell": 30},
    "Phönixfeder":      {"effect": "cleanse", "value": 15, "emoji": "🪶", "desc": "Heilt 15 HP & entfernt Blutung","sell": 40},
    "Energie-Kristall": {"effect": "energy",  "value": 15, "emoji": "💎", "desc": "Stellt 15 Energie wieder her", "sell": 12},
    "Stärketrank":      {"effect": "attack",  "value": 3,  "emoji": "💪", "desc": "+3 ATK für diesen Kampf",      "sell": 20},
    "Antidot":          {"effect": "cleanse", "value": 0,  "emoji": "🌿", "desc": "Entfernt alle Blutungsstacks", "sell": 5},
}

# Verkaufspreise für Equipment (ca. 50% des Kaufpreises)
EQUIPMENT_SELL_PRICES = {
    "Kurzschwert":    20,
    "Langschwert":    40,
    "Drachenzahn":    80,
    "Lederrüstung":   17,
    "Kettenhemd":     35,
    "Drachenschuppen":70,
}

LOOT_POOL = {
    # -- COMMON
    "common": [
        {"name": "Healing Potion",   "type": "consumable", "key": "Healing Potion",   "min": 1, "max": 1},
        {"name": "Gold",             "type": "gold",        "key": "Gold",             "min": 2, "max": 8},
        {"name": "Altes Seil",       "type": "junk",        "key": "Altes Seil",       "min": 1, "max": 1},
        {"name": "Lumpen",           "type": "junk",        "key": "Lumpen",           "min": 1, "max": 2},
        {"name": "Antidot",          "type": "consumable",  "key": "Antidot",          "min": 1, "max": 1},
    ],
    # -- UNCOMMON
    "uncommon": [
        {"name": "Großes Heiltrank", "type": "consumable",  "key": "Großes Heiltrank", "min": 1, "max": 2},
        {"name": "Gold",             "type": "gold",         "key": "Gold",             "min": 8, "max": 20},
        {"name": "Kurzschwert",      "type": "weapon",       "key": "Kurzschwert",      "attack": 3, "min": 1, "max": 1},
        {"name": "Lederrüstung",     "type": "chest",        "key": "Lederrüstung",     "armor": 2,  "min": 1, "max": 1},
        {"name": "Energie-Kristall", "type": "consumable",   "key": "Energie-Kristall", "min": 1, "max": 1},
        {"name": "Stärketrank",      "type": "consumable",   "key": "Stärketrank",      "min": 1, "max": 1},
    ],
    # -- RARE
    "rare": [
        {"name": "Gold",             "type": "gold",        "key": "Gold",             "min": 20, "max": 50},
        {"name": "Langschwert",      "type": "weapon",      "key": "Langschwert",      "attack": 6, "min": 1, "max": 1},
        {"name": "Kettenhemd",       "type": "chest",       "key": "Kettenhemd",       "armor": 4,  "min": 1, "max": 1},
        {"name": "Elixier",          "type": "consumable",  "key": "Elixier",          "min": 1, "max": 2},
        {"name": "Energie-Kristall", "type": "consumable",  "key": "Energie-Kristall", "min": 2, "max": 3},
    ],
    # -- EPIC
    "epic": [
        {"name": "Gold",             "type": "gold",       "key": "Gold",             "min": 50, "max": 100},
        {"name": "Drachenzahn",      "type": "weapon",     "key": "Drachenzahn",      "attack": 10, "min": 1, "max": 1},
        {"name": "Drachenschuppen",  "type": "chest",      "key": "Drachenschuppen",  "armor": 7,   "min": 1, "max": 1},
        {"name": "Phönixfeder",      "type": "consumable", "key": "Phönixfeder",      "min": 1, "max": 2},
        {"name": "Stärketrank",      "type": "consumable", "key": "Stärketrank",      "min": 2, "max": 3},
    ],
}

RANK_LOOT_WEIGHTS = {
    1: {"common": 80, "uncommon": 18, "rare": 2,  "epic": 0},
    2: {"common": 65, "uncommon": 25, "rare": 9,  "epic": 1},
    3: {"common": 45, "uncommon": 30, "rare": 20, "epic": 5},
    4: {"common": 25, "uncommon": 30, "rare": 30, "epic": 15},
    5: {"common": 10, "uncommon": 25, "rare": 35, "epic": 30},
}


def roll_loot(rank: int, rolls: int = 2) -> list:
    weights  = RANK_LOOT_WEIGHTS.get(rank, RANK_LOOT_WEIGHTS[1])
    rarities = list(weights.keys())
    chances  = list(weights.values())
    dropped  = []
    for _ in range(rolls):
        rarity = random.choices(rarities, weights=chances, k=1)[0]
        pool   = LOOT_POOL[rarity]
        item   = random.choice(pool)
        dropped.append(item)
    return dropped


def apply_loot(player, loot_list: list) -> list:
    from player import MAX_INVENTORY_SLOTS
    messages = []
    for item in loot_list:
        if item["type"] == "gold":
            amount = random.randint(item["min"], item["max"])
            player.inventory["Gold"] = player.inventory.get("Gold", 0) + amount
            messages.append(f"  💰 {amount}x Gold")

        elif item["type"] == "consumable":
            key = item["key"]
            if not player.can_add_consumable(key):
                messages.append(f"  ⚠️  Inventar voll! {item['name']} verloren.")
                continue
            amount = random.randint(item["min"], item["max"])
            if "Consumables" not in player.inventory:
                player.inventory["Consumables"] = {}
            player.inventory["Consumables"][key] = player.inventory["Consumables"].get(key, 0) + amount
            cdef  = CONSUMABLE_DEFS.get(key, {})
            emoji = cdef.get("emoji", "🧪")
            messages.append(f"  {emoji} {amount}x {item['name']}")

        elif item["type"] == "junk":
            amount = random.randint(item["min"], item["max"])
            player.inventory[item["key"]] = player.inventory.get(item["key"], 0) + amount
            messages.append(f"  🗑️  {amount}x {item['name']}")

        elif item["type"] in ("weapon", "chest"):
            if not player.has_inventory_space():
                messages.append(f"  ⚠️  Inventar voll! {item['name']} verloren.")
                continue
            equip = {"name": item["name"], "type": item["type"]}
            if item["type"] == "weapon":
                equip["attack"] = item["attack"]
            else:
                equip["armor"] = item["armor"]
            player.inventory["Equipment"].append(equip)
            stat = f"ATK +{item['attack']}" if item["type"] == "weapon" else f"DEF +{item['armor']}"
            messages.append(f"  ✨ {item['name']} ({stat})")

    return messages
