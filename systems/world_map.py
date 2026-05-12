"""
world_map.py — Weltkarten-System (Grundgerüst für v2.0)

Geplante Funktionalität:
  - Zonen auf der Weltkarte anzeigen (freigeschaltet / gesperrt)
  - Dungeon-Fortschritt pro Zone tracken (zone_progress)
  - Zonen-Boss freischalten wenn dungeon_count erfüllt
  - Neue Zonen durch Bosse freischalten
"""

from systems.zones import ZONE_DEFS, ZONE_ORDER


def get_zone_status(player, zone_id: str) -> str:
    """Gibt den Status einer Zone zurück: 'locked', 'available', 'in_progress', 'boss_ready', 'completed'"""
    zdef  = ZONE_DEFS.get(zone_id)
    if zdef is None:
        return "locked"
    if player.level < zdef["unlock_level"]:
        return "locked"

    zp             = getattr(player, "zone_progress", {}).get(zone_id, {})
    boss_defeated  = zp.get("boss_defeated", False)
    dungeons_done  = zp.get("dungeons_completed", 0)
    required       = zdef["dungeon_count"]

    if boss_defeated:
        return "completed"
    if dungeons_done >= required:
        return "boss_ready"
    if dungeons_done > 0:
        return "in_progress"
    return "available"


def show_world_map(player):
    """Zeigt die Weltkarte mit Zonen-Status an. (v2.0 — noch nicht vollständig implementiert)"""
    from ui.utils import clear_screen, print_header
    clear_screen()
    print_header("🗺️  Weltkarte")
    print("  (Vollständige Implementierung in v2.0)\n")

    for zone_id in ZONE_ORDER:
        zdef   = ZONE_DEFS[zone_id]
        status = get_zone_status(player, zone_id)
        zp     = getattr(player, "zone_progress", {}).get(zone_id, {})
        done   = zp.get("dungeons_completed", 0)
        req    = zdef["dungeon_count"]

        status_icons = {
            "locked":      "🔒",
            "available":   "🟢",
            "in_progress": "🔵",
            "boss_ready":  "🔥",
            "completed":   "✅",
        }
        icon = status_icons.get(status, "❓")

        if status == "locked":
            print(f"  {icon} {zdef['emoji']} {zdef['name']:<14}  (Level {zdef['unlock_level']} benötigt)")
        elif status == "completed":
            print(f"  {icon} {zdef['emoji']} {zdef['name']:<14}  Boss besiegt!")
        elif status == "boss_ready":
            print(f"  {icon} {zdef['emoji']} {zdef['name']:<14}  Boss bereit! ({done}/{req} Dungeons)")
        else:
            print(f"  {icon} {zdef['emoji']} {zdef['name']:<14}  {done}/{req} Dungeons")

    input("\n(ENTER)")
