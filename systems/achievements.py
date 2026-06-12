from ui.utils import clear_screen, print_header, console

ACHIEVEMENTS = {
    # ── Kampf ──────────────────────────────────────────────────
    "first_blood":    {"name": "Erste Blut",       "emoji": "🩸", "desc": "Ersten Gegner besiegt"},
    "slayer_10":      {"name": "Schlächter",        "emoji": "⚔️", "desc": "10 Gegner besiegt"},
    "slayer_100":     {"name": "Massenmörder",      "emoji": "💀", "desc": "100 Gegner besiegt"},
    "fighter_50":     {"name": "Schlachtveteran",   "emoji": "🛡️", "desc": "50 Kämpfe gewonnen"},
    "no_potions":     {"name": "Harter Bursche",    "emoji": "🧱", "desc": "Kampf ohne Heiltrank gewonnen"},
    "boss_slayer":    {"name": "Monsterjäger",      "emoji": "🔥", "desc": "Rang-5-Boss besiegt"},
    # ── Aufstieg ───────────────────────────────────────────────
    "reach_lv5":      {"name": "Aufstieg",          "emoji": "📈", "desc": "Level 5 erreicht"},
    "reach_lv10":     {"name": "Legende",           "emoji": "👑", "desc": "Level 10 erreicht"},
    "warrior_legend": {"name": "Krieger-Legende",   "emoji": "⚔️", "desc": "Level 10 als Krieger erreicht"},
    "rogue_master":   {"name": "Schatten-Meister",  "emoji": "🌙", "desc": "Level 10 als Schurke erreicht"},
    "mage_sage":      {"name": "Arkan-Weiser",      "emoji": "🔮", "desc": "Level 10 als Magier erreicht"},
    # ── Dungeons & Zonen ───────────────────────────────────────
    "dungeon_veteran":{"name": "Dungeon-Veteran",   "emoji": "🗡️", "desc": "10 Dungeons abgeschlossen"},
    "wald_cleared":   {"name": "Waldbezwinger",     "emoji": "🌲", "desc": "Wald-Dungeon abgeschlossen"},
    "ruinen_cleared": {"name": "Ruinenspringer",    "emoji": "🏚️", "desc": "Ruinen-Dungeon abgeschlossen"},
    "wueste_cleared": {"name": "Wüstenfuchs",       "emoji": "🏜️", "desc": "Wüsten-Dungeon abgeschlossen"},
    "vulkan_cleared": {"name": "Vulkanläufer",      "emoji": "🌋", "desc": "Vulkan-Dungeon abgeschlossen"},
    "dunkel_cleared": {"name": "Dunkelherrscher",   "emoji": "💀", "desc": "Dunkel-Reich-Dungeon abgeschlossen"},
    # ── Wirtschaft ─────────────────────────────────────────────
    "wealthy":        {"name": "Goldgräber",        "emoji": "💰", "desc": "500 Gold gleichzeitig besessen"},
    "got_legendary":  {"name": "Legendär",          "emoji": "🟨", "desc": "Legendäres Item gefunden"},
    # ── Meta ───────────────────────────────────────────────────
    "run_won":        {"name": "Bezwinger",         "emoji": "⭐", "desc": "Einen Run siegreich abgeschlossen"},
    # ── Roguelite (v3.2) ───────────────────────────────────────
    "erster_schritt": {"name": "Erster Schritt",    "emoji": "👣", "desc": "5 Runs abgeschlossen"},
    "spiegel_meister":{"name": "Spiegel-Meister",   "emoji": "🪞", "desc": "Alle Spiegel-Upgrades freigeschaltet"},
    "rune_sammler":   {"name": "Runen-Sammler",     "emoji": "🧿", "desc": "Alle Runen gefunden"},
    "synergist":      {"name": "Synergist",         "emoji": "🔗", "desc": "2 Segnung-Synergien gleichzeitig aktiv"},
    "unberuehrt":     {"name": "Unberührt",         "emoji": "💨", "desc": "Dungeon ohne erlittenen Schaden abgeschlossen"},
    "todesveraechter":{"name": "Todesverächter",    "emoji": "⚰️", "desc": "Zweites Leben genutzt und Run dennoch gewonnen"},
    "gilden_gruender":{"name": "Gilden-Gründer",    "emoji": "🏕️", "desc": "Alle Zuflucht-NPCs freigeschaltet"},
    "got_mythic":     {"name": "Mythisch",          "emoji": "🟥", "desc": "Mythic-Item gefunden"},
    "ewige_legende":  {"name": "Ewige Legende",     "emoji": "🏅", "desc": "Mit allen 3 Klassen einen Run gewonnen"},
    "verdammter_held":{"name": "Verdammter Held",   "emoji": "😈", "desc": "Run mit allen 3 Dunkelsiegeln gewonnen"},
}

_ZONE_ACH = {
    "wald":        "wald_cleared",
    "ruinen":      "ruinen_cleared",
    "wueste":      "wueste_cleared",
    "vulkan":      "vulkan_cleared",
    "dunkelreich": "dunkel_cleared",
}


def _unlock_msg(achievement_id: str) -> str:
    a = ACHIEVEMENTS[achievement_id]
    return f"🏆 Errungenschaft freigeschaltet: {a['emoji']} {a['name']} — {a['desc']}"


def check_and_unlock(player, achievement_id: str) -> str | None:
    if not hasattr(player, "achievements"):
        player.achievements = set()
    if achievement_id not in player.achievements and achievement_id in ACHIEVEMENTS:
        player.achievements.add(achievement_id)
        return _unlock_msg(achievement_id)
    return None


