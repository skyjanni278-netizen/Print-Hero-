from utils import clear_screen, print_header

SKILL_TREE = {
    # Kampf-Baum
    "Scharfe Klingen":    {"tree": "Kampf",     "tier": 1, "cost": 1, "requires": None,               "desc": "ATK dauerhaft +2"},
    "Kritischer Treffer": {"tree": "Kampf",     "tier": 2, "cost": 2, "requires": "Scharfe Klingen",  "desc": "15% Chance auf Doppelschaden"},
    "Blutgier":           {"tree": "Kampf",     "tier": 3, "cost": 3, "requires": "Kritischer Treffer","desc": "20% Lifesteal bei jedem Angriff"},
    # Ueberleben-Baum
    "Eisenhaut":          {"tree": "Ueberleben","tier": 1, "cost": 1, "requires": None,               "desc": "DEF dauerhaft +3"},
    "Zaehigkeit":         {"tree": "Ueberleben","tier": 2, "cost": 2, "requires": "Eisenhaut",        "desc": "Max-HP +10"},
    "Regeneration":       {"tree": "Ueberleben","tier": 3, "cost": 3, "requires": "Zaehigkeit",       "desc": "+1 HP-Regen pro Runde"},
    # Energie-Baum
    "Energiefluss":       {"tree": "Energie",   "tier": 1, "cost": 1, "requires": None,               "desc": "Energie-Regen +2 pro Runde"},
    "Fokus":              {"tree": "Energie",   "tier": 2, "cost": 2, "requires": "Energiefluss",     "desc": "Spezialfaehigkeiten -5 Energie"},
    "Magieschild":        {"tree": "Energie",   "tier": 3, "cost": 3, "requires": "Fokus",            "desc": "Einmal pro Kampf: naechsten Angriff blocken"},
}

_TREE_ORDER = {
    "Kampf":      ["Scharfe Klingen", "Kritischer Treffer", "Blutgier"],
    "Ueberleben": ["Eisenhaut",       "Zaehigkeit",          "Regeneration"],
    "Energie":    ["Energiefluss",    "Fokus",               "Magieschild"],
}

_TIER_LABEL = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3"}


def _can_unlock(player, skill_name: str) -> tuple[bool, str]:
    sdef = SKILL_TREE[skill_name]
    if skill_name in player.skills:
        return False, "bereits gelernt"
    req = sdef["requires"]
    if req and req not in player.skills:
        return False, f"benoetigt: {req}"
    if player.skill_points < sdef["cost"]:
        return False, f"zu wenig Punkte ({player.skill_points}/{sdef['cost']})"
    return True, ""


def skill_menu(player):
    while True:
        clear_screen()
        print_header("Skill-Baum")
        print(f"Verfuegbare Skillpunkte: {player.skill_points}")
        print(f"Gelernte Skills: {len(player.skills)}/9\n")

        rows = []
        idx = 0
        for tree_name, skills in _TREE_ORDER.items():
            print(f"── {tree_name}-Baum " + "─" * (28 - len(tree_name)))
            for skill_name in skills:
                sdef = SKILL_TREE[skill_name]
                unlocked = skill_name in player.skills
                can, reason = _can_unlock(player, skill_name)

                if unlocked:
                    marker = "✅"
                    hint   = ""
                elif can:
                    marker = f"[{idx}]"
                    hint   = f"  ({sdef['cost']} Pkt)"
                else:
                    marker = "🔒"
                    hint   = f"  ({reason})"

                tier = _TIER_LABEL[sdef["tier"]]
                print(f"  {marker:<5} {skill_name:<22} — {sdef['desc']:<38} [{tier}]{hint}")
                if can:
                    rows.append(skill_name)
                    idx += 1
            print()

        if not rows:
            print("Keine Skills freischaltbar (keine Punkte oder Voraussetzungen fehlen).")
            input("\n[Z] Zurueck: ")
            break

        print("[Z] Zurueck")
        choice = input("\nWelchen Skill lernen? ").strip().lower()

        if choice == "z":
            break
        if choice.isdigit() and 0 <= int(choice) < len(rows):
            skill_name = rows[int(choice)]
            sdef       = SKILL_TREE[skill_name]
            player.skills.add(skill_name)
            player.skill_points -= sdef["cost"]

            # Sofort-Effekte anwenden
            if skill_name == "Zaehigkeit":
                player.max_hp += 10
                player.hp     += 10
            elif skill_name == "Magieschild":
                player.shield_ready = True

            print(f"\n✨ {skill_name} gelernt! ({sdef['desc']})")
            input("(ENTER)")
