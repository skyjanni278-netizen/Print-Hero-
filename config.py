DIFFICULTY_SETTINGS = {
    "easy":   {"hp_mult": 0.80, "atk_mult": 0.85, "start_hp": 35, "label": "Einfach  🟢"},
    "normal": {"hp_mult": 1.00, "atk_mult": 1.00, "start_hp": 30, "label": "Normal   🟡"},
    "hard":   {"hp_mult": 1.25, "atk_mult": 1.20, "start_hp": 25, "label": "Schwer   🔴"},
}

# Kampf-Konstanten
BLEED_DAMAGE   = 3   # HP-Schaden pro Blutungs-Stack pro Runde
POISON_DAMAGE  = 5   # HP-Schaden pro Gift-Stack pro Runde
ENERGY_REGEN   = 3   # Energie-Regeneration pro Runde

# Level-Up-Konstanten
LEVEL_HP_GAIN  = 4   # max HP pro Level-Up
LEVEL_ATK_GAIN = 1   # ATK pro Level-Up
