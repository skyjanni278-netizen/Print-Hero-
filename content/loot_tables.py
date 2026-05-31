import random


# Alle Consumables: Effekt, Wert, Stack-Limit, Verkaufspreis
CONSUMABLE_DEFS = {
    "Healing Potion":   {"effect": "heal",    "value": 10, "emoji": "🧪", "desc": "Heilt 10 HP",                   "max_stack": 5,  "sell": 7},
    "Großes Heiltrank": {"effect": "heal",    "value": 25, "emoji": "🍶", "desc": "Heilt 25 HP",                   "max_stack": 5,  "sell": 17},
    "Elixier":          {"effect": "heal",    "value": 40, "emoji": "✨", "desc": "Heilt 40 HP",                   "max_stack": 3,  "sell": 30},
    "Phönixfeder":      {"effect": "cleanse", "value": 15, "emoji": "🪶", "desc": "Heilt 15 HP & entfernt Blutung","max_stack": 3,  "sell": 40},
    "Energie-Kristall": {"effect": "energy",  "value": 15, "emoji": "💎", "desc": "Stellt 15 Energie wieder her",  "max_stack": 5,  "sell": 12},
    "Stärketrank":      {"effect": "attack",  "value": 3,  "emoji": "💪", "desc": "+3 ATK für diesen Kampf",       "max_stack": 3,  "sell": 20},
    "Antidot":          {"effect": "cleanse", "value": 0,  "emoji": "🌿", "desc": "Entfernt Blutung & Gift",       "max_stack": 5,  "sell": 5},
}

# Junk-Items: nur zum Verkaufen
JUNK_DEFS = {
    "Altes Seil":     {"emoji": "🪢", "desc": "Wertloser Schrott",        "sell": 3},
    "Lumpen":         {"emoji": "🧣", "desc": "Zerfetzter Stoff",          "sell": 2},
    "Knochen":        {"emoji": "🦴", "desc": "Ein morscher Knochen",      "sell": 4},
    "Schleimklumpen": {"emoji": "🟢", "desc": "Eklig, aber verkäuflich",   "sell": 5},
    "Goblinzahn":     {"emoji": "🦷", "desc": "Riecht furchtbar",          "sell": 6},
    "Trollfell":      {"emoji": "🐾", "desc": "Dickes, zähes Fell",        "sell": 8},
    "Wolfspelz":      {"emoji": "🐺", "desc": "Dunkler Schattenwolfpelz",  "sell": 7},
    "Banditen-Abzeichen": {"emoji": "🏴", "desc": "Zeichen einer Diebesgilde", "sell": 9},
}

