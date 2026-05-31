# Item-Definitionen: Consumables, Junk, Equipment, Klassen-Mapping, Rezepte.
# Wird von content/sets.py, content/loot.py und allen anderen Modulen importiert.

CONSUMABLE_DEFS = {
    "Healing Potion":   {"effect": "heal",    "value": 10, "emoji": "🧪", "desc": "Heilt 10 HP",                   "max_stack": 5,  "sell": 7},
    "Großes Heiltrank": {"effect": "heal",    "value": 25, "emoji": "🍶", "desc": "Heilt 25 HP",                   "max_stack": 5,  "sell": 17},
    "Elixier":          {"effect": "heal",    "value": 40, "emoji": "✨", "desc": "Heilt 40 HP",                   "max_stack": 3,  "sell": 30},
    "Phönixfeder":      {"effect": "cleanse", "value": 15, "emoji": "🪶", "desc": "Heilt 15 HP & entfernt Blutung","max_stack": 3,  "sell": 40},
    "Energie-Kristall": {"effect": "energy",  "value": 15, "emoji": "💎", "desc": "Stellt 15 Energie wieder her",  "max_stack": 5,  "sell": 12},
    "Stärketrank":      {"effect": "attack",  "value": 3,  "emoji": "💪", "desc": "+3 ATK für diesen Kampf",       "max_stack": 3,  "sell": 20},
    "Antidot":          {"effect": "cleanse", "value": 0,  "emoji": "🌿", "desc": "Entfernt Blutung & Gift",       "max_stack": 5,  "sell": 5},
}

JUNK_DEFS = {
    "Altes Seil":        {"emoji": "🪢", "desc": "Wertloser Schrott",        "sell": 3},
    "Lumpen":            {"emoji": "🧣", "desc": "Zerfetzter Stoff",          "sell": 2},
    "Knochen":           {"emoji": "🦴", "desc": "Ein morscher Knochen",      "sell": 4},
    "Schleimklumpen":    {"emoji": "🟢", "desc": "Eklig, aber verkäuflich",   "sell": 5},
    "Goblinzahn":        {"emoji": "🦷", "desc": "Riecht furchtbar",          "sell": 6},
    "Trollfell":         {"emoji": "🐾", "desc": "Dickes, zähes Fell",        "sell": 8},
    "Wolfspelz":         {"emoji": "🐺", "desc": "Dunkler Schattenwolfpelz",  "sell": 7},
    "Banditen-Abzeichen":{"emoji": "🏴", "desc": "Zeichen einer Diebesgilde", "sell": 9},
}

