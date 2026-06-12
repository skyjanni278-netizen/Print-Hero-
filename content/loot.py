import random

# Loot-Pools, Würfel-Funktionen und Loot-Vergabe.
# Importiert Item-Definitionen aus content/items.py.

from content.items import (
    CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_DEFS,
    CLASS_WEAPON_MAP, RARITY_LABEL,
)

# ── Rang-basierter Loot-Pool ──────────────────────────────────────────────────

LOOT_POOL = {
    "common": [
        {"name": "Healing Potion", "type": "consumable", "key": "Healing Potion", "min": 1, "max": 1},
        {"name": "Gold",           "type": "gold",        "key": "Gold",           "min": 3, "max": 10},
        {"name": "Altes Seil",     "type": "junk",        "key": "Altes Seil",     "min": 1, "max": 2},
        {"name": "Lumpen",         "type": "junk",        "key": "Lumpen",         "min": 1, "max": 3},
        {"name": "Antidot",        "type": "consumable",  "key": "Antidot",        "min": 1, "max": 1},
        {"name": "Knochen",        "type": "junk",        "key": "Knochen",        "min": 1, "max": 2},
        {"name": "Lederkappe",     "type": "equipment",   "key": "Lederkappe"},
        {"name": "Kurzschwert",    "type": "equipment",   "key": "Kurzschwert"},
        {"name": "Lederrüstung",   "type": "equipment",   "key": "Lederrüstung"},
        {"name": "Lederstiefel",   "type": "equipment",   "key": "Lederstiefel"},
        {"name": "Eisenstiefel",   "type": "equipment",   "key": "Eisenstiefel"},
    ],
    "uncommon": [
        {"name": "Großes Heiltrank",    "type": "consumable",  "key": "Großes Heiltrank",    "min": 1, "max": 1},
        {"name": "Gold",                "type": "gold",         "key": "Gold",                "min": 10, "max": 25},
        {"name": "Energie-Kristall",    "type": "consumable",   "key": "Energie-Kristall",    "min": 1, "max": 1},
        {"name": "Stärketrank",         "type": "consumable",   "key": "Stärketrank",         "min": 1, "max": 1},
        {"name": "Schleimklumpen",      "type": "junk",         "key": "Schleimklumpen",      "min": 1, "max": 2},
        {"name": "Goblinzahn",          "type": "junk",         "key": "Goblinzahn",          "min": 1, "max": 2},
        {"name": "Wolfspelz",           "type": "junk",         "key": "Wolfspelz",           "min": 1, "max": 2},
        {"name": "Trollfell",           "type": "junk",         "key": "Trollfell",           "min": 1, "max": 1},
        {"name": "Banditen-Abzeichen",  "type": "junk",         "key": "Banditen-Abzeichen",  "min": 1, "max": 1},
        {"name": "Eisenhelm",           "type": "equipment", "key": "Eisenhelm"},
        {"name": "Langschwert",         "type": "equipment", "key": "Langschwert"},
        {"name": "Kriegshammer",        "type": "equipment", "key": "Kriegshammer"},
        {"name": "Kettenhemd",          "type": "equipment", "key": "Kettenhemd"},
        {"name": "Plattenpanzer",       "type": "equipment", "key": "Plattenpanzer"},
        {"name": "Schnellläuferstiefel","type": "equipment", "key": "Schnellläuferstiefel"},
        {"name": "Schattendolch",       "type": "equipment", "key": "Schattendolch"},
        {"name": "Schattenstiefel",     "type": "equipment", "key": "Schattenstiefel"},
        {"name": "Kriegsstiefel",       "type": "equipment", "key": "Kriegsstiefel"},
    ],
    "rare": [
        {"name": "Gold",             "type": "gold",        "key": "Gold",             "min": 25, "max": 60},
        {"name": "Elixier",          "type": "consumable",  "key": "Elixier",          "min": 1, "max": 1},
        {"name": "Energie-Kristall", "type": "consumable",  "key": "Energie-Kristall", "min": 1, "max": 2},
        {"name": "Stahlhelm",        "type": "equipment", "key": "Stahlhelm"},
        {"name": "Runenschwert",     "type": "equipment", "key": "Runenschwert"},
        {"name": "Runenrüstung",     "type": "equipment", "key": "Runenrüstung"},
        {"name": "Runenhelm",        "type": "equipment", "key": "Runenhelm"},
        {"name": "Runenstiefel",     "type": "equipment", "key": "Runenstiefel"},
        {"name": "Sturmklinge",      "type": "equipment", "key": "Sturmklinge"},
        {"name": "Schattenrüstung",  "type": "equipment", "key": "Schattenrüstung"},
        {"name": "Schattenhelm",     "type": "equipment", "key": "Schattenhelm"},
    ],
    "epic": [
        {"name": "Gold",            "type": "gold",       "key": "Gold",            "min": 60, "max": 120},
        {"name": "Phönixfeder",     "type": "consumable", "key": "Phönixfeder",     "min": 1, "max": 1},
        {"name": "Stärketrank",     "type": "consumable", "key": "Stärketrank",     "min": 1, "max": 2},
        {"name": "Drachenzahn",     "type": "equipment", "key": "Drachenzahn"},
        {"name": "Drachenschuppen", "type": "equipment", "key": "Drachenschuppen"},
        {"name": "Drachenkrone",    "type": "equipment", "key": "Drachenkrone"},
        {"name": "Drachenklauen",   "type": "equipment", "key": "Drachenklauen"},
        {"name": "Knochensense",    "type": "equipment", "key": "Knochensense"},
        # Klassen-Sets (Filter in apply_loot — nur für passende Klasse)
        {"name": "Festungsklinge",  "type": "equipment", "key": "Festungsklinge"},
        {"name": "Festungsplatte",  "type": "equipment", "key": "Festungsplatte"},
        {"name": "Festungshelm",    "type": "equipment", "key": "Festungshelm"},
        {"name": "Festungsstiefel", "type": "equipment", "key": "Festungsstiefel"},
        {"name": "Hüllendolch",     "type": "equipment", "key": "Hüllendolch"},
        {"name": "Hüllenpanzer",    "type": "equipment", "key": "Hüllenpanzer"},
        {"name": "Hüllenmaske",     "type": "equipment", "key": "Hüllenmaske"},
        {"name": "Hüllenstiefel",   "type": "equipment", "key": "Hüllenstiefel"},
        {"name": "Arkaner Stab",    "type": "equipment", "key": "Arkaner Stab"},
        {"name": "Arkane Robe",     "type": "equipment", "key": "Arkane Robe"},
        {"name": "Arkane Kapuze",   "type": "equipment", "key": "Arkane Kapuze"},
        {"name": "Arkane Schuhe",   "type": "equipment", "key": "Arkane Schuhe"},
    ],
    "legendary": [
        {"name": "Gold",                 "type": "gold",      "key": "Gold",                 "min": 150, "max": 300},
        {"name": "Göttliche Klinge",     "type": "equipment", "key": "Göttliche Klinge"},
        {"name": "Rüstung des Lichts",   "type": "equipment", "key": "Rüstung des Lichts"},
        {"name": "Krone des Ewigen",     "type": "equipment", "key": "Krone des Ewigen"},
        {"name": "Stiefel der Ewigkeit", "type": "equipment", "key": "Stiefel der Ewigkeit"},
    ],
}

