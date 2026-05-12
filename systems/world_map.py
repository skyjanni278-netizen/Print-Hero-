import random
from ui.utils import clear_screen, print_header
from systems.zones import ZONE_DEFS, ZONE_ORDER, ZONE_FLAVOR, _is_zone_unlocked

ZONE_BOSS_DEFS = {
    "wald": {
        "name":    "Torg, Wächter des Waldes",
        "emoji":   "🌿",
        "hp_mult": 2.5,
        "intro":   (
            "Aus dem Dunkel des uralten Waldes tritt ein gewaltiger Troll.\n"
            "Torg hat diesen Wald seit Jahrhunderten bewacht — und er kennt\n"
            "keine Gnade für Eindringlinge."
        ),
        "victory": "Torg stürzt donnernd zu Boden. Die Bäume erzittern. Zum ersten Mal seit Jahrhunderten herrscht Stille im Wald.",
    },
    "ruinen": {
        "name":    "Korroth, der Ewige Wächter",
        "emoji":   "🗿",
        "hp_mult": 2.5,
        "intro":   (
            "Die Ruinen beben. Steine fügen sich zu einer gewaltigen Gestalt.\n"
            "Korroth war einst der Hüter dieser Festung — jetzt ist er verdammt,\n"
            "sie in Ewigkeit zu beschützen. Nichts überlebt seinen Zorn."
        ),
        "victory": "Mit einem letzten Knirschen zerfällt Korroth zu Staub. Die Ruinen schweigen endlich.",
    },
    "wueste": {
        "name":    "Razin, König der Meuchler",
        "emoji":   "🏜️",
        "hp_mult": 2.8,
        "intro":   (
            "Ein Schatten löst sich von der Wand.\n"
            "Razin, der Meuchler-König, tritt in das Licht — er hat dich\n"
            "schon lange beobachtet. Er kennt deinen Todeszeitpunkt. Bereits."
        ),
        "victory": "Razin sinkt in den Sand. Die Meuchler-Gilden sind führerlos. Die Wüste gehört dir.",
    },
    "vulkan": {
        "name":    "Ignar, der Ewige Drache",
        "emoji":   "🐉",
        "hp_mult": 3.0,
        "intro":   (
            "Die Lava brodelt. Ein Drache — alt wie der Vulkan selbst —\n"
            "entfaltet seine gewaltigen Schwingen. Ignar hat noch keinen\n"
            "Herausforderer überleben lassen. Sein Atem schmilzt Stahl."
        ),
        "victory": "Ignar stürzt in die Lava. Ein letzter Feuersturm erfüllt die Höhle — dann Stille. Du hast den ewigen Drachen bezwungen.",
    },
    "dunkelreich": {
        "name":    "Malachar, Herr der Finsternis",
        "emoji":   "💀",
        "hp_mult": 3.5,
        "intro":   (
            "Absolute Stille. Dann: Schritte.\n"
            "Malachar, der Herr des Dunkel-Reichs, tritt aus der Finsternis.\n"
            "Er ist kein Mensch mehr — er ist die Dunkelheit selbst.\n"
            "Dies ist dein letzter Kampf."
        ),
        "victory": "Malachar zersplittert in tausend Scherben. Das Dunkel-Reich bricht zusammen. Du hast gewonnen.",
    },
}


def _legacy_unlock_fix(player):
    """
    Kompatibilität mit alten Spielständen: War der Spieler bereits in einer
    höheren Zone, werden alle vorherigen Zonen-Bosse als besiegt markiert.
    Nur aktiv wenn zone_progress noch komplett leer ist.
    """
    zp = getattr(player, "zone_progress", {})
    total = sum(v.get("dungeons_completed", 0) for v in zp.values())
    if total > 0:
        return
    current = getattr(player, "current_zone", "wald")
    if current not in ZONE_ORDER:
        return
    idx = ZONE_ORDER.index(current)
    for i in range(idx):
        zid = ZONE_ORDER[i]
        if zid not in zp:
            zp[zid] = {"dungeons_completed": 0, "boss_defeated": False}
        zp[zid]["boss_defeated"] = True
    player.zone_progress = zp


def get_zone_status(player, zone_id: str) -> str:
    """Gibt zurück: 'locked' | 'available' | 'in_progress' | 'boss_ready' | 'completed'"""
    _legacy_unlock_fix(player)
    if not _is_zone_unlocked(player, zone_id):
        return "locked"
    zp   = getattr(player, "zone_progress", {}).get(zone_id, {})
    done = zp.get("dungeons_completed", 0)
    req  = ZONE_DEFS[zone_id]["dungeon_count"]
    if zp.get("boss_defeated", False):
        return "completed"
    if done >= req:
        return "boss_ready"
    if done > 0:
        return "in_progress"
    return "available"


