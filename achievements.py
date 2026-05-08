from utils import clear_screen, print_header

ACHIEVEMENTS = {
    "first_blood":   {"name": "Erste Blut",      "emoji": "🩸", "desc": "Ersten Gegner besiegt"},
    "slayer_10":     {"name": "Schlächter",       "emoji": "⚔️", "desc": "10 Gegner besiegt"},
    "slayer_100":    {"name": "Massenmörder",     "emoji": "💀", "desc": "100 Gegner besiegt"},
    "reach_lv5":     {"name": "Aufstieg",         "emoji": "📈", "desc": "Level 5 erreicht"},
    "reach_lv10":    {"name": "Legende",          "emoji": "👑", "desc": "Level 10 erreicht"},
    "wealthy":       {"name": "Goldgräber",       "emoji": "💰", "desc": "500 Gold gleichzeitig besessen"},
    "no_potions":    {"name": "Harter Bursche",   "emoji": "🧱", "desc": "Kampf ohne Heiltrank gewonnen"},
    "boss_slayer":   {"name": "Monsterjäger",     "emoji": "🔥", "desc": "Rang-5-Boss besiegt"},
    "got_legendary": {"name": "Legendär",         "emoji": "🟨", "desc": "Legendäres Item gefunden"},
    "ng_plus":       {"name": "Zweite Runde",     "emoji": "⭐", "desc": "New Game+ gestartet"},
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

    kills = player.stats.get("kills", 0)
    gold  = player.inventory.get("Gold", 0)
    event = context.get("event", "")

    if event == "victory":
        enemies    = context.get("enemies", [])
        potions_in = context.get("potions_before", 0)
        potions_out= context.get("potions_after", 0)

        if kills >= 1:
            _try("first_blood")
        if kills >= 10:
            _try("slayer_10")
        if kills >= 100:
            _try("slayer_100")
        if potions_in == potions_out:
            _try("no_potions")
        if any(getattr(e, "rank", 1) == 5 for e in enemies):
            _try("boss_slayer")

    elif event == "level_up":
        lvl = context.get("level", 1)
        if lvl >= 5:
            _try("reach_lv5")
        if lvl >= 10:
            _try("reach_lv10")

    elif event == "loot":
        if context.get("got_legendary"):
            _try("got_legendary")

    elif event == "gold_check":
        if gold >= 500:
            _try("wealthy")

    elif event == "ng_plus":
        _try("ng_plus")

    return msgs


def achievements_menu(player):
    if not hasattr(player, "achievements"):
        player.achievements = set()
    clear_screen()
    print_header("Errungenschaften")
    unlocked = len(player.achievements)
    total    = len(ACHIEVEMENTS)
    print(f"Freigeschaltet: {unlocked}/{total}\n")
    for aid, a in ACHIEVEMENTS.items():
        status = "✅" if aid in player.achievements else "🔒"
        print(f"  {status} {a['emoji']} {a['name']:<22} — {a['desc']}")
    input("\n(ENTER)")