RANK_LOOT_WEIGHTS = {
    1: {"common": 80, "uncommon": 18, "rare": 2,   "epic": 0,  "legendary": 0},
    2: {"common": 65, "uncommon": 28, "rare": 7,   "epic": 0,  "legendary": 0},
    3: {"common": 48, "uncommon": 35, "rare": 15,  "epic": 2,  "legendary": 0},
    4: {"common": 25, "uncommon": 33, "rare": 33,  "epic": 9,  "legendary": 0},
    5: {"common": 8,  "uncommon": 17, "rare": 33,  "epic": 33, "legendary": 9},
}

# ── Zonen-basierte Loot-Pools ─────────────────────────────────────────────────

def _e(key, w):              return {"type": "equipment",  "key": key, "weight": w}
def _c(key, w, mn=1, mx=1): return {"type": "consumable", "key": key, "weight": w, "min": mn, "max": mx}
def _j(key, w, mn=1, mx=2): return {"type": "junk",       "key": key, "weight": w, "min": mn, "max": mx}
def _g(w, mn, mx):           return {"type": "gold",        "key": "Gold", "weight": w, "min": mn, "max": mx}

ZONE_LOOT_POOL = {
    "wald": [
        _g(22,  3, 12),
        _c("Healing Potion",   18),
        _c("Antidot",           8),
        _c("Energie-Kristall",  6),
        _j("Altes Seil",       10, 1, 2),
        _j("Lumpen",            8, 1, 2),
        _j("Knochen",           7, 1, 2),
        _j("Schleimklumpen",    6, 1, 2),
        _j("Wolfspelz",         4, 1, 1),
        _e("Kurzschwert",       7),
        _e("Lederrüstung",      6),
        _e("Lederkappe",        6),
        _e("Lederstiefel",      6),
        _e("Eisenstiefel",      4),
        _e("Eisenhelm",         4),
        _e("Kettenhemd",        3),
        _e("Giftklaue",         2),
    ],
    "ruinen": [
        _g(20, 10, 28),
        _c("Großes Heiltrank", 16),
        _c("Energie-Kristall",  8),
        _c("Stärketrank",       6),
        _c("Antidot",           5),
        _j("Wolfspelz",         8, 1, 2),
        _j("Trollfell",         6, 1, 1),
        _j("Goblinzahn",        5, 1, 2),
        _j("Banditen-Abzeichen",4, 1, 1),
        _e("Kriegshammer",      6),
        _e("Plattenpanzer",     5),
        _e("Stahlhelm",         5),
        _e("Schnellläuferstiefel", 4),
        _e("Schattendolch",     4),
        _e("Schattenstiefel",   3),
        _e("Eisaxt",            2),
        _e("Runen-Kriegshammer",1),
        _e("Panzerklinge",      2),
        _e("Runen-Platte",      2),
        _e("Runen-Visier",      1),
        _e("Runen-Schritte",    1),
    ],
    "wueste": [
        _g(18, 20, 48),
        _c("Elixier",          12),
        _c("Energie-Kristall",  8),
        _c("Stärketrank",       7),
        _j("Goblinzahn",        5, 1, 2),
        _j("Trollfell",         4, 1, 1),
        _j("Banditen-Abzeichen",4, 1, 1),
        _e("Runenschwert",      6),
        _e("Runenrüstung",      5),
        _e("Runenhelm",         5),
        _e("Runenstiefel",      4),
        _e("Schattenrüstung",   4),
        _e("Schattenhelm",      3),
        _e("Mondklinge",        4),
        _e("Schattengewand",    4),
        _e("Schattenkapuze",    3),
        _e("Schattensandale",   3),
        _e("Flammenklinge",     3),
        _e("Festungsklinge",    1),
        _e("Festungsstiefel",   1),
        _e("Hüllendolch",       1),
        _e("Hüllenstiefel",     1),
        _e("Arkaner Stab",      1),
        _e("Arkane Schuhe",     1),
    ],
    "vulkan": [
        _g(16, 40, 80),
        _c("Elixier",          10),
        _c("Phönixfeder",       7),
        _c("Stärketrank",       5),
        _e("Drachenzahn",       6),
        _e("Drachenschuppen",   5),
        _e("Drachenkrone",      5),
        _e("Drachenklauen",     4),
        _e("Knochensense",      4),
        _e("Schuppenklinge",    4),
        _e("Schuppenpanzer",    4),
        _e("Schuppenhelm",      3),
        _e("Schuppenstiefel",   3),
        _e("Festungsplatte",    2),
        _e("Festungshelm",      2),
        _e("Hüllenpanzer",      2),
        _e("Hüllenmaske",       2),
        _e("Arkane Robe",       2),
        _e("Arkane Kapuze",     2),
        _e("Totenklinge",       3),
        _e("Totenrüstung",      3),
        _e("Totenschädel",      2),
        _e("Totenstiefel",      2),
        _e("Göttliche Klinge",  1),
        _e("Rüstung des Lichts",1),
        _e("Krone des Ewigen",  1),
        _e("Stiefel der Ewigkeit", 1),
    ],
    "dunkelreich": [
        _g(14, 80, 150),
        _c("Elixier",           9),
        _c("Phönixfeder",       7),
        _e("Verdammte Klinge",  3),
        _e("Verdammte Rüstung", 3),
        _e("Verdammter Helm",   2),
        _e("Verdammte Stiefel", 2),
        _e("Totenklinge",       2),
        _e("Totenrüstung",      2),
        _e("Totenschädel",      2),
        _e("Totenstiefel",      2),
        _e("Göttliche Klinge",  3),
        _e("Rüstung des Lichts",3),
        _e("Krone des Ewigen",  3),
        _e("Stiefel der Ewigkeit", 3),
        _e("Abyssalklinge",     2),
        _e("Abyssalrobe",       2),
        _e("Abyssalhelm",       2),
        _e("Abyssalsohlen",     2),
        _e("Götterspeer",       1),
        _e("Seelenpanzer",      1),
        _e("Krone der Götter",  1),
    ],
}

