from ui.utils import clear_screen, print_header, console

# 4 Fähigkeiten pro Klasse: S(LV1), R(LV1), C(LV3), X(LV5)
# cd=0 → kein Cooldown, cd=N → N Runden, cd=99 → 1× pro Kampf
CLASS_ABILITY_DEFS = {
    "warrior": {
        "S": {"name": "Brutaler Hieb",  "energy": 18, "cd": 0,  "unlock": 1, "needs_target": True,
              "desc": "Kraftvoller Angriff. +6 Schaden, 30% der DEF ignoriert."},
        "R": {"name": "Schildwall",     "energy": 10, "cd": 0,  "unlock": 1, "needs_target": False,
              "desc": "Blockt den nächsten eingehenden Angriff vollständig."},
        "C": {"name": "Schildstoß",     "energy": 20, "cd": 3,  "unlock": 3, "needs_target": True,
              "desc": "Angriff + 50% Betäubungs-Chance. (3 Runden Abklingzeit)"},
        "X": {"name": "Kriegsschrei",   "energy": 25, "cd": 99, "unlock": 5, "needs_target": False,
              "desc": "+5 ATK für den gesamten Kampf. (1× pro Kampf)"},
    },
    "rogue": {
        "S": {"name": "Aus dem Schatten", "energy": 15, "cd": 0,  "unlock": 1, "needs_target": False,
              "desc": "Nächster Angriff: garantierter Krit + ignoriert DEF komplett."},
        "R": {"name": "Giftklinge",       "energy": 12, "cd": 0,  "unlock": 1, "needs_target": True,
              "desc": "Angriff + 3 Giftstacks garantiert auf das Ziel."},
        "C": {"name": "Blendpulver",      "energy": 20, "cd": 4,  "unlock": 3, "needs_target": True,
              "desc": "Gegner verfehlt seine nächsten 2 Angriffe. (4 Runden CD)"},
        "X": {"name": "Rauchbombe",       "energy": 10, "cd": 99, "unlock": 5, "needs_target": False,
              "desc": "Garantierter Rückzug aus dem Kampf. (1× pro Kampf)"},
    },
    "mage": {
        "S": {"name": "Arkane Entladung", "energy": 15, "cd": 0,  "unlock": 1, "needs_target": False,
              "desc": "Trifft alle Gegner mit magischem Schaden (ignoriert DEF). Skaliert mit Level."},
        "R": {"name": "Froststrahl",      "energy": 18, "cd": 0,  "unlock": 1, "needs_target": True,
              "desc": "Eisschaden ignoriert DEF — Gegner ist 1 Runde eingefroren."},
        "C": {"name": "Feuerball",        "energy": 22, "cd": 3,  "unlock": 3, "needs_target": True,
              "desc": "Starker Feuerangriff + 3 Verbrennungsstacks. (3 Runden CD)"},
        "X": {"name": "Mana-Schild",      "energy":  0, "cd": 4,  "unlock": 5, "needs_target": False,
              "desc": "Absorbiert nächsten Angriff mit Energie statt HP. (4 Runden CD)"},
    },
}

CLASS_DEFS = {
    "warrior": {
        "name":        "Krieger",
        "emoji":       "⚔️",
        "start_hp":    40,
        "start_atk":   12,
        "start_energy":25,
        "armor":        2,
        "desc":        "Zäher Kämpfer mit hoher Rüstung",
        "bonus_desc":  "+5 DEF, startet mit Kettenhemd",
        "ability_name":"Schildwall",
        "ability_desc":"Nächsten eingehenden Angriff vollständig blocken",
        "start_item":  {"name": "Kettenhemd", "armor": 5, "type": "chest"},
    },
    "mage": {
        "name":        "Magier",
        "emoji":       "🔮",
        "start_hp":    25,
        "start_atk":    8,
        "start_energy":45,
        "armor":        0,
        "desc":        "Hohe Energie, günstige Spezialfähigkeiten",
        "bonus_desc":  "Energie-Regen +3/Runde, Spezialfähigkeiten -5 Energie",
        "ability_name":"Arkane Entladung",
        "ability_desc":"Magischer Schaden an ALLE Gegner, ignoriert DEF, skaliert mit Level",
        "start_item":   None,
    },
    "rogue": {
        "name":        "Schurke",
        "emoji":       "🗡️",
        "start_hp":    30,
        "start_atk":   15,
        "start_energy":30,
        "armor":        0,
        "desc":        "Hoher Angriff, Flucht fast immer erfolgreich",
        "bonus_desc":  "Flieh-Chance 70%, Krit-Chance +10%",
        "ability_name":"Aus dem Schatten",
        "ability_desc":"Nächster Angriff: automatischer Krit + ignoriert DEF",
        "start_item":   None,
    },
}


def choose_class() -> str:
    clear_screen()
    print_header("Klasse wählen")
    entries = list(CLASS_DEFS.items())
    for i, (cid, c) in enumerate(entries):
        console.print(f"  [[{i+1}]] [bold]{c['emoji']}  {c['name']:<12}[/bold] — [dim]{c['desc']}[/dim]")
        console.print(f"       [cyan]Bonus:[/cyan]     {c['bonus_desc']}")
        console.print(f"       [yellow]Fähigkeit:[/yellow] {c['ability_name']} — [dim]{c['ability_desc']}[/dim]")
        console.print()
    while True:
        ch = input("Deine Wahl [1/2/3]: ").strip()
        if ch.isdigit() and 1 <= int(ch) <= len(entries):
            return entries[int(ch) - 1][0]


def apply_class(player, class_id: str):
    from content.loot_tables import EQUIPMENT_DEFS
    c = CLASS_DEFS.get(class_id)
    if not c:
        return
    player.player_class        = class_id
    player.max_hp              = c["start_hp"]
    player.hp                  = c["start_hp"]
    player.attack              = c["start_atk"]
    player.min_attack          = 1
    player.max_energy          = c["start_energy"]
    player.energy              = c["start_energy"] // 2
    player.armor               = c["armor"]
    player.ability_cooldowns   = {"S": 0, "R": 0, "C": 0, "X": 0}
    player.shadow_strike_ready = False
    player.block_next          = False
    player.mana_shield_active  = False

    # Startitem anlegen (Krieger bekommt Kettenhemd)
    if c["start_item"]:
        item = dict(c["start_item"])
        player.equipment["chest"] = item
