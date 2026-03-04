import random

# ============================================================
#  ZENTRALE LOOT-TABELLE
#  Jedes Item hat: name, type, rarity, min_qty, max_qty
#  und optional: attack / armor (für Equipment)
# ============================================================

LOOT_POOL = {
    # ── COMMON ──────────────────────────────────────────────
    "common": [
        {"name": "Healing Potion",    "type": "consumable", "key": "Healing Potions", "min": 1, "max": 1},
        {"name": "Gold",              "type": "gold",        "key": "Gold",            "min": 2, "max": 8},
        {"name": "Altes Seil",        "type": "junk",        "key": "Altes Seil",      "min": 1, "max": 1},
        {"name": "Lumpen",            "type": "junk",        "key": "Lumpen",          "min": 1, "max": 2},
    ],
    # ── UNCOMMON ────────────────────────────────────────────
    "uncommon": [
        {"name": "Großes Heiltrank",  "type": "consumable", "key": "Healing Potions", "min": 2, "max": 3},
        {"name": "Gold",              "type": "gold",        "key": "Gold",            "min": 8, "max": 20},
        {"name": "Kurzschwert",       "type": "weapon",      "key": "Kurzschwert",     "attack": 3, "min": 1, "max": 1},
        {"name": "Lederrüstung",      "type": "chest",       "key": "Lederrüstung",    "armor": 2,  "min": 1, "max": 1},
    ],
    # ── RARE ────────────────────────────────────────────────
    "rare": [
        {"name": "Gold",              "type": "gold",        "key": "Gold",            "min": 20, "max": 50},
        {"name": "Langschwert",       "type": "weapon",      "key": "Langschwert",     "attack": 6, "min": 1, "max": 1},
        {"name": "Kettenhemd",        "type": "chest",       "key": "Kettenhemd",      "armor": 4,  "min": 1, "max": 1},
        {"name": "Elixier",           "type": "consumable",  "key": "Healing Potions", "min": 3, "max": 5},
    ],
    # ── EPIC ────────────────────────────────────────────────
    "epic": [
        {"name": "Gold",              "type": "gold",       "key": "Gold",            "min": 50, "max": 100},
        {"name": "Drachenzahn",       "type": "weapon",     "key": "Drachenzahn",     "attack": 10, "min": 1, "max": 1},
        {"name": "Drachenschuppen",   "type": "chest",      "key": "Drachenschuppen", "armor": 7,  "min": 1, "max": 1},
        {"name": "Phönixfeder",       "type": "consumable", "key": "Healing Potions", "min": 5, "max": 8},
    ],
}

# Wahrscheinlichkeiten je nach Mob-Rang (muss 100 ergeben)
# rank → {rarity: weight}
RANK_LOOT_WEIGHTS = {
    1: {"common": 80, "uncommon": 18, "rare": 2,  "epic": 0},
    2: {"common": 65, "uncommon": 25, "rare": 9,  "epic": 1},
    3: {"common": 45, "uncommon": 30, "rare": 20, "epic": 5},
    4: {"common": 25, "uncommon": 30, "rare": 30, "epic": 15},
    5: {"common": 10, "uncommon": 25, "rare": 35, "epic": 30},
}


def roll_loot(rank: int, rolls: int = 2) -> list[dict]:
    """
    Würfelt `rolls` Mal Loot für einen Mob des gegebenen Rangs.
    Gibt eine Liste von Loot-Dicts zurück.
    """
    weights = RANK_LOOT_WEIGHTS.get(rank, RANK_LOOT_WEIGHTS[1])
    rarities  = list(weights.keys())
    chances   = list(weights.values())

    dropped = []
    for _ in range(rolls):
        rarity = random.choices(rarities, weights=chances, k=1)[0]
        pool   = LOOT_POOL[rarity]
        item   = random.choice(pool)
        dropped.append(item)
    return dropped


def apply_loot(player, loot_list: list[dict]) -> list[str]:
    """
    Wendet eine Liste von Loot-Items auf den Spieler an.
    Gibt eine Liste von Nachrichten zurück.
    """
    messages = []
    for item in loot_list:
        if item["type"] == "gold":
            amount = random.randint(item["min"], item["max"])
            player.inventory["Gold"] = player.inventory.get("Gold", 0) + amount
            messages.append(f"  💰 {amount}x Gold")

        elif item["type"] == "consumable":
            amount = random.randint(item["min"], item["max"])
            player.inventory["Healing Potions"] = player.inventory.get("Healing Potions", 0) + amount
            messages.append(f"  🧪 {amount}x {item['name']}")

        elif item["type"] == "junk":
            amount = random.randint(item["min"], item["max"])
            player.inventory[item["key"]] = player.inventory.get(item["key"], 0) + amount
            messages.append(f"  🗑️  {amount}x {item['name']}")

        elif item["type"] in ("weapon", "chest"):
            equip = {
                "name": item["name"],
                "type": item["type"],
            }
            if item["type"] == "weapon":
                equip["attack"] = item["attack"]
            else:
                equip["armor"] = item["armor"]
            player.inventory["Equipment"].append(equip)
            stat = f"ATK +{item['attack']}" if item["type"] == "weapon" else f"DEF +{item['armor']}"
            messages.append(f"  ✨ {item['name']} ({stat})")

    return messages