def check_and_unlock_meta(meta: dict, achievement_id: str) -> str | None:
    unlocked = set(meta.get("achievements", []))
    if achievement_id in unlocked or achievement_id not in ACHIEVEMENTS:
        return None
    unlocked.add(achievement_id)
    meta["achievements"] = sorted(unlocked)
    return _unlock_msg(achievement_id)


# Achievements aus dem Meta-Stand (ohne laufenden Run prüfbar) —
# aufrufen wo sich Meta ändert: Spiegel-Kauf, Runen-Drop, Run-Ende.
def check_meta(meta: dict) -> list:
    from systems.spiegel import SPIEGEL_DEFS
    from systems.runen import RUNEN_DEFS
    msgs = []

    def _try(aid):
        m = check_and_unlock_meta(meta, aid)
        if m:
            msgs.append(m)

    ls      = meta.get("lifetime_stats", {})
    spiegel = meta.get("spiegel_state", {})
    runen   = set(meta.get("unlocked_runen", []))

    if ls.get("runs_won", 0) + ls.get("runs_lost", 0) >= 5:
        _try("erster_schritt")
    if all(spiegel.get(uid) in ("A", "B") for uid in SPIEGEL_DEFS):
        _try("spiegel_meister")
    if runen >= set(RUNEN_DEFS):
        _try("rune_sammler")
    if all(rid in runen for rid, d in RUNEN_DEFS.items() if d["kategorie"] == "npc"):
        _try("gilden_gruender")
    if {"warrior", "rogue", "mage"} <= set(ls.get("classes_won", [])):
        _try("ewige_legende")

    if msgs:
        from core.save import save_meta
        save_meta(meta)
    return msgs


def check_all(player, context: dict):
    msgs = []

    def _try(aid):
        m = check_and_unlock(player, aid)
        if m:
            msgs.append(m)

    kills  = player.stats.get("kills", 0)
    fights = player.stats.get("fights", 0)
    gold   = player.inventory.get("Gold", 0)
    event  = context.get("event", "")

    if event == "victory":
        enemies      = context.get("enemies", [])
        potions_used = context.get("potions_used", -1)

        if kills >= 1:    _try("first_blood")
        if kills >= 10:   _try("slayer_10")
        if kills >= 100:  _try("slayer_100")
        if fights >= 50:  _try("fighter_50")
        if potions_used == 0:
            _try("no_potions")
        if any(getattr(e, "rank", 1) == 5 for e in enemies):
            _try("boss_slayer")

    elif event == "level_up":
        lvl    = context.get("level", 1)
        pclass = getattr(player, "player_class", "warrior")
        if lvl >= 5:  _try("reach_lv5")
        if lvl >= 10:
            _try("reach_lv10")
            if pclass == "warrior": _try("warrior_legend")
            elif pclass == "rogue": _try("rogue_master")
            elif pclass == "mage":  _try("mage_sage")

    elif event == "loot":
        if context.get("got_legendary"):
            _try("got_legendary")
        if context.get("got_mythic"):
            _try("got_mythic")

    elif event == "gold_check":
        if gold >= 500:
            _try("wealthy")

    elif event == "run_won":
        _try("run_won")
        if getattr(player, "spiegel_leben_used", False):
            _try("todesveraechter")
        from systems.dunkelsiegel import SIEGEL_DEFS
        if set(SIEGEL_DEFS) <= set(getattr(player, "aktive_siegel", [])):
            _try("verdammter_held")

    elif event == "dungeon_complete":
        dc      = player.stats.get("dungeons_completed", 0)
        cleared = player.stats.get("zones_cleared", [])
        zone_id = context.get("zone_id", "")
        if dc >= 10:
            _try("dungeon_veteran")
        ach = _ZONE_ACH.get(zone_id)
        if ach and zone_id in cleared:
            _try(ach)
        if context.get("dungeon_damage", -1) == 0:
            _try("unberuehrt")

    elif event == "segnung":
        from systems.segnungen import get_active_synergien
        if len(get_active_synergien(player)) >= 2:
            _try("synergist")

    return msgs


def achievements_menu(unlocked: set):
    clear_screen()
    print_header("Errungenschaften")
    total = len(ACHIEVEMENTS)
    console.print(f"  Freigeschaltet: [bold cyan]{len(unlocked)}/{total}[/bold cyan]\n")

    sections = [
        ("⚔️  Kampf",            ["first_blood", "slayer_10", "slayer_100", "fighter_50", "no_potions", "boss_slayer"]),
        ("📈 Aufstieg",          ["reach_lv5", "reach_lv10", "warrior_legend", "rogue_master", "mage_sage"]),
        ("🗡️  Dungeons & Zonen", ["dungeon_veteran", "wald_cleared", "ruinen_cleared", "wueste_cleared", "vulkan_cleared", "dunkel_cleared"]),
        ("💰 Wirtschaft",        ["wealthy", "got_legendary", "got_mythic"]),
        ("⭐ Meta",              ["run_won", "erster_schritt", "ewige_legende", "todesveraechter", "verdammter_held"]),
        ("🌀 Roguelite",         ["spiegel_meister", "rune_sammler", "gilden_gruender", "synergist", "unberuehrt"]),
    ]
    for section_name, ids in sections:
        console.print(f"\n  [bold]{section_name}[/bold]")
        for aid in ids:
            if aid not in ACHIEVEMENTS:
                continue
            a = ACHIEVEMENTS[aid]
            if aid in unlocked:
                console.print(f"  [green]✅ {a['emoji']} {a['name']:<22}[/green] — {a['desc']}")
            else:
                console.print(f"  [dim]🔒 {a['emoji']} {a['name']:<22} — {a['desc']}[/dim]")
    input("\n(ENTER)")