def check_all_zones_cleared(player) -> bool:
    return all(
        getattr(player, "zone_progress", {}).get(z, {}).get("boss_defeated", False)
        for z in ZONE_ORDER
    )


def run_zone_boss(player, zone_id: str) -> str:
    """
    Zonen-Boss-Kampf.
    Rückgabe: 'victory' | 'defeat' | 'fled'
    """
    from core.combat import combat
    from content.loot_tables import roll_loot, apply_loot
    from systems.achievements import check_all
    from config import DIFFICULTY_SETTINGS

    bdef       = ZONE_BOSS_DEFS[zone_id]
    zdef       = ZONE_DEFS[zone_id]
    boss_class = zdef["boss_class"]

    boss         = boss_class(rank=5)
    boss.name    = bdef["name"]
    boss.max_hp  = max(1, int(boss.max_hp * bdef.get("hp_mult", 2.5)))
    boss.hp      = boss.max_hp

    diff = getattr(player, "difficulty", "normal")
    if diff != "normal":
        cfg          = DIFFICULTY_SETTINGS[diff]
        boss.max_hp  = max(1, int(boss.max_hp * cfg["hp_mult"]))
        boss.hp      = boss.max_hp
        boss.attack  = max(1, int(boss.attack * cfg["atk_mult"]))

    ng = getattr(player, "ng_plus", 0)
    if ng > 0:
        mult        = 1.3 ** ng
        boss.max_hp = max(1, int(boss.max_hp * mult))
        boss.hp     = boss.max_hp
        boss.attack = max(1, int(boss.attack * mult))

    clear_screen()
    print_header(f"🔥 ZONEN-BOSS  —  {bdef['emoji']} {zdef['name']}")
    print()
    for line in bdef["intro"].splitlines():
        print(f"  {line}")
    print(f"\n  Boss:  {boss.name}")
    print(f"  HP:    {boss.max_hp}   |   ATK: {boss.attack}")
    input("\n⚔️  In den Kampf! (ENTER)")

    result = combat(player, [boss])
    player.reset_combat_modifiers()

    if result == "defeat":
        player.stats["deaths"] = player.stats.get("deaths", 0) + 1
        return "defeat"
    if result == "fled":
        return "fled"

    # ── Sieg ──────────────────────────────────────────────────
    clear_screen()
    print_header(f"🏆 ZONEN-BOSS BESIEGT!  {bdef['emoji']}")
    print(f"\n  {bdef['victory']}\n")

    zp = getattr(player, "zone_progress", {})
    if zone_id not in zp:
        zp[zone_id] = {"dungeons_completed": 0, "boss_defeated": False}
    zp[zone_id]["boss_defeated"] = True
    player.zone_progress = zp

    player.stats["kills"]  = player.stats.get("kills", 0) + 1
    player.stats["fights"] = player.stats.get("fights", 0) + 1

    gold_before = player.inventory["Gold"]
    loot_items  = roll_loot(rank=5, rolls=8)
    loot_msgs   = apply_loot(player, loot_items)
    player.stats["gold_earned"] = player.stats.get("gold_earned", 0) + player.inventory["Gold"] - gold_before

    total_xp = int(boss.xp_value * player.next_fight_xp_mult)
    player.next_fight_xp_mult = 1.0
    player.xp += total_xp
    player.check_level_up()

    if loot_msgs:
        print("💰 Boss-Beute:")
        for m in loot_msgs:
            print(m)
    print(f"\n+{total_xp} XP")

    for m in check_all(player, {"event": "victory", "enemies": [boss]}):
        print(m)

    # Nächste Zone freigeschaltet?
    idx = ZONE_ORDER.index(zone_id)
    if idx + 1 < len(ZONE_ORDER):
        next_zid  = ZONE_ORDER[idx + 1]
        next_zdef = ZONE_DEFS[next_zid]
        if player.level >= next_zdef["unlock_level"]:
            print(f"\n🗺️  Neue Zone freigeschaltet: {next_zdef['emoji']} {next_zdef['name']}!")
        else:
            print(f"\n🗺️  {next_zdef['emoji']} {next_zdef['name']} — ab Level {next_zdef['unlock_level']} zugänglich.")

    input("\n(ENTER)")
    return "victory"


