from ui.utils import clear_screen, print_header

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
    "ng_plus":        {"name": "Zweite Runde",      "emoji": "⭐", "desc": "New Game+ gestartet"},
}

_ZONE_ACH = {
    "wald":        "wald_cleared",
    "ruinen":      "ruinen_cleared",
    "wueste":      "wueste_cleared",
    "vulkan":      "vulkan_cleared",
    "dunkelreich": "dunkel_cleared",
}


def check_and_unlock(player, achievement_id: str) -> str | None:
    if not hasattr(player, "achievements"):
        player.achievements = set()
    if achievement_id not in player.achievements and achievement_id in ACHIEVEMENTS:
        player.achievements.add(achievement_id)
        a = ACHIEVEMENTS[achievement_id]
        return f"🏆 Errungenschaft freigeschaltet: {a['emoji']} {a['name']} — {a['desc']}"
    return None


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
        enemies     = context.get("enemies", [])
        potions_in  = context.get("potions_before", 0)
        potions_out = context.get("potions_after", 0)

        if kills >= 1:    _try("first_blood")
        if kills >= 10:   _try("slayer_10")
        if kills >= 100:  _try("slayer_100")
        if fights >= 50:  _try("fighter_50")
        if potions_in == potions_out:
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

    elif event == "gold_check":
        if gold >= 500:
            _try("wealthy")

    elif event == "ng_plus":
        _try("ng_plus")

    elif event == "dungeon_complete":
        dc      = player.stats.get("dungeons_completed", 0)
        cleared = player.stats.get("zones_cleared", [])
        zone_id = context.get("zone_id", "")
        if dc >= 10:
            _try("dungeon_veteran")
        ach = _ZONE_ACH.get(zone_id)
        if ach and zone_id in cleared:
            _try(ach)

    return msgs


def achievements_menu(player):
    if not hasattr(player, "achievements"):
        player.achievements = set()
    clear_screen()
    print_header("Errungenschaften")
    unlocked = len(player.achievements)
    total    = len(ACHIEVEMENTS)
    print(f"Freigeschaltet: {unlocked}/{total}\n")

    sections = [
        ("⚔️  Kampf",            ["first_blood", "slayer_10", "slayer_100", "fighter_50", "no_potions", "boss_slayer"]),
        ("📈 Aufstieg",          ["reach_lv5", "reach_lv10", "warrior_legend", "rogue_master", "mage_sage"]),
        ("🗡️  Dungeons & Zonen", ["dungeon_veteran", "wald_cleared", "ruinen_cleared", "wueste_cleared", "vulkan_cleared", "dunkel_cleared"]),
        ("💰 Wirtschaft",        ["wealthy", "got_legendary"]),
        ("⭐ Meta",              ["ng_plus"]),
    ]
    for section_name, ids in sections:
        print(f"\n{section_name}")
        for aid in ids:
            if aid not in ACHIEVEMENTS:
                continue
            a      = ACHIEVEMENTS[aid]
            status = "✅" if aid in player.achievements else "🔒"
            print(f"  {status} {a['emoji']} {a['name']:<22} — {a['desc']}")
    input("\n(ENTER)")
