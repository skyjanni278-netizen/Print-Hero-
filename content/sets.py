# Set-Definitionen und Set-Bonus-Berechnung.
# Importiert WEAPON_VARIANT_TO_BASE aus content/items.py.

from content.items import WEAPON_VARIANT_TO_BASE

SET_DEFS = {
    "Leder-Set": {
        "emoji": "🥋",
        "pieces": {"Kurzschwert", "Lederrüstung", "Lederkappe", "Lederstiefel"},
        "bonuses": {
            2: {"desc": "+2 DEF",                          "atk": 0, "def": 2},
            3: {"desc": "+2 DEF +1 ATK",                   "atk": 1, "def": 2},
            4: {"desc": "+4 DEF +3 ATK — 10% Ausweichen",  "atk": 3, "def": 4, "special": "leder_dodge"},
        },
    },
    "Eisen-Set": {
        "emoji": "⛓️",
        "pieces": {"Langschwert", "Kettenhemd", "Eisenhelm", "Eisenstiefel"},
        "bonuses": {
            2: {"desc": "+3 DEF",                              "atk": 0, "def": 3},
            3: {"desc": "+3 DEF +2 ATK",                       "atk": 2, "def": 3},
            4: {"desc": "+6 DEF +4 ATK — +3 Energie/Runde",    "atk": 4, "def": 6, "special": "eisen_energy_regen"},
        },
    },
    "Stahl-Set": {
        "emoji": "🔩",
        "pieces": {"Kriegshammer", "Plattenpanzer", "Stahlhelm", "Schnellläuferstiefel"},
        "bonuses": {
            2: {"desc": "+4 DEF",                             "atk": 0, "def": 4},
            3: {"desc": "+4 DEF +3 ATK",                      "atk": 3, "def": 4},
            4: {"desc": "+8 DEF +6 ATK — Blutungsimmunität",  "atk": 6, "def": 8, "special": "stahl_bleed_immune"},
        },
    },
    "Schatten-Set": {
        "emoji": "🌑",
        "pieces": {"Schattendolch", "Schattenrüstung", "Schattenhelm", "Schattenstiefel"},
        "bonuses": {
            2: {"desc": "+4 DEF",                           "atk": 0, "def": 4},
            3: {"desc": "+4 DEF +4 ATK",                    "atk": 4, "def": 4},
            4: {"desc": "+8 DEF +8 ATK — +15% Krit-Chance", "atk": 8, "def": 8, "special": "schatten_crit"},
        },
    },
    "Runen-Set": {
        "emoji": "🌀",
        "pieces": {"Runenschwert", "Runenrüstung", "Runenhelm", "Runenstiefel"},
        "bonuses": {
            2: {"desc": "+6 DEF",                    "atk": 0, "def": 6},
            3: {"desc": "+6 DEF +4 ATK",             "atk": 4, "def": 6},
            4: {"desc": "+12 DEF +8 ATK — +20% XP",  "atk": 8, "def": 12, "special": "runen_xp_bonus"},
        },
    },
    "Drachen-Set": {
        "emoji": "🐉",
        "pieces": {"Drachenzahn", "Drachenschuppen", "Drachenkrone", "Drachenklauen"},
        "bonuses": {
            2: {"desc": "+8 DEF",                                       "atk": 0,  "def": 8},
            3: {"desc": "+8 DEF +6 ATK",                                "atk": 6,  "def": 8},
            4: {"desc": "+15 DEF +12 ATK — 15% Angriff vollst. blocken","atk": 12, "def": 15, "special": "drachen_block"},
        },
    },
    "Licht-Set": {
        "emoji": "✨",
        "pieces": {"Göttliche Klinge", "Rüstung des Lichts", "Krone des Ewigen", "Stiefel der Ewigkeit"},
        "bonuses": {
            2: {"desc": "+12 DEF",                       "atk": 0,  "def": 12},
            3: {"desc": "+12 DEF +10 ATK",               "atk": 10, "def": 12},
            4: {"desc": "+20 DEF +18 ATK — +3 HP/Runde", "atk": 18, "def": 20, "special": "licht_hp_regen"},
        },
    },
    "Runen-Panzer": {
        "emoji": "🛡️",
        "pieces": {"Panzerklinge", "Runen-Platte", "Runen-Visier", "Runen-Schritte"},
        "bonuses": {
            2: {"desc": "+3 DEF",                                   "atk": 0, "def": 3},
            3: {"desc": "+5 DEF +2 ATK",                            "atk": 2, "def": 5},
            4: {"desc": "+8 DEF +5 ATK — Blutungsschaden −1/Stack", "atk": 5, "def": 8, "special": "panzer_bleed_reduce"},
        },
    },
    "Schattentuch": {
        "emoji": "🌙",
        "pieces": {"Mondklinge", "Schattengewand", "Schattenkapuze", "Schattensandale"},
        "bonuses": {
            2: {"desc": "+1 DEF",                          "atk": 0, "def":  1},
            3: {"desc": "+2 DEF +2 ATK",                   "atk": 2, "def":  2},
            4: {"desc": "−3 DEF +2 ATK — 15% Ausweichen",  "atk": 2, "def": -3, "special": "schattentuch_dodge"},
        },
    },
    "Drachenschuppen": {
        "emoji": "🐉",
        "pieces": {"Schuppenklinge", "Schuppenpanzer", "Schuppenhelm", "Schuppenstiefel"},
        "bonuses": {
            2: {"desc": "+6 DEF",                                         "atk": 0, "def":  6},
            3: {"desc": "+9 DEF +4 ATK",                                  "atk": 4, "def":  9},
            4: {"desc": "+12 DEF +8 ATK — 20% Angriff vollst. blocken",   "atk": 8, "def": 12, "special": "schuppen_block"},
        },
    },
    "Verdammten-Stahl": {
        "emoji": "💀",
        "pieces": {"Verdammte Klinge", "Verdammte Rüstung", "Verdammter Helm", "Verdammte Stiefel"},
        "bonuses": {
            2: {"desc": "+2 ATK",        "atk":  2, "def":  0},
            3: {"desc": "+4 ATK −2 DEF", "atk":  4, "def": -2},
            4: {"desc": "+6 ATK −4 DEF", "atk":  6, "def": -4},
        },
    },
    "Eisenfestung": {
        "emoji": "🏰",
        "pieces": {"Festungsklinge", "Festungsplatte", "Festungshelm", "Festungsstiefel"},
        "bonuses": {
            2: {"desc": "+3 DEF",                         "atk": 0, "def": 3},
            3: {"desc": "+3 DEF +2 ATK",                  "atk": 2, "def": 3},
            4: {"desc": "+10 DEF +5 ATK — Schildwall ×2", "atk": 5, "def": 10, "special": "warrior_2block"},
        },
    },
    "Schattenhülle": {
        "emoji": "🌙",
        "pieces": {"Hüllendolch", "Hüllenpanzer", "Hüllenmaske", "Hüllenstiefel"},
        "bonuses": {
            2: {"desc": "+3 DEF",                                              "atk": 0, "def": 3},
            3: {"desc": "+5 DEF +4 ATK",                                       "atk": 4, "def": 5},
            4: {"desc": "+8 DEF +5 ATK — Aus dem Schatten: +15% Krit-Chance",  "atk": 5, "def": 8, "special": "rogue_shadow_regen"},
        },
    },
    "Totenritter": {
        "emoji": "⚰️",
        "pieces": {"Totenklinge", "Totenrüstung", "Totenschädel", "Totenstiefel"},
        "bonuses": {
            2: {"desc": "+5 DEF",                                                    "atk": 0, "def":  5},
            3: {"desc": "+8 DEF +5 ATK",                                             "atk": 5, "def":  8},
            4: {"desc": "+10 DEF +8 ATK — Bei ≤25% HP: +50% ATK, +20% Ausweichen",   "atk": 8, "def": 10, "special": "totenritter_berserker"},
        },
    },
    "Abyssal-Set": {
        "emoji": "🕳️",
        "pieces": {"Abyssalklinge", "Abyssalrobe", "Abyssalhelm", "Abyssalsohlen"},
        "bonuses": {
            2: {"desc": "+10 DEF",                                                       "atk": 0,  "def": 10},
            3: {"desc": "+14 DEF +8 ATK",                                                "atk": 8,  "def": 14},
            4: {"desc": "+16 DEF +12 ATK — 30% des erlittenen Schadens als Rückstoß",    "atk": 12, "def": 16, "special": "abyssal_thorns"},
        },
    },
    "Arkane Roben": {
        "emoji": "🔮",
        "pieces": {"Arkaner Stab", "Arkane Robe", "Arkane Kapuze", "Arkane Schuhe"},
        "bonuses": {
            2: {"desc": "+5 max Energie",                         "atk": 0, "def": 0, "energy":  5},
            3: {"desc": "+10 max Energie +2 ATK",                 "atk": 2, "def": 0, "energy": 10},
            4: {"desc": "+8 DEF +4 ATK +20 Energie — Arkane ×2", "atk": 4, "def": 8, "energy": 20, "special": "mage_double_arcane"},
        },
    },
}


def get_active_sets(player) -> list:
    equipped = {WEAPON_VARIANT_TO_BASE.get(item["name"], item["name"]) for item in player.equipment.values()}
    result = []
    for sname, sdef in SET_DEFS.items():
        count = len(equipped & sdef["pieces"])
        bonus = sdef["bonuses"].get(count)
        if bonus:
            result.append((sname, sdef, count, bonus))
    return result


def get_set_specials(player) -> set:
    return {b["special"] for _, _, count, b in get_active_sets(player) if count == 4 and "special" in b}
