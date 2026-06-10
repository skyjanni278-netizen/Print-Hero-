from enum import Enum


class Zone(str, Enum):
    WALD        = "wald"
    RUINEN      = "ruinen"
    WUESTE      = "wueste"
    VULKAN      = "vulkan"
    DUNKELREICH = "dunkelreich"


DIFFICULTY_SETTINGS = {
    "easy":   {"hp_mult": 0.80, "atk_mult": 0.85, "start_hp": 35, "label": "Einfach  🟢"},
    "normal": {"hp_mult": 1.00, "atk_mult": 1.00, "start_hp": 30, "label": "Normal   🟡"},
    "hard":   {"hp_mult": 1.25, "atk_mult": 1.20, "start_hp": 25, "label": "Schwer   🔴"},
}

# Inventar
MAX_INVENTORY_SLOTS = 30

# Kampf-Konstanten
BLEED_DAMAGE   = 3   # HP-Schaden pro Blutungs-Stack pro Runde
POISON_DAMAGE  = 5   # HP-Schaden pro Gift-Stack pro Runde
BURN_DAMAGE    = 4   # HP-Schaden pro Verbrennungs-Stack pro Runde
ENERGY_REGEN   = 3   # Energie-Regeneration pro Runde

# Level-Up-Konstanten
LEVEL_HP_GAIN  = 4   # max HP pro Level-Up
LEVEL_ATK_GAIN = 1   # ATK pro Level-Up

# Roguelite-Basis-Balancing: gilt für ALLE Gegner zusätzlich zur Schwierigkeit
ENEMY_BASE_HP_MULT  = 1.20
ENEMY_BASE_ATK_MULT = 1.15

# Runenessenz — permanente Metawährung (wird auch bei Tod nicht verloren)
RUNENESSENZ_DUNGEON = (15, 25)   # pro abgeschlossenem Dungeon
RUNENESSENZ_BOSS    = (50, 80)   # pro besiegtem Zonen-Boss
RUNENESSENZ_VICTORY = 200        # Bonus bei Sieg (alle 5 Zonen-Bosse)

# XP-Multiplikatoren je Level: Lvl 1→2: 30 XP (~1 Kampf), danach exponentiell
XP_MULTIPLIERS = {1: 2.0, 2: 1.85, 3: 1.75, 4: 1.7, 5: 1.65, 6: 1.6, 7: 1.55, 8: 1.5, 9: 1.5}