EQUIPMENT_DEFS = {
    # ── STARTER (nicht verkaufbar) ────────────────────────────
    "Fäuste":        {"slot": "weapon", "attack": 0,  "rarity": "common",    "emoji": "👊",  "sell": 0,   "desc": "Bloße Hände"},
    "Lumpen":        {"slot": "chest",  "armor": 0,   "rarity": "common",    "emoji": "🧣",  "sell": 0,   "desc": "Zerfetzte Lumpen"},
    "Kein Helm":     {"slot": "head",   "armor": 0,   "rarity": "common",    "emoji": "❌",  "sell": 0,   "desc": "Kein Kopfschutz"},
    "Keine Schuhe":  {"slot": "feet",   "armor": 0,   "rarity": "common",    "emoji": "🦶",  "sell": 0,   "desc": "Barfuß"},
    # ── WAFFEN ───────────────────────────────────────────────────
    "Kurzschwert":          {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🗡️",  "sell": 20,  "desc": "Ein einfaches Schwert"},
    "Langschwert":          {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "⚔️",  "sell": 40,  "desc": "Ausgewogene Klinge"},
    "Kriegshammer":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🔨",  "sell": 60,  "desc": "Wuchtig und langsam"},
    "Runenschwert":         {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Mit Magie durchzogen"},
    "Drachenzahn":          {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Geschmiedet aus Drachenzahn"},
    "Göttliche Klinge":     {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Waffe der Götter"},
    # ── RÜSTUNGEN ─────────────────────────────────────────────────
    "Lederrüstung":         {"slot": "chest",  "armor": 2,   "rarity": "common",    "emoji": "🥋",  "sell": 17,  "desc": "Leichter Schutz"},
    "Kettenhemd":           {"slot": "chest",  "armor": 4,   "rarity": "uncommon",  "emoji": "🔗",  "sell": 35,  "desc": "Gute Balance"},
    "Plattenpanzer":        {"slot": "chest",  "armor": 7,   "rarity": "uncommon",  "emoji": "🛡️",  "sell": 60,  "desc": "Schwerer Stahl"},
    "Runenrüstung":         {"slot": "chest",  "armor": 10,  "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Magisch verstärkt"},
    "Drachenschuppen":      {"slot": "chest",  "armor": 14,  "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Schuppen eines Drachen"},
    "Rüstung des Lichts":   {"slot": "chest",  "armor": 20,  "rarity": "legendary", "emoji": "⚡",  "sell": 350, "desc": "Von Göttern gesegnet"},
    # ── HELME ─────────────────────────────────────────────────────
    "Lederkappe":           {"slot": "head",   "armor": 1,   "rarity": "common",    "emoji": "🪖",  "sell": 12,  "desc": "Einfacher Kopfschutz"},
    "Eisenhelm":            {"slot": "head",   "armor": 2,   "rarity": "common",    "emoji": "⛑️",  "sell": 22,  "desc": "Solider Schutz"},
    "Stahlhelm":            {"slot": "head",   "armor": 4,   "rarity": "uncommon",  "emoji": "🪖",  "sell": 45,  "desc": "Gehärteter Stahl"},
    "Runenhelm":            {"slot": "head",   "armor": 6,   "rarity": "rare",      "emoji": "🌀",  "sell": 90,  "desc": "Runen leuchten schwach"},
    "Drachenkrone":         {"slot": "head",   "armor": 9,   "rarity": "epic",      "emoji": "👑",  "sell": 140, "desc": "Krone eines Drachenfürsten"},
    "Krone des Ewigen":     {"slot": "head",   "armor": 13,  "rarity": "legendary", "emoji": "🌟",  "sell": 300, "desc": "Trägt, wer Ewigkeit verdient"},
    # ── SCHATTEN-SET ──────────────────────────────────────────────
    "Schattendolch":        {"slot": "weapon", "attack": 7,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 50,  "desc": "Schnell und lautlos"},
    "Schattenrüstung":      {"slot": "chest",  "armor": 8,   "rarity": "rare",      "emoji": "🌑",  "sell": 85,  "desc": "Gewobene Dunkelheit"},
    "Schattenhelm":         {"slot": "head",   "armor": 5,   "rarity": "rare",      "emoji": "🌑",  "sell": 70,  "desc": "Verbirgt das Gesicht"},
    "Schattenstiefel":      {"slot": "feet",   "armor": 3,   "rarity": "uncommon",  "emoji": "🌑",  "sell": 32,  "desc": "Lautlose Sohlen"},
    # ── EXTRA WAFFEN ──────────────────────────────────────────────
    "Sturmklinge":          {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Züngelnde Blitze"},
    "Knochensense":         {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Aus Totenknochen gefertigt"},
    # ── PASSIVE WAFFEN ────────────────────────────────────────────
    "Giftklaue":            {"slot": "weapon", "attack":  5, "rarity": "uncommon",  "emoji": "☠️",  "sell": 40,  "desc": "Jeder Treffer: +1 Giftstack",      "passive": "poison_on_hit"},
    "Flammenklinge":        {"slot": "weapon", "attack":  8, "rarity": "rare",      "emoji": "🔥",  "sell": 70,  "desc": "25% Chance: 2 Verbrennungsstacks", "passive": "burn_on_hit"},
    "Eisaxt":               {"slot": "weapon", "attack": 10, "rarity": "rare",      "emoji": "❄️",  "sell": 85,  "desc": "20% Chance: Einfrieren (1 Runde)", "passive": "freeze_on_hit"},
    "Runen-Kriegshammer":   {"slot": "weapon", "attack": 12, "rarity": "rare",      "emoji": "🔨",  "sell": 95,  "desc": "30% Chance: -3 DEF-Debuff",        "passive": "def_debuff_on_hit"},
    # ── RUNEN-PANZER-SET (Ruinen) ─────────────────────────────────
    "Panzerklinge":         {"slot": "weapon", "attack":  9, "rarity": "rare",      "emoji": "🛡️",  "sell": 75,  "desc": "Klinge des Runenpanzers"},
    "Runen-Platte":         {"slot": "chest",  "armor":   8, "rarity": "rare",      "emoji": "🛡️",  "sell": 75,  "desc": "Gepanzerte Runenrüstung"},
    "Runen-Visier":         {"slot": "head",   "armor":   4, "rarity": "rare",      "emoji": "🛡️",  "sell": 60,  "desc": "Visier des Runenpanzers"},
    "Runen-Schritte":       {"slot": "feet",   "armor":   3, "rarity": "rare",      "emoji": "🛡️",  "sell": 50,  "desc": "Schwere Panzerschritte"},
    # ── SCHATTENTUCH-SET (Wüste) ──────────────────────────────────
    "Mondklinge":           {"slot": "weapon", "attack":  7, "rarity": "rare",      "emoji": "🌙",  "sell": 65,  "desc": "Leichte Klinge für schnelle Züge"},
    "Schattengewand":       {"slot": "chest",  "armor":   5, "rarity": "rare",      "emoji": "🌙",  "sell": 60,  "desc": "Leichtes Gewand aus Schattenstoff"},
    "Schattenkapuze":       {"slot": "head",   "armor":   2, "rarity": "rare",      "emoji": "🌙",  "sell": 45,  "desc": "Kapuze aus gewebter Dunkelheit"},
    "Schattensandale":      {"slot": "feet",   "armor":   1, "rarity": "rare",      "emoji": "🌙",  "sell": 35,  "desc": "Lautlose Sandalen"},
    # ── DRACHENSCHUPPEN-SET (Vulkan) ──────────────────────────────
    "Schuppenklinge":       {"slot": "weapon", "attack": 14, "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Klinge aus Drachenschuppen"},
    "Schuppenpanzer":       {"slot": "chest",  "armor":  12, "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Panzer aus echten Drachenschuppen"},
    "Schuppenhelm":         {"slot": "head",   "armor":   7, "rarity": "epic",      "emoji": "🐉",  "sell": 100, "desc": "Helm aus Drachenschädelknochen"},
    "Schuppenstiefel":      {"slot": "feet",   "armor":   5, "rarity": "epic",      "emoji": "🐉",  "sell": 85,  "desc": "Stiefel aus Drachenhaut"},
    # ── VERDAMMTEN-STAHL-SET (Dunkel-Reich) ───────────────────────
    "Verdammte Klinge":     {"slot": "weapon", "attack": 18, "rarity": "epic",      "emoji": "💀",  "sell": 175, "desc": "Klinge des Verdammten"},
    "Verdammte Rüstung":    {"slot": "chest",  "armor":  12, "rarity": "epic",      "emoji": "💀",  "sell": 165, "desc": "Rüstung aus verdammtem Metall"},
    "Verdammter Helm":      {"slot": "head",   "armor":   7, "rarity": "epic",      "emoji": "💀",  "sell": 125, "desc": "Helm des Verdammten"},
    "Verdammte Stiefel":    {"slot": "feet",   "armor":   5, "rarity": "epic",      "emoji": "💀",  "sell": 105, "desc": "Stiefel des Verdammten"},
    # ── KLASSEN-RÜSTUNGSSETS ──────────────────────────────────────
    "Festungsklinge":  {"slot": "weapon", "attack": 15, "rarity": "epic", "emoji": "🏰", "sell": 140, "desc": "Klinge des Festungsritters",   "class_only": "warrior"},
    "Festungsplatte":  {"slot": "chest",  "armor":  12, "rarity": "epic", "emoji": "🏰", "sell": 140, "desc": "Platte aus Festungsstein",     "class_only": "warrior"},
    "Festungshelm":    {"slot": "head",   "armor":   8, "rarity": "epic", "emoji": "🏰", "sell": 100, "desc": "Helm der Eisenfestung",        "class_only": "warrior"},
    "Festungsstiefel": {"slot": "feet",   "armor":   7, "rarity": "epic", "emoji": "🏰", "sell":  95, "desc": "Stiefel aus getriebenem Eisen","class_only": "warrior"},
    "Hüllendolch":     {"slot": "weapon", "attack": 14, "rarity": "epic", "emoji": "🌙", "sell": 135, "desc": "Dolch aus gewebtem Schatten",  "class_only": "rogue"},
    "Hüllenpanzer":    {"slot": "chest",  "armor":  11, "rarity": "epic", "emoji": "🌙", "sell": 130, "desc": "Rüstung der Schattenhülle",    "class_only": "rogue"},
    "Hüllenmaske":     {"slot": "head",   "armor":   7, "rarity": "epic", "emoji": "🌙", "sell":  95, "desc": "Maske aus Nachtgarn",          "class_only": "rogue"},
    "Hüllenstiefel":   {"slot": "feet",   "armor":   6, "rarity": "epic", "emoji": "🌙", "sell":  85, "desc": "Lautlos wie der Mond",         "class_only": "rogue"},
    "Arkaner Stab":    {"slot": "weapon", "attack": 13, "rarity": "epic", "emoji": "🔮", "sell": 125, "desc": "Stab aus kristallisierter Magie","class_only": "mage"},
    "Arkane Robe":     {"slot": "chest",  "armor":  10, "rarity": "epic", "emoji": "🔮", "sell": 125, "desc": "Von Arkaner Energie durchwirkt","class_only": "mage"},
    "Arkane Kapuze":   {"slot": "head",   "armor":   6, "rarity": "epic", "emoji": "🔮", "sell":  90, "desc": "Kapuze des Arkanen Weisen",    "class_only": "mage"},
    "Arkane Schuhe":   {"slot": "feet",   "armor":   5, "rarity": "epic", "emoji": "🔮", "sell":  80, "desc": "Gleiten über den Äther",       "class_only": "mage"},
    # ── KLASSEN-WAFFEN (gleiche Stats, klassenspezifischer Name) ──
    "Kampfschwert":         {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "⚔️",  "sell": 20,  "desc": "Kräftige Klinge für den Nahkampf"},
    "Spitzdolch":           {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🗡️",  "sell": 20,  "desc": "Schnell und präzise"},
    "Novizenstab":          {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🪄",  "sell": 20,  "desc": "Einfacher Magierstab"},
    "Bastardschwert":       {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "⚔️",  "sell": 40,  "desc": "Schwere Zweihandklinge"},
    "Klingenschatten":      {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 40,  "desc": "Im Schatten kaum sichtbar"},
    "Magierstab":           {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "🪄",  "sell": 40,  "desc": "Verstärkt magische Kräfte"},
    "Streitaxt":            {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🪓",  "sell": 60,  "desc": "Brutal und wuchtig"},
    "Schattenbeil":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 60,  "desc": "Lautlos und tödlich"},
    "Arkane Keule":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🔮",  "sell": 60,  "desc": "Mit arkaner Energie geladen"},
    "Gewitterschwert":      {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Blitze tanzen auf der Klinge"},
    "Blitzdolch":           {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Schnell wie ein Blitz"},
    "Sturmstab":            {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "🌩️",  "sell": 90,  "desc": "Beschwört Blitzgewitter"},
    "Runenklinge":          {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Runen schützen den Träger"},
    "Runendolch":           {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Magische Runenschärfe"},
    "Runenstab":            {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Kanalisiert Runenkraft"},
    "Kriegssense":          {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "⚔️",  "sell": 145, "desc": "Mäht durch Feinde wie Gras"},
    "Seelenstehler":        {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Stiehlt die Seele des Feindes"},
    "Totenstab":            {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Beschwört Todesenergien"},
    "Drachenklaue":         {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Scharfe Drachenkralle"},
    "Drachenstich":         {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Präzise wie ein Drachenangriff"},
    "Drachenstab":          {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Von Drachenmagie durchdrungen"},
    "Heilige Klinge":       {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Gesegnet von den Göttern"},
    "Klingengeist":         {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "👻",  "sell": 350, "desc": "Ein Geist wohnt in der Klinge"},
    "Götterstab":           {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Würdig eines Gottes"},
    # ── SCHUHE ────────────────────────────────────────────────────
    "Lederstiefel":         {"slot": "feet",   "armor": 1,   "rarity": "common",    "emoji": "👞",  "sell": 10,  "desc": "Einfache Lederschuhe"},
    "Eisenstiefel":         {"slot": "feet",   "armor": 2,   "rarity": "common",    "emoji": "🥾",  "sell": 20,  "desc": "Schwere Eisensohlen"},
    "Kriegsstiefel":        {"slot": "feet",   "armor": 3,   "rarity": "uncommon",  "emoji": "🥾",  "sell": 35,  "desc": "Gehärtete Kriegssohlen"},
    "Schnellläuferstiefel": {"slot": "feet",   "armor": 4,   "rarity": "uncommon",  "emoji": "💨",  "sell": 42,  "desc": "Leicht und wendig"},
    "Runenstiefel":         {"slot": "feet",   "armor": 6,   "rarity": "rare",      "emoji": "🌀",  "sell": 85,  "desc": "Mit Schutzrunen versehen"},
    "Drachenklauen":        {"slot": "feet",   "armor": 9,   "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Krallen eines Drachen"},
    "Stiefel der Ewigkeit": {"slot": "feet",   "armor": 12,  "rarity": "legendary", "emoji": "⚡",  "sell": 280, "desc": "Kein Weg ist zu weit"},
}

# Generische Waffe → klassenspezifische Variante
CLASS_WEAPON_MAP = {
    "Kurzschwert":      {"warrior": "Kampfschwert",    "rogue": "Spitzdolch",      "mage": "Novizenstab"},
    "Langschwert":      {"warrior": "Bastardschwert",  "rogue": "Klingenschatten", "mage": "Magierstab"},
    "Kriegshammer":     {"warrior": "Streitaxt",       "rogue": "Schattenbeil",    "mage": "Arkane Keule"},
    "Sturmklinge":      {"warrior": "Gewitterschwert", "rogue": "Blitzdolch",      "mage": "Sturmstab"},
    "Runenschwert":     {"warrior": "Runenklinge",     "rogue": "Runendolch",      "mage": "Runenstab"},
    "Knochensense":     {"warrior": "Kriegssense",     "rogue": "Seelenstehler",   "mage": "Totenstab"},
    "Drachenzahn":      {"warrior": "Drachenklaue",    "rogue": "Drachenstich",    "mage": "Drachenstab"},
    "Göttliche Klinge": {"warrior": "Heilige Klinge",  "rogue": "Klingengeist",    "mage": "Götterstab"},
}

# Rückwärts-Map: Klassenvariante → generische Basiswaffe (für Set-Bonus-Prüfung)
WEAPON_VARIANT_TO_BASE = {
    variant: base
    for base, variants in CLASS_WEAPON_MAP.items()
    for variant in variants.values()
}

RARITY_LABEL = {
    "common":    ("Gewöhnlich",  "⬜"),
    "uncommon":  ("Ungewöhnlich","🟩"),
    "rare":      ("Selten",      "🟦"),
    "epic":      ("Episch",      "🟪"),
    "legendary": ("Legendär",    "🟨"),
}

CRAFT_RECIPES = {
    "antidot": {
        "output": "Antidot", "output_count": 1,
        "inputs": {"Knochen": 3},
        "desc": "3× Knochen → 1× Antidot",
    },
    "staerketrank": {
        "output": "Stärketrank", "output_count": 1,
        "inputs": {"Trollfell": 2, "Goblinzahn": 1},
        "desc": "2× Trollfell + 1× Goblinzahn → 1× Stärketrank",
    },
    "energie_kristall": {
        "output": "Energie-Kristall", "output_count": 1,
        "inputs": {"Schleimklumpen": 3},
        "desc": "3× Schleimklumpen → 1× Energie-Kristall",
    },
    "healing_potion": {
        "output": "Healing Potion", "output_count": 1,
        "inputs": {"Wolfspelz": 2, "Lumpen": 1},
        "desc": "2× Wolfspelz + 1× Lumpen → 1× Healing Potion",
    },
}