# Boss-Loot: garantierte Set-Teile des nächsten Tiers
BOSS_LOOT_POOL = {
    "wald":        ["Kriegshammer", "Plattenpanzer", "Stahlhelm", "Schnellläuferstiefel",
                    "Panzerklinge", "Runen-Platte", "Runen-Visier", "Runen-Schritte"],
    "ruinen":      ["Runenschwert", "Runenrüstung", "Runenhelm", "Runenstiefel",
                    "Mondklinge", "Schattengewand", "Schattenkapuze", "Schattensandale"],
    "wueste":      ["Drachenzahn", "Drachenschuppen", "Drachenkrone", "Drachenklauen",
                    "Schuppenklinge", "Schuppenpanzer", "Schuppenhelm", "Schuppenstiefel"],
    "vulkan":      ["Verdammte Klinge", "Verdammte Rüstung", "Verdammter Helm", "Verdammte Stiefel",
                    "Totenklinge", "Totenrüstung", "Totenschädel", "Totenstiefel"],
    "dunkelreich": ["Göttliche Klinge", "Rüstung des Lichts", "Krone des Ewigen", "Stiefel der Ewigkeit",
                    "Abyssalklinge", "Abyssalrobe", "Abyssalhelm", "Abyssalsohlen"],
}

# ── Würfel-Funktionen ─────────────────────────────────────────────────────────