EQUIPMENT_DEFS = {
    # ── STARTER (nicht verkaufbar, nur für KeyError-Schutz) ──
    "Fäuste":        {"slot": "weapon", "attack": 0,  "rarity": "common",    "emoji": "👊",  "sell": 0,   "desc": "Bloße Hände"},
    "Lumpen":        {"slot": "chest",  "armor": 0,   "rarity": "common",    "emoji": "🧣",  "sell": 0,   "desc": "Zerfetzte Lumpen"},
    "Kein Helm":     {"slot": "head",   "armor": 0,   "rarity": "common",    "emoji": "❌",  "sell": 0,   "desc": "Kein Kopfschutz"},
    "Keine Schuhe":  {"slot": "feet",   "armor": 0,   "rarity": "common",    "emoji": "🦶",  "sell": 0,   "desc": "Barfuß"},
    # ── WAFFEN ───────────────────────────────────────────────
    "Kurzschwert":          {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🗡️",  "sell": 20,  "desc": "Ein einfaches Schwert"},
    "Langschwert":          {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "⚔️",  "sell": 40,  "desc": "Ausgewogene Klinge"},
    "Kriegshammer":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🔨",  "sell": 60,  "desc": "Wuchtig und langsam"},
    "Runenschwert":         {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Mit Magie durchzogen"},
    "Drachenzahn":          {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Geschmiedet aus Drachenzahn"},
    "Göttliche Klinge":     {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Waffe der Götter"},
    # ── RÜSTUNGEN ────────────────────────────────────────────
    "Lederrüstung":         {"slot": "chest",  "armor": 2,   "rarity": "common",    "emoji": "🥋",  "sell": 17,  "desc": "Leichter Schutz"},
    "Kettenhemd":           {"slot": "chest",  "armor": 4,   "rarity": "uncommon",  "emoji": "🔗",  "sell": 35,  "desc": "Gute Balance"},
    "Plattenpanzer":        {"slot": "chest",  "armor": 7,   "rarity": "uncommon",  "emoji": "🛡️",  "sell": 60,  "desc": "Schwerer Stahl"},
    "Runenrüstung":         {"slot": "chest",  "armor": 10,  "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Magisch verstärkt"},
    "Drachenschuppen":      {"slot": "chest",  "armor": 14,  "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Schuppen eines Drachen"},
    "Rüstung des Lichts":   {"slot": "chest",  "armor": 20,  "rarity": "legendary", "emoji": "⚡",  "sell": 350, "desc": "Von Göttern gesegnet"},
    # ── HELME ────────────────────────────────────────────────
    "Lederkappe":           {"slot": "head",   "armor": 1,   "rarity": "common",    "emoji": "🪖",  "sell": 12,  "desc": "Einfacher Kopfschutz"},
    "Eisenhelm":            {"slot": "head",   "armor": 2,   "rarity": "common",    "emoji": "⛑️",  "sell": 22,  "desc": "Solider Schutz"},
    "Stahlhelm":            {"slot": "head",   "armor": 4,   "rarity": "uncommon",  "emoji": "🪖",  "sell": 45,  "desc": "Gehärteter Stahl"},
    "Runenhelm":            {"slot": "head",   "armor": 6,   "rarity": "rare",      "emoji": "🌀",  "sell": 90,  "desc": "Runen leuchten schwach"},
    "Drachenkrone":         {"slot": "head",   "armor": 9,   "rarity": "epic",      "emoji": "👑",  "sell": 140, "desc": "Krone eines Drachenfürsten"},
    "Krone des Ewigen":     {"slot": "head",   "armor": 13,  "rarity": "legendary", "emoji": "🌟",  "sell": 300, "desc": "Trägt, wer Ewigkeit verdient"},
    # ── SCHATTEN-SET ─────────────────────────────────────────
    "Schattendolch":        {"slot": "weapon", "attack": 7,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 50,  "desc": "Schnell und lautlos"},
    "Schattenrüstung":      {"slot": "chest",  "armor": 8,   "rarity": "rare",      "emoji": "🌑",  "sell": 85,  "desc": "Gewobene Dunkelheit"},
    "Schattenhelm":         {"slot": "head",   "armor": 5,   "rarity": "rare",      "emoji": "🌑",  "sell": 70,  "desc": "Verbirgt das Gesicht"},
    "Schattenstiefel":      {"slot": "feet",   "armor": 3,   "rarity": "uncommon",  "emoji": "🌑",  "sell": 32,  "desc": "Lautlose Sohlen"},
    # ── EXTRA WAFFEN ─────────────────────────────────────────
    "Sturmklinge":          {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Züngelnde Blitze"},
    "Knochensense":         {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Aus Totenknochen gefertigt"},
    # ── PASSIVE WAFFEN ───────────────────────────────────────
    "Giftklaue":            {"slot": "weapon", "attack":  5, "rarity": "uncommon",  "emoji": "☠️",  "sell": 40,  "desc": "Jeder Treffer: +1 Giftstack",       "passive": "poison_on_hit"},
    "Flammenklinge":        {"slot": "weapon", "attack":  8, "rarity": "rare",      "emoji": "🔥",  "sell": 70,  "desc": "25% Chance: 2 Verbrennungsstacks",  "passive": "burn_on_hit"},
    "Eisaxt":               {"slot": "weapon", "attack": 10, "rarity": "rare",      "emoji": "❄️",  "sell": 85,  "desc": "20% Chance: Einfrieren (1 Runde)",  "passive": "freeze_on_hit"},
    "Runen-Kriegshammer":   {"slot": "weapon", "attack": 12, "rarity": "rare",      "emoji": "🔨",  "sell": 95,  "desc": "30% Chance: -3 DEF-Debuff",         "passive": "def_debuff_on_hit"},
    # ── RUNEN-PANZER-SET (Ruinen) ────────────────────────────
    "Panzerklinge":         {"slot": "weapon", "attack":  9, "rarity": "rare",      "emoji": "🛡️",  "sell": 75,  "desc": "Klinge des Runenpanzers"},
    "Runen-Platte":         {"slot": "chest",  "armor":   8, "rarity": "rare",      "emoji": "🛡️",  "sell": 75,  "desc": "Gepanzerte Runenrüstung"},
    "Runen-Visier":         {"slot": "head",   "armor":   4, "rarity": "rare",      "emoji": "🛡️",  "sell": 60,  "desc": "Visier des Runenpanzers"},
    "Runen-Schritte":       {"slot": "feet",   "armor":   3, "rarity": "rare",      "emoji": "🛡️",  "sell": 50,  "desc": "Schwere Panzerschritte"},
    # ── SCHATTENTUCH-SET (Wüste) ─────────────────────────────
    "Mondklinge":           {"slot": "weapon", "attack":  7, "rarity": "rare",      "emoji": "🌙",  "sell": 65,  "desc": "Leichte Klinge für schnelle Züge"},
    "Schattengewand":       {"slot": "chest",  "armor":   5, "rarity": "rare",      "emoji": "🌙",  "sell": 60,  "desc": "Leichtes Gewand aus Schattenstoff"},
    "Schattenkapuze":       {"slot": "head",   "armor":   2, "rarity": "rare",      "emoji": "🌙",  "sell": 45,  "desc": "Kapuze aus gewebter Dunkelheit"},
    "Schattensandale":      {"slot": "feet",   "armor":   1, "rarity": "rare",      "emoji": "🌙",  "sell": 35,  "desc": "Lautlose Sandalen"},
    # ── DRACHENSCHUPPEN-SET (Vulkan) ─────────────────────────
    "Schuppenklinge":       {"slot": "weapon", "attack": 14, "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Klinge aus Drachenschuppen"},
    "Schuppenpanzer":       {"slot": "chest",  "armor":  12, "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Panzer aus echten Drachenschuppen"},
    "Schuppenhelm":         {"slot": "head",   "armor":   7, "rarity": "epic",      "emoji": "🐉",  "sell": 100, "desc": "Helm aus Drachenschädelknochen"},
    "Schuppenstiefel":      {"slot": "feet",   "armor":   5, "rarity": "epic",      "emoji": "🐉",  "sell": 85,  "desc": "Stiefel aus Drachenhaut"},
    # ── VERDAMMTEN-STAHL-SET (Dunkel-Reich) ──────────────────
    "Verdammte Klinge":     {"slot": "weapon", "attack": 18, "rarity": "epic",      "emoji": "💀",  "sell": 175, "desc": "Klinge des Verdammten"},
    "Verdammte Rüstung":    {"slot": "chest",  "armor":  12, "rarity": "epic",      "emoji": "💀",  "sell": 165, "desc": "Rüstung aus verdammtem Metall"},
    "Verdammter Helm":      {"slot": "head",   "armor":   7, "rarity": "epic",      "emoji": "💀",  "sell": 125, "desc": "Helm des Verdammten"},
    "Verdammte Stiefel":    {"slot": "feet",   "armor":   5, "rarity": "epic",      "emoji": "💀",  "sell": 105, "desc": "Stiefel des Verdammten"},
    # ── KLASSEN-RÜSTUNGSSETS ─────────────────────────────────────
    # Eisenfestung (Krieger, epic)
    "Festungsklinge":   {"slot": "weapon", "attack": 15, "rarity": "epic", "emoji": "🏰", "sell": 140, "desc": "Klinge des Festungsritters",  "class_only": "warrior"},
    "Festungsplatte":   {"slot": "chest",  "armor":  12, "rarity": "epic", "emoji": "🏰", "sell": 140, "desc": "Platte aus Festungsstein",    "class_only": "warrior"},
    "Festungshelm":     {"slot": "head",   "armor":   8, "rarity": "epic", "emoji": "🏰", "sell": 100, "desc": "Helm der Eisenfestung",       "class_only": "warrior"},
    "Festungsstiefel":  {"slot": "feet",   "armor":   7, "rarity": "epic", "emoji": "🏰", "sell":  95, "desc": "Stiefel aus getriebenem Eisen","class_only": "warrior"},
    # Schattenhülle (Schurke, epic)
    "Hüllendolch":      {"slot": "weapon", "attack": 14, "rarity": "epic", "emoji": "🌙", "sell": 135, "desc": "Dolch aus gewebtem Schatten",  "class_only": "rogue"},
    "Hüllenpanzer":     {"slot": "chest",  "armor":  11, "rarity": "epic", "emoji": "🌙", "sell": 130, "desc": "Rüstung der Schattenhülle",   "class_only": "rogue"},
    "Hüllenmaske":      {"slot": "head",   "armor":   7, "rarity": "epic", "emoji": "🌙", "sell":  95, "desc": "Maske aus Nachtgarn",         "class_only": "rogue"},
    "Hüllenstiefel":    {"slot": "feet",   "armor":   6, "rarity": "epic", "emoji": "🌙", "sell":  85, "desc": "Lautlos wie der Mond",        "class_only": "rogue"},
    # Arkane Roben (Magier, epic)
    "Arkaner Stab":     {"slot": "weapon", "attack": 13, "rarity": "epic", "emoji": "🔮", "sell": 125, "desc": "Stab aus kristallisierter Magie","class_only": "mage"},
    "Arkane Robe":      {"slot": "chest",  "armor":  10, "rarity": "epic", "emoji": "🔮", "sell": 125, "desc": "Von Arkaner Energie durchwirkt","class_only": "mage"},
    "Arkane Kapuze":    {"slot": "head",   "armor":   6, "rarity": "epic", "emoji": "🔮", "sell":  90, "desc": "Kapuze des Arkanen Weisen",   "class_only": "mage"},
    "Arkane Schuhe":    {"slot": "feet",   "armor":   5, "rarity": "epic", "emoji": "🔮", "sell":  80, "desc": "Gleiten über den Äther",      "class_only": "mage"},
    # ── KLASSEN-WAFFEN (gleiche Stats, klassenspezifischer Name) ─
    # Kurzschwert-Varianten (common, ATK 3)
    "Kampfschwert":         {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "⚔️",  "sell": 20,  "desc": "Kräftige Klinge für den Nahkampf"},
    "Spitzdolch":           {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🗡️",  "sell": 20,  "desc": "Schnell und präzise"},
    "Novizenstab":          {"slot": "weapon", "attack": 3,  "rarity": "common",    "emoji": "🪄",  "sell": 20,  "desc": "Einfacher Magierstab"},
    # Langschwert-Varianten (uncommon, ATK 6)
    "Bastardschwert":       {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "⚔️",  "sell": 40,  "desc": "Schwere Zweihandklinge"},
    "Klingenschatten":      {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 40,  "desc": "Im Schatten kaum sichtbar"},
    "Magierstab":           {"slot": "weapon", "attack": 6,  "rarity": "uncommon",  "emoji": "🪄",  "sell": 40,  "desc": "Verstärkt magische Kräfte"},
    # Kriegshammer-Varianten (uncommon, ATK 9)
    "Streitaxt":            {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🪓",  "sell": 60,  "desc": "Brutal und wuchtig"},
    "Schattenbeil":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🌑",  "sell": 60,  "desc": "Lautlos und tödlich"},
    "Arkane Keule":         {"slot": "weapon", "attack": 9,  "rarity": "uncommon",  "emoji": "🔮",  "sell": 60,  "desc": "Mit arkaner Energie geladen"},
    # Sturmklinge-Varianten (rare, ATK 11)
    "Gewitterschwert":      {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Blitze tanzen auf der Klinge"},
    "Blitzdolch":           {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "⚡",  "sell": 90,  "desc": "Schnell wie ein Blitz"},
    "Sturmstab":            {"slot": "weapon", "attack": 11, "rarity": "rare",      "emoji": "🌩️",  "sell": 90,  "desc": "Beschwört Blitzgewitter"},
    # Runenschwert-Varianten (rare, ATK 13)
    "Runenklinge":          {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Runen schützen den Träger"},
    "Runendolch":           {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Magische Runenschärfe"},
    "Runenstab":            {"slot": "weapon", "attack": 13, "rarity": "rare",      "emoji": "🌀",  "sell": 100, "desc": "Kanalisiert Runenkraft"},
    # Knochensense-Varianten (epic, ATK 15)
    "Kriegssense":          {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "⚔️",  "sell": 145, "desc": "Mäht durch Feinde wie Gras"},
    "Seelenstehler":        {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Stiehlt die Seele des Feindes"},
    "Totenstab":            {"slot": "weapon", "attack": 15, "rarity": "epic",      "emoji": "💀",  "sell": 145, "desc": "Beschwört Todesenergien"},
    # Drachenzahn-Varianten (epic, ATK 17)
    "Drachenklaue":         {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Scharfe Drachenkralle"},
    "Drachenstich":         {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Präzise wie ein Drachenangriff"},
    "Drachenstab":          {"slot": "weapon", "attack": 17, "rarity": "epic",      "emoji": "🐉",  "sell": 160, "desc": "Von Drachenmagie durchdrungen"},
    # Göttliche Klinge-Varianten (legendary, ATK 25)
    "Heilige Klinge":       {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Gesegnet von den Göttern"},
    "Klingengeist":         {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "👻",  "sell": 350, "desc": "Ein Geist wohnt in der Klinge"},
    "Götterstab":           {"slot": "weapon", "attack": 25, "rarity": "legendary", "emoji": "✨",  "sell": 350, "desc": "Würdig eines Gottes"},
    # ── SCHUHE ───────────────────────────────────────────────
    "Lederstiefel":         {"slot": "feet",   "armor": 1,   "rarity": "common",    "emoji": "👞",  "sell": 10,  "desc": "Einfache Lederschuhe"},
    "Eisenstiefel":         {"slot": "feet",   "armor": 2,   "rarity": "common",    "emoji": "🥾",  "sell": 20,  "desc": "Schwere Eisensohlen"},
    "Kriegsstiefel":        {"slot": "feet",   "armor": 3,   "rarity": "uncommon",  "emoji": "🥾",  "sell": 35,  "desc": "Gehärtete Kriegssohlen"},
    "Schnellläuferstiefel": {"slot": "feet",   "armor": 4,   "rarity": "uncommon",  "emoji": "💨",  "sell": 42,  "desc": "Leicht und wendig"},
    "Runenstiefel":         {"slot": "feet",   "armor": 6,   "rarity": "rare",      "emoji": "🌀",  "sell": 85,  "desc": "Mit Schutzrunen versehen"},
    "Drachenklauen":        {"slot": "feet",   "armor": 9,   "rarity": "epic",      "emoji": "🐉",  "sell": 130, "desc": "Krallen eines Drachen"},
    "Stiefel der Ewigkeit": {"slot": "feet",   "armor": 12,  "rarity": "legendary", "emoji": "⚡",  "sell": 280, "desc": "Kein Weg ist zu weit"},
}

# Generische Waffe → klassenspezifische Variante beim Drop
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

# Rarity-Label und Farb-Emoji für Anzeige
RARITY_LABEL = {
    "common":    ("Gewöhnlich",  "⬜"),
    "uncommon":  ("Ungewöhnlich","🟩"),
    "rare":      ("Selten",      "🟦"),
    "epic":      ("Episch",      "🟪"),
    "legendary": ("Legendär",    "🟨"),
}

# Handwerk: Junk → Consumables
CRAFT_RECIPES = {
    "antidot": {
        "output": "Antidot",
        "output_count": 1,
        "inputs": {"Knochen": 3},
        "desc": "3× Knochen → 1× Antidot",
    },
    "staerketrank": {
        "output": "Stärketrank",
        "output_count": 1,
        "inputs": {"Trollfell": 2, "Goblinzahn": 1},
        "desc": "2× Trollfell + 1× Goblinzahn → 1× Stärketrank",
    },
    "energie_kristall": {
        "output": "Energie-Kristall",
        "output_count": 1,
        "inputs": {"Schleimklumpen": 3},
        "desc": "3× Schleimklumpen → 1× Energie-Kristall",
    },
    "healing_potion": {
        "output": "Healing Potion",
        "output_count": 1,
        "inputs": {"Wolfspelz": 2, "Lumpen": 1},
        "desc": "2× Wolfspelz + 1× Lumpen → 1× Healing Potion",
    },
}

# Ausrüstungs-Sets: 4 Teile je Set, Boni bei 2/3/4 angelegten Teilen
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
            2: {"desc": "+3 DEF",                               "atk": 0, "def": 3},
            3: {"desc": "+3 DEF +2 ATK",                        "atk": 2, "def": 3},
            4: {"desc": "+6 DEF +4 ATK — +3 Energie/Runde",     "atk": 4, "def": 6, "special": "eisen_energy_regen"},
        },
    },
    "Stahl-Set": {
        "emoji": "🔩",
        "pieces": {"Kriegshammer", "Plattenpanzer", "Stahlhelm", "Schnellläuferstiefel"},
        "bonuses": {
            2: {"desc": "+4 DEF",                              "atk": 0, "def": 4},
            3: {"desc": "+4 DEF +3 ATK",                       "atk": 3, "def": 4},
            4: {"desc": "+8 DEF +6 ATK — Blutungsimmunität",   "atk": 6, "def": 8, "special": "stahl_bleed_immune"},
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
            2: {"desc": "+6 DEF",                           "atk": 0, "def": 6},
            3: {"desc": "+6 DEF +4 ATK",                    "atk": 4, "def": 6},
            4: {"desc": "+12 DEF +8 ATK — +20% XP",         "atk": 8, "def": 12, "special": "runen_xp_bonus"},
        },
    },
    "Drachen-Set": {
        "emoji": "🐉",
        "pieces": {"Drachenzahn", "Drachenschuppen", "Drachenkrone", "Drachenklauen"},
        "bonuses": {
            2: {"desc": "+8 DEF",                                      "atk": 0,  "def": 8},
            3: {"desc": "+8 DEF +6 ATK",                               "atk": 6,  "def": 8},
            4: {"desc": "+15 DEF +12 ATK — 15% Angriff vollst. blocken","atk": 12, "def": 15, "special": "drachen_block"},
        },
    },
    "Licht-Set": {
        "emoji": "✨",
        "pieces": {"Göttliche Klinge", "Rüstung des Lichts", "Krone des Ewigen", "Stiefel der Ewigkeit"},
        "bonuses": {
            2: {"desc": "+12 DEF",                          "atk": 0,  "def": 12},
            3: {"desc": "+12 DEF +10 ATK",                  "atk": 10, "def": 12},
            4: {"desc": "+20 DEF +18 ATK — +3 HP/Runde",    "atk": 18, "def": 20, "special": "licht_hp_regen"},
        },
    },
    # ── NEUE SETS ────────────────────────────────────────────
    "Runen-Panzer": {
        "emoji": "🛡️",
        "pieces": {"Panzerklinge", "Runen-Platte", "Runen-Visier", "Runen-Schritte"},
        "bonuses": {
            2: {"desc": "+3 DEF",                                      "atk": 0, "def": 3},
            3: {"desc": "+5 DEF +2 ATK",                               "atk": 2, "def": 5},
            4: {"desc": "+8 DEF +5 ATK — Blutungsschaden −1/Stack",    "atk": 5, "def": 8, "special": "panzer_bleed_reduce"},
        },
    },
    "Schattentuch": {
        "emoji": "🌙",
        "pieces": {"Mondklinge", "Schattengewand", "Schattenkapuze", "Schattensandale"},
        "bonuses": {
            2: {"desc": "+1 DEF",                                "atk": 0, "def":  1},
            3: {"desc": "+2 DEF +2 ATK",                         "atk": 2, "def":  2},
            4: {"desc": "−3 DEF +2 ATK — 15% Ausweichen",        "atk": 2, "def": -3, "special": "schattentuch_dodge"},
        },
    },
    "Drachenschuppen": {
        "emoji": "🐉",
        "pieces": {"Schuppenklinge", "Schuppenpanzer", "Schuppenhelm", "Schuppenstiefel"},
        "bonuses": {
            2: {"desc": "+6 DEF",                                          "atk": 0, "def":  6},
            3: {"desc": "+9 DEF +4 ATK",                                   "atk": 4, "def":  9},
            4: {"desc": "+12 DEF +8 ATK — 20% Angriff vollst. blocken",    "atk": 8, "def": 12, "special": "schuppen_block"},
        },
    },
    "Verdammten-Stahl": {
        "emoji": "💀",
        "pieces": {"Verdammte Klinge", "Verdammte Rüstung", "Verdammter Helm", "Verdammte Stiefel"},
        "bonuses": {
            2: {"desc": "+2 ATK",           "atk":  2, "def":  0},
            3: {"desc": "+4 ATK −2 DEF",    "atk":  4, "def": -2},
            4: {"desc": "+6 ATK −4 DEF",    "atk":  6, "def": -4},
        },
    },
    # ── KLASSEN-SETS ─────────────────────────────────────────────
    "Eisenfestung": {
        "emoji": "🏰",
        "pieces": {"Festungsklinge", "Festungsplatte", "Festungshelm", "Festungsstiefel"},
        "bonuses": {
            2: {"desc": "+3 DEF",                             "atk": 0, "def": 3},
            3: {"desc": "+3 DEF +2 ATK",                      "atk": 2, "def": 3},
            4: {"desc": "+10 DEF +5 ATK — Schildwall ×2",     "atk": 5, "def": 10, "special": "warrior_2block"},
        },
    },
    "Schattenhülle": {
        "emoji": "🌙",
        "pieces": {"Hüllendolch", "Hüllenpanzer", "Hüllenmaske", "Hüllenstiefel"},
        "bonuses": {
            2: {"desc": "+3 DEF",                                        "atk": 0, "def": 3},
            3: {"desc": "+5 DEF +4 ATK",                                 "atk": 4, "def": 5},
            4: {"desc": "+8 DEF +5 ATK — Aus dem Schatten: +15% Krit-Chance", "atk": 5, "def": 8, "special": "rogue_shadow_regen"},
        },
    },
    "Arkane Roben": {
        "emoji": "🔮",
        "pieces": {"Arkaner Stab", "Arkane Robe", "Arkane Kapuze", "Arkane Schuhe"},
        "bonuses": {
            2: {"desc": "+5 max Energie",                          "atk": 0, "def": 0, "energy":  5},
            3: {"desc": "+10 max Energie +2 ATK",                  "atk": 2, "def": 0, "energy": 10},
            4: {"desc": "+8 DEF +4 ATK +20 Energie — Arkane ×2",  "atk": 4, "def": 8, "energy": 20, "special": "mage_double_arcane"},
        },
    },
}


def get_active_sets(player) -> list:
    """Gibt Liste von (set_name, sdef, count, bonus) für alle aktiven Sets (>= 2 Teile) zurück."""
    equipped = {WEAPON_VARIANT_TO_BASE.get(item["name"], item["name"]) for item in player.equipment.values()}
    result = []
    for sname, sdef in SET_DEFS.items():
        count = len(equipped & sdef["pieces"])
        bonus = sdef["bonuses"].get(count)
        if bonus:
            result.append((sname, sdef, count, bonus))
    return result


def get_set_specials(player) -> set:
    """Gibt Menge aller aktiven 4-teiligen Set-Spezialeffekte zurück."""
    return {b["special"] for _, _, count, b in get_active_sets(player) if count == 4 and "special" in b}

LOOT_POOL = {
    # -- COMMON
    "common": [
        {"name": "Healing Potion",  "type": "consumable", "key": "Healing Potion",  "min": 1, "max": 1},
        {"name": "Gold",            "type": "gold",        "key": "Gold",            "min": 3, "max": 10},
        {"name": "Altes Seil",      "type": "junk",        "key": "Altes Seil",      "min": 1, "max": 2},
        {"name": "Lumpen",          "type": "junk",        "key": "Lumpen",          "min": 1, "max": 3},
        {"name": "Antidot",         "type": "consumable",  "key": "Antidot",         "min": 1, "max": 1},
        {"name": "Knochen",         "type": "junk",        "key": "Knochen",         "min": 1, "max": 2},
        {"name": "Lederkappe",      "type": "equipment",   "key": "Lederkappe"},
        {"name": "Kurzschwert",     "type": "equipment",   "key": "Kurzschwert"},
        {"name": "Lederrüstung",    "type": "equipment",   "key": "Lederrüstung"},
        {"name": "Lederstiefel",    "type": "equipment",   "key": "Lederstiefel"},
        {"name": "Eisenstiefel",    "type": "equipment",   "key": "Eisenstiefel"},
    ],
    # -- UNCOMMON
    "uncommon": [
        {"name": "Großes Heiltrank","type": "consumable",  "key": "Großes Heiltrank","min": 1, "max": 1},
        {"name": "Gold",            "type": "gold",         "key": "Gold",            "min": 10, "max": 25},
        {"name": "Energie-Kristall","type": "consumable",   "key": "Energie-Kristall","min": 1, "max": 1},
        {"name": "Stärketrank",     "type": "consumable",   "key": "Stärketrank",     "min": 1, "max": 1},
        {"name": "Schleimklumpen",  "type": "junk",         "key": "Schleimklumpen",  "min": 1, "max": 2},
        {"name": "Goblinzahn",      "type": "junk",         "key": "Goblinzahn",      "min": 1, "max": 2},
        {"name": "Wolfspelz",       "type": "junk",         "key": "Wolfspelz",       "min": 1, "max": 2},
        {"name": "Trollfell",       "type": "junk",         "key": "Trollfell",       "min": 1, "max": 1},
        {"name": "Banditen-Abzeichen", "type": "junk",      "key": "Banditen-Abzeichen", "min": 1, "max": 1},
        {"name": "Eisenhelm",            "type": "equipment", "key": "Eisenhelm"},
        {"name": "Langschwert",          "type": "equipment", "key": "Langschwert"},
        {"name": "Kriegshammer",         "type": "equipment", "key": "Kriegshammer"},
        {"name": "Kettenhemd",           "type": "equipment", "key": "Kettenhemd"},
        {"name": "Plattenpanzer",        "type": "equipment", "key": "Plattenpanzer"},
        {"name": "Schnellläuferstiefel", "type": "equipment", "key": "Schnellläuferstiefel"},
        {"name": "Schattendolch",        "type": "equipment", "key": "Schattendolch"},
        {"name": "Schattenstiefel",      "type": "equipment", "key": "Schattenstiefel"},
        {"name": "Kriegsstiefel",        "type": "equipment", "key": "Kriegsstiefel"},
    ],
    # -- RARE
    "rare": [
        {"name": "Gold",            "type": "gold",        "key": "Gold",            "min": 25, "max": 60},
        {"name": "Elixier",         "type": "consumable",  "key": "Elixier",         "min": 1, "max": 1},
        {"name": "Energie-Kristall","type": "consumable",  "key": "Energie-Kristall","min": 1, "max": 2},
        {"name": "Stahlhelm",       "type": "equipment", "key": "Stahlhelm"},
        {"name": "Runenschwert",    "type": "equipment", "key": "Runenschwert"},
        {"name": "Runenrüstung",    "type": "equipment", "key": "Runenrüstung"},
        {"name": "Runenhelm",       "type": "equipment", "key": "Runenhelm"},
        {"name": "Runenstiefel",    "type": "equipment", "key": "Runenstiefel"},
        {"name": "Sturmklinge",     "type": "equipment", "key": "Sturmklinge"},
        {"name": "Schattenrüstung", "type": "equipment", "key": "Schattenrüstung"},
        {"name": "Schattenhelm",    "type": "equipment", "key": "Schattenhelm"},
    ],
    # -- EPIC
    "epic": [
        {"name": "Gold",            "type": "gold",       "key": "Gold",            "min": 60, "max": 120},
        {"name": "Phönixfeder",     "type": "consumable", "key": "Phönixfeder",     "min": 1, "max": 1},
        {"name": "Stärketrank",     "type": "consumable", "key": "Stärketrank",     "min": 1, "max": 2},
        {"name": "Drachenzahn",     "type": "equipment", "key": "Drachenzahn"},
        {"name": "Drachenschuppen", "type": "equipment", "key": "Drachenschuppen"},
        {"name": "Drachenkrone",    "type": "equipment", "key": "Drachenkrone"},
        {"name": "Drachenklauen",   "type": "equipment", "key": "Drachenklauen"},
        {"name": "Knochensense",    "type": "equipment", "key": "Knochensense"},
        # Klassen-Sets (droppen nur für passende Klasse, Filter in apply_loot)
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
    # -- LEGENDARY  (sehr seltener Pool)
    "legendary": [
        {"name": "Gold",                  "type": "gold",       "key": "Gold",                  "min": 150, "max": 300},
        {"name": "Göttliche Klinge",      "type": "equipment",  "key": "Göttliche Klinge"},
        {"name": "Rüstung des Lichts",    "type": "equipment",  "key": "Rüstung des Lichts"},
        {"name": "Krone des Ewigen",      "type": "equipment",  "key": "Krone des Ewigen"},
        {"name": "Stiefel der Ewigkeit",  "type": "equipment",  "key": "Stiefel der Ewigkeit"},
    ],
}

RANK_LOOT_WEIGHTS = {
    1: {"common": 80, "uncommon": 18, "rare": 2,   "epic": 0,  "legendary": 0},
    2: {"common": 65, "uncommon": 28, "rare": 7,   "epic": 0,  "legendary": 0},
    3: {"common": 48, "uncommon": 35, "rare": 15,  "epic": 2,  "legendary": 0},
    4: {"common": 25, "uncommon": 33, "rare": 33,  "epic": 9,  "legendary": 0},
    5: {"common": 8,  "uncommon": 17, "rare": 33,  "epic": 33, "legendary": 9},
}


# ── Zonen-basierte Loot-Pools ────────────────────────────────────────────────

def _e(key, w):  return {"type": "equipment",  "key": key, "weight": w}
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
        _e("Eisaxt",            3),
        _e("Runen-Kriegshammer",2),
        _e("Panzerklinge",      3),
        _e("Runen-Platte",      3),
        _e("Runen-Visier",      2),
        _e("Runen-Schritte",    2),
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
        _e("Festungsklinge",    2),
        _e("Festungsplatte",    2),
        _e("Festungshelm",      2),
        _e("Festungsstiefel",   2),
        _e("Hüllendolch",       2),
        _e("Hüllenpanzer",      2),
        _e("Hüllenmaske",       2),
        _e("Hüllenstiefel",     2),
        _e("Arkaner Stab",      2),
        _e("Arkane Robe",       2),
        _e("Arkane Kapuze",     2),
        _e("Arkane Schuhe",     2),
    ],
    "dunkelreich": [
        _g(14, 80, 150),
        _c("Elixier",           9),
        _c("Phönixfeder",       7),
        _e("Verdammte Klinge",  5),
        _e("Verdammte Rüstung", 5),
        _e("Verdammter Helm",   4),
        _e("Verdammte Stiefel", 4),
        _e("Göttliche Klinge",  2),
        _e("Rüstung des Lichts",2),
        _e("Krone des Ewigen",  2),
        _e("Stiefel der Ewigkeit", 2),
    ],
}

# Boss-Loot: garantierte Set-Teile des NÄCHSTEN Tiers
BOSS_LOOT_POOL = {
    "wald":        ["Kriegshammer", "Plattenpanzer", "Stahlhelm", "Schnellläuferstiefel",
                    "Panzerklinge", "Runen-Platte", "Runen-Visier", "Runen-Schritte"],
    "ruinen":      ["Runenschwert", "Runenrüstung", "Runenhelm", "Runenstiefel",
                    "Mondklinge", "Schattengewand", "Schattenkapuze", "Schattensandale"],
    "wueste":      ["Drachenzahn", "Drachenschuppen", "Drachenkrone", "Drachenklauen",
                    "Schuppenklinge", "Schuppenpanzer", "Schuppenhelm", "Schuppenstiefel"],
    "vulkan":      ["Verdammte Klinge", "Verdammte Rüstung", "Verdammter Helm", "Verdammte Stiefel"],
    "dunkelreich": ["Göttliche Klinge", "Rüstung des Lichts", "Krone des Ewigen", "Stiefel der Ewigkeit"],
}


def roll_zone_loot(zone_id: str, rolls: int = 2) -> list:
    pool    = ZONE_LOOT_POOL.get(zone_id, ZONE_LOOT_POOL["wald"])
    weights = [p["weight"] for p in pool]
    return [random.choices(pool, weights=weights, k=1)[0] for _ in range(rolls)]


def roll_boss_loot(zone_id: str) -> list:
    pool  = BOSS_LOOT_POOL.get(zone_id, [])
    picks = random.sample(pool, min(2, len(pool))) if pool else []
    result = [{"type": "equipment", "key": k} for k in picks]
    gold_ranges = {"wald": (30,60), "ruinen": (50,90), "wueste": (70,120),
                   "vulkan": (100,160), "dunkelreich": (150,250)}
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
            player.inventory["Gold"] = player.inventory.get("Gold", 0) + amount
            messages.append(f"  💰 {amount}x Gold")

        elif item["type"] == "consumable":
            key    = item["key"]
            label  = item.get("name", key)
            amount = random.randint(item.get("min", 1), item.get("max", 1))
            result = player.add_consumable(key, amount)
            cdef   = CONSUMABLE_DEFS.get(key, {})
            emoji  = cdef.get("emoji", "🧪")
            if result > 0:
                messages.append(f"  {emoji} {result}x {label}")
            if result < amount:
                messages.append(f"  ⚠️  {amount-result}x {label} nicht aufgenommen (Stapel voll / Inventar voll)")

        elif item["type"] == "junk":
            key    = item["key"]
            label  = item.get("name", key)
            amount = random.randint(item.get("min", 1), item.get("max", 1))
            result = player.add_junk(key, amount)
            jdef   = JUNK_DEFS.get(key, {})
            emoji  = jdef.get("emoji", "🗑️")
            if result > 0:
                messages.append(f"  {emoji} {result}x {label}")
            if result < amount:
                messages.append(f"  ⚠️  {amount-result}x {label} nicht aufgenommen (Inventar voll)")

        elif item["type"] == "equipment":
            if not player.has_inventory_space():
                messages.append(f"  ⚠️  Inventar voll! {item.get('name', item.get('key', '?'))} verloren.")
                continue
            item_key  = item["key"]
            raw_edef  = EQUIPMENT_DEFS.get(item_key, {})
            class_only = raw_edef.get("class_only")
            if class_only and class_only != getattr(player, "player_class", "warrior"):
                continue  # Falsche Klasse – kein Drop
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
            if rarity == "legendary":
                from systems.achievements import check_and_unlock
                msg = check_and_unlock(player, "got_legendary")
                if msg:
                    messages.append(f"  {msg}")

    return messages