def show_world_map(player):
    """
    Interaktive Weltkarte zur Zonen-Auswahl.
    Setzt player.current_zone und gibt None zurück.
    """
    _legacy_unlock_fix(player)

    STATUS_ICONS = {
        "locked":      "🔒",
        "available":   "🟢",
        "in_progress": "🔵",
        "boss_ready":  "🔥",
        "completed":   "✅",
    }

    while True:
        clear_screen()
        print_header("🗺️  Weltkarte")

        statuses = {z: get_zone_status(player, z) for z in ZONE_ORDER}
        cur_zone = getattr(player, "current_zone", "wald")

        for i, zid in enumerate(ZONE_ORDER):
            zdef   = ZONE_DEFS[zid]
            bdef   = ZONE_BOSS_DEFS[zid]
            status = statuses[zid]
            icon   = STATUS_ICONS[status]
            zp     = getattr(player, "zone_progress", {}).get(zid, {})
            done   = zp.get("dungeons_completed", 0)
            req    = zdef["dungeon_count"]
            active = "►" if zid == cur_zone else " "

            if status == "locked":
                prev_zid  = ZONE_ORDER[i - 1]
                prev_boss = ZONE_BOSS_DEFS[prev_zid]["name"]
                lock_info = f"🔒 {prev_boss} besiegen"
                if player.level < zdef["unlock_level"]:
                    lock_info += f" + Level {zdef['unlock_level']}"
                print(f"  {icon} [{i+1}]{active} {zdef['emoji']} {zdef['name']:<16} {lock_info}")
            elif status == "completed":
                print(f"  {icon} [{i+1}]{active} {zdef['emoji']} {zdef['name']:<16} Boss besiegt ✓")
            elif status == "boss_ready":
                print(f"  {icon} [{i+1}]{active} {zdef['emoji']} {zdef['name']:<16} 🔥 BOSS BEREIT  ({done}/{req})")
            else:
                print(f"  {icon} [{i+1}]{active} {zdef['emoji']} {zdef['name']:<16} {done}/{req} Dungeons")

        print("\n  [1-5] Zone wählen   [Z] Zurück")
        choice = input("\nDeine Wahl: ").strip().lower()

        if choice == "z":
            return

        if not choice.isdigit() or not (1 <= int(choice) <= len(ZONE_ORDER)):
            continue

        idx    = int(choice) - 1
        zid    = ZONE_ORDER[idx]
        status = statuses[zid]

        if status == "locked":
            print("\n  🔒 Diese Zone ist noch gesperrt.")
            input("  (ENTER)")
            continue

        if zid != cur_zone:
            player.current_zone           = zid
            player.schwarzmarkt_available = True
            player.shop_stock             = []
            clear_screen()
            zdef = ZONE_DEFS[zid]
            print_header(f"{zdef['emoji']}  {zdef['name']}")
            for line in ZONE_FLAVOR.get(zid, []):
                print(f"  {line}")
            print(f"\n✅ Zone gewechselt zu: {zdef['emoji']} {zdef['name']}")
            input("\n(ENTER)")
        return


def endscreen(player) -> str:
    """
    Zeigt den Endscreen nach dem Besiegen aller Zonen-Bosse.
    Rückgabe: 'ng_plus' | 'continue'
    """
    from core.save import save_game
    from systems.achievements import check_all

    clear_screen()
    print("=" * 52)
    print("    🏆  ALLE ZONEN BEZWUNGEN!  🏆")
    print("=" * 52)
    print()
    print("  Du hast alle 5 Zonen des Reiches bezwungen.")
    print("  Malachar, der Herr der Finsternis, ist gefallen.")
    print("  Das Reich ist gerettet — vorerst.\n")
    print("-" * 52)

    s = player.stats
    print(f"  ⚔️  Kämpfe gewonnen      : {s.get('fights', 0)}")
    print(f"  💀  Gegner besiegt       : {s.get('kills', 0)}")
    print(f"  🗡️  Schaden ausgeteilt   : {s.get('damage_dealt', 0)}")
    print(f"  🛡️  Schaden erhalten     : {s.get('damage_taken', 0)}")
    print(f"  🏰  Dungeons abgeschl.   : {s.get('dungeons_completed', 0)}")
    print(f"  💰  Gold verdient        : {s.get('gold_earned', 0)}")
    print(f"  🧪  Tränke benutzt       : {s.get('potions_used', 0)}")
    print(f"  📈  Errungenschaften     : {len(getattr(player, 'achievements', set()))}/20")
    print("-" * 52)

    ng_next = player.ng_plus + 1
    mult    = round(1.3 ** ng_next, 2)
    print(f"\n  ⭐ New Game+ Runde {ng_next} — Gegner ×{mult} HP und ATK")
    print("  Du behältst: Gold + alle legendären Items\n")
    print("  [J] New Game+ starten")
    print("  [W] Weiterspielen (freies Erkunden)")

    while True:
        c = input("\nDeine Wahl: ").lower()
        if c == "j":
            player.start_ng_plus()
            for m in check_all(player, {"event": "ng_plus"}):
                print(m)
            save_game(player)
            clear_screen()
            print_header("⭐ New Game+ gestartet!")
            print(f"  Runde {player.ng_plus} beginnt.")
            print("  Die Zonen-Bosse erwachen stärker als je zuvor...")
            input("\n(ENTER)")
            return "ng_plus"
        elif c == "w":
            return "continue"