def roll_zone_loot(zone_id: str, rolls: int = 2) -> list:
    pool    = ZONE_LOOT_POOL.get(zone_id, ZONE_LOOT_POOL["wald"])
    weights = [p["weight"] for p in pool]
    return [random.choices(pool, weights=weights, k=1)[0] for _ in range(rolls)]


def roll_boss_loot(zone_id: str) -> list:
    pool  = BOSS_LOOT_POOL.get(zone_id, [])
    picks = random.sample(pool, min(2, len(pool))) if pool else []
    result = [{"type": "equipment", "key": k} for k in picks]
    gold_ranges = {
        "wald": (30, 60), "ruinen": (50, 90), "wueste": (70, 120),
        "vulkan": (100, 160), "dunkelreich": (150, 250),
    }
    mn, mx = gold_ranges.get(zone_id, (40, 80))
    result.append({"type": "gold", "key": "Gold", "min": mn, "max": mx})
    return result


def roll_loot(rank: int = 1, rolls: int = 2) -> list:
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
    messages = []

    for item in loot_list:
        if item["type"] == "gold":
            amount = random.randint(item["min"], item["max"])
            if "goldgier" in getattr(player, "active_segnungen", []):
                amount = int(amount * 1.25)
            if getattr(player, "spiegel", {}).get("glueck") == "A":
                amount = int(amount * 1.15)
            player.inventory["Gold"] = player.inventory.get("Gold", 0) + amount
            messages.append(f"  💰 {amount}x Gold")

        elif item["type"] == "consumable":
            key    = item["key"]
            label  = item.get("name", key)
            amount = random.randint(item.get("min", 1), item.get("max", 1))
            result = player.add_consumable(key, amount)
            emoji  = CONSUMABLE_DEFS.get(key, {}).get("emoji", "🧪")
            if result > 0:
                messages.append(f"  {emoji} {result}x {label}")
            if result < amount:
                messages.append(f"  ⚠️  {amount - result}x {label} nicht aufgenommen (Stapel voll / Inventar voll)")

        elif item["type"] == "junk":
            key    = item["key"]
            label  = item.get("name", key)
            amount = random.randint(item.get("min", 1), item.get("max", 1))
            result = player.add_junk(key, amount)
            emoji  = JUNK_DEFS.get(key, {}).get("emoji", "🗑️")  # noqa: RUF001
            if result > 0:
                messages.append(f"  {emoji} {result}x {label}")
            if result < amount:
                messages.append(f"  ⚠️  {amount - result}x {label} nicht aufgenommen (Inventar voll)")

        elif item["type"] == "equipment":
            if not player.has_inventory_space():
                messages.append(f"  ⚠️  Inventar voll! {item.get('name', item.get('key', '?'))} verloren.")
                continue
            item_key   = item["key"]
            raw_edef   = EQUIPMENT_DEFS.get(item_key, {})
            class_only = raw_edef.get("class_only")
            if class_only and class_only != getattr(player, "player_class", "warrior"):
                continue
            if raw_edef.get("slot") == "weapon":
                player_class = getattr(player, "player_class", "warrior")
                variant = CLASS_WEAPON_MAP.get(item_key, {}).get(player_class)
                if variant and variant in EQUIPMENT_DEFS:
                    item_key = variant
            edef   = EQUIPMENT_DEFS.get(item_key, {})
            slot   = edef.get("slot", "weapon")
            emoji  = edef.get("emoji", "⚔️")
            rarity = edef.get("rarity", "common")
            rlabel, rbadge = RARITY_LABEL.get(rarity, ("?", "⬜"))

            equip = {"name": item_key, "type": slot}
            if slot == "weapon":
                equip["attack"] = edef["attack"]
                stat = f"ATK +{edef['attack']}"
            else:
                equip["armor"] = edef["armor"]
                stat = f"DEF +{edef['armor']}"

            player.inventory["Equipment"].append(equip)
            messages.append(f"  {rbadge}{emoji} {item_key} [{rlabel}] ({stat})")
            if rarity in ("legendary", "mythic"):
                from systems.achievements import check_and_unlock
                msg = check_and_unlock(player, "got_legendary")
                if msg:
                    messages.append(f"  {msg}")
                if rarity == "mythic":
                    msg = check_and_unlock(player, "got_mythic")
                    if msg:
                        messages.append(f"  {msg}")

    return messages
