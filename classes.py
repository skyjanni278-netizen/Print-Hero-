from utils import clear_screen, print_header

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
        "ability_desc":"25–40 Schaden an ALLE Gegner, ignoriert DEF",
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
        print(f"  [{i+1}] {c['emoji']}  {c['name']:<12} — {c['desc']}")
        print(f"       Bonus:    {c['bonus_desc']}")
        print(f"       Fähigkeit: {c['ability_name']} — {c['ability_desc']}")
        print()
    while True:
        ch = input("Deine Wahl [1/2/3]: ").strip()
        if ch.isdigit() and 1 <= int(ch) <= len(entries):
            return entries[int(ch) - 1][0]


def apply_class(player, class_id: str):
    from loot_tables import EQUIPMENT_DEFS
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
    player.class_ability_used  = False
    player.shadow_strike_ready = False
    player.block_next          = False

    # Startitem anlegen (Krieger bekommt Kettenhemd)
    if c["start_item"]:
        item = dict(c["start_item"])
        player.equipment["chest"] = item
