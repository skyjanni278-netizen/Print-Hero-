import random
from rich.markup import escape as _esc

# ── Runen (permanente Unlocks, Dead-Cells-Blueprints) ─────────────────────────
# Rune-IDs sind Keys in meta["unlocked_runen"] — umbenennen bricht Spielstände.

RUNEN_DEFS = {
    "kriegers_vermaechtnis": {"name": "Kriegers Vermächtnis", "emoji": "🪓", "kategorie": "startkit", "class": "warrior",
                              "desc": "Startkit: Streitaxt + Kettenhemd + 60 Gold"},
    "schurken_einsteiger":   {"name": "Schurken-Einsteiger",  "emoji": "🗡️", "kategorie": "startkit", "class": "rogue",
                              "desc": "Startkit: Giftklaue + 2× Antidot + 30 Gold"},
    "magier_erbe":           {"name": "Magier-Erbe",          "emoji": "🪄", "kategorie": "startkit", "class": "mage",
                              "desc": "Startkit: Novizenstab + volle Energie + 1 Stärketrank"},
    "ueberlebender":         {"name": "Überlebender",         "emoji": "🎒", "kategorie": "startkit", "class": None,
                              "desc": "Startkit: 3× Healing Potion + 1× Phönixfeder + 80 Gold"},
    "berserker_erbe":        {"name": "Berserker-Erbe",       "emoji": "💢", "kategorie": "variante", "class": "warrior",
                              "desc": "Krieger-Variante: −10 max HP, +6 ATK, kein Schildwall"},
    "meuchler_erbe":         {"name": "Meuchler-Erbe",        "emoji": "🌘", "kategorie": "variante", "class": "rogue",
                              "desc": "Schurken-Variante: 15 HP, 18 ATK, Flucht gelingt immer"},
    "schmiedegeheimnis":     {"name": "Schmiedegeheimnis",    "emoji": "🔨", "kategorie": "npc", "class": None,
                              "desc": "Schmied: 1 kostenloses Equipment-Upgrade pro Run"},
    "haendlernetzwerk":      {"name": "Händlernetzwerk",      "emoji": "🧺", "kategorie": "npc", "class": None,
                              "desc": "Händlerin: Verbrauchsgüter vor Run-Start für Runenessenz kaufen"},
    "orakelwissen":          {"name": "Orakelwissen",         "emoji": "🔮", "kategorie": "npc", "class": None,
                              "desc": "Orakel in der Zuflucht: zeigt die Werte des nächsten Zonen-Bosses"},
}

KATEGORIE_LABELS = {
    "startkit": "🎒 Startkits",
    "variante": "🧬 Klassen-Varianten",
    "npc":      "🏕️ Zuflucht-NPCs",
}

RUNE_DROP_CHANCES = {
    "zone_boss":    1.00,
    "dungeon_boss": 0.25,
    "elite":        0.05,
    "chest":        0.15,
    "grave":        0.15,
}


# ── Unlock & Drop ─────────────────────────────────────────────────────────────

def rune_unlocked(meta, rid: str) -> bool:
    return rid in meta.get("unlocked_runen", [])


def get_locked_runen(meta) -> list:
    unlocked = set(meta.get("unlocked_runen", []))
    return [rid for rid in RUNEN_DEFS if rid not in unlocked]


def check_rune_drop(meta, source: str, zone_id: str = None):
    locked = get_locked_runen(meta)
    if not locked:
        return None
    if source == "zone_boss" and zone_id in meta.get("boss_runen_dropped", []):
        return None
    if random.random() >= RUNE_DROP_CHANCES.get(source, 0):
        return None
    rid = random.choice(locked)
    meta.setdefault("unlocked_runen", []).append(rid)
    if source == "zone_boss":
        meta.setdefault("boss_runen_dropped", []).append(zone_id)
    from core.save import save_meta
    save_meta(meta)
    return rid


def rune_found_msgs(rid: str) -> list:
    d = RUNEN_DEFS[rid]
    return [
        f"[bold magenta]🧿 RUNE GEFUNDEN: {d['emoji']} {_esc(d['name'])}![/bold magenta]",
        f"[magenta]{_esc(d['desc'])}[/magenta]",
        "[dim]Dauerhaft freigeschaltet — Übersicht in der Zuflucht unter [[R]].[/dim]",
    ]


# ── Klassen-Varianten ─────────────────────────────────────────────────────────

def apply_klassen_variante(player, variante: str) -> list:
    if variante == "berserker":
        player.class_variant = "berserker"
        player.max_hp = max(1, player.max_hp - 10)
        player.hp     = player.max_hp
        player.attack += 6
        return ["💢 Berserker-Erbe: −10 max HP, +6 ATK — Schildwall steht dir nicht zur Verfügung!"]
    if variante == "meuchler":
        player.class_variant = "meuchler"
        player.max_hp = 15
        player.hp     = 15
        player.attack = 18
        return ["🌘 Meuchler-Erbe: 15 HP, 18 ATK — Flucht gelingt immer!"]
    return []


# ── Startkits ─────────────────────────────────────────────────────────────────

def apply_startkit(player, rid: str) -> list:
    from content.items import EQUIPMENT_DEFS
    msgs = []

    def _equip_weapon(key):
        edef = EQUIPMENT_DEFS[key]
        player.equipment["weapon"] = {"name": key, "attack": edef["attack"], "type": "weapon"}
        msgs.append(f"{edef.get('emoji','⚔️')} {key} ausgerüstet (ATK +{edef['attack']})")

    if rid == "kriegers_vermaechtnis":
        _equip_weapon("Streitaxt")
        chest = EQUIPMENT_DEFS["Kettenhemd"]
        player.equipment["chest"] = {"name": "Kettenhemd", "armor": chest["armor"], "type": "chest"}
        msgs.append(f"{chest.get('emoji','🛡️')} Kettenhemd ausgerüstet (DEF +{chest['armor']})")
        player.inventory["Gold"] += 60
        msgs.append("💰 +60 Gold")
    elif rid == "schurken_einsteiger":
        _equip_weapon("Giftklaue")
        player.add_consumable("Antidot", 2)
        msgs.append("🧪 2× Antidot")
        player.inventory["Gold"] += 30
        msgs.append("💰 +30 Gold")
    elif rid == "magier_erbe":
        _equip_weapon("Novizenstab")
        player.energy = player.get_effective_max_energy()
        msgs.append("⚡ Energie vollständig gefüllt")
        player.add_consumable("Stärketrank", 1)
        msgs.append("🧪 1× Stärketrank")
    elif rid == "ueberlebender":
        player.add_consumable("Healing Potion", 3)
        msgs.append("🧪 3× Healing Potion")
        player.add_consumable("Phönixfeder", 1)
        msgs.append("🪶 1× Phönixfeder")
        player.inventory["Gold"] += 80
        msgs.append("💰 +80 Gold")
    return msgs


def available_startkits(meta, class_id: str) -> list:
    kits = []
    for rid, d in RUNEN_DEFS.items():
        if d["kategorie"] != "startkit" or not rune_unlocked(meta, rid):
            continue
        if d["class"] is None or d["class"] == class_id:
            kits.append(rid)
    return kits
