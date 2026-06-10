import random
from ui.utils import clear_screen, print_header, console, hp_bar
from rich.markup import escape as _esc
from rich.panel import Panel
from systems.zones import ZONE_DEFS, ZONE_ORDER, ZONE_FLAVOR, _is_zone_unlocked

ZONE_BOSS_DEFS = {
    "wald": {
        "name":      "Torg, Wächter des Waldes",
        "emoji":     "🌿",
        "hp_mult":   1.95,
        "atk_mult":  0.85,
        "loot_rank": 3,
        "intro":   (
            "Aus dem Dunkel des uralten Waldes tritt ein gewaltiger Troll.\n"
            "Torg hat diesen Wald seit Jahrhunderten bewacht — und er kennt\n"
            "keine Gnade für Eindringlinge."
        ),
        "victory": "Torg stürzt donnernd zu Boden. Die Bäume erzittern. Zum ersten Mal seit Jahrhunderten herrscht Stille im Wald.",
    },
    "ruinen": {
        "name":      "Korroth, der Ewige Wächter",
        "emoji":     "🗿",
        "hp_mult":   1.85,
        "atk_mult":  0.80,
        "loot_rank": 3,
        "intro":   (
            "Die Ruinen beben. Steine fügen sich zu einer gewaltigen Gestalt.\n"
            "Korroth war einst der Hüter dieser Festung — jetzt ist er verdammt,\n"
            "sie in Ewigkeit zu beschützen. Nichts überlebt seinen Zorn."
        ),
        "victory": "Mit einem letzten Knirschen zerfällt Korroth zu Staub. Die Ruinen schweigen endlich.",
    },
    "wueste": {
        "name":      "Razin, König der Meuchler",
        "emoji":     "🏜️",
        "hp_mult":   2.05,
        "atk_mult":  0.82,
        "loot_rank": 4,
        "intro":   (
            "Ein Schatten löst sich von der Wand.\n"
            "Razin, der Meuchler-König, tritt in das Licht — er hat dich\n"
            "schon lange beobachtet. Er kennt deinen Todeszeitpunkt. Bereits."
        ),
        "victory": "Razin sinkt in den Sand. Die Meuchler-Gilden sind führerlos. Die Wüste gehört dir.",
    },
    "vulkan": {
        "name":      "Ignar, der Ewige Drache",
        "emoji":     "🐉",
        "hp_mult":   2.2,
        "atk_mult":  0.83,
        "loot_rank": 4,
        "intro":   (
            "Die Lava brodelt. Ein Drache — alt wie der Vulkan selbst —\n"
            "entfaltet seine gewaltigen Schwingen. Ignar hat noch keinen\n"
            "Herausforderer überleben lassen. Sein Atem schmilzt Stahl."
        ),
        "victory": "Ignar stürzt in die Lava. Ein letzter Feuersturm erfüllt die Höhle — dann Stille. Du hast den ewigen Drachen bezwungen.",
    },
    "dunkelreich": {
        "name":      "Malachar, Herr der Finsternis",
        "emoji":     "💀",
        "hp_mult":   2.6,
        "atk_mult":  0.87,
        "loot_rank": 5,
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
    from content.loot_tables import roll_boss_loot, apply_loot
    from systems.achievements import check_all
    from systems.zones import scale_enemy

    bdef       = ZONE_BOSS_DEFS[zone_id]
    zdef       = ZONE_DEFS[zone_id]
    boss_class = zdef["boss_class"]

    boss         = boss_class(rank=5)
    boss.name    = bdef["name"]
    boss.max_hp  = max(1, int(boss.max_hp * bdef.get("hp_mult", 2.5)))
    boss.hp      = boss.max_hp
    boss.attack  = max(1, int(boss.attack * bdef.get("atk_mult", 1.0)))
    scale_enemy(boss, player)

    clear_screen()
    print_header(f"🔥 ZONEN-BOSS  —  {_esc(bdef['emoji'])} {_esc(zdef['name'])}")
    intro_text = "\n".join(f"  {_esc(line)}" for line in bdef["intro"].splitlines())
    console.print(Panel(intro_text, border_style="bright_red", expand=False, padding=(0, 1)))
    hp_b = hp_bar(boss.max_hp, boss.max_hp)
    console.print(f"\n  [bold]{_esc(boss.name)}[/bold]")
    console.print(f"  HP {hp_b} {boss.max_hp}   ATK {boss.attack}")
    console.print("\n  [bold bright_red]⚔️  In den Kampf![/bold bright_red]")
    input("  (ENTER) ")

    pots_before = player.stats.get("potions_used", 0)
    result = combat(player, [boss])
    player.reset_combat_modifiers()

    if result == "defeat":
        player.stats["deaths"] = player.stats.get("deaths", 0) + 1
        return "defeat"
    if result == "fled":
        return "fled"

    # ── Sieg ──────────────────────────────────────────────────
    clear_screen()
    print_header(f"🏆 ZONEN-BOSS BESIEGT!  {_esc(bdef['emoji'])}")
    console.print(f"\n  [bold green]{_esc(bdef['victory'])}[/bold green]\n")

    zp = getattr(player, "zone_progress", {})
    if zone_id not in zp:
        zp[zone_id] = {"dungeons_completed": 0, "boss_defeated": False}
    zp[zone_id]["boss_defeated"] = True
    player.zone_progress = zp

    player.stats["kills"]  = player.stats.get("kills", 0) + 1
    player.stats["fights"] = player.stats.get("fights", 0) + 1

    gold_before = player.inventory["Gold"]
    zone_id     = getattr(player, "current_zone", "wald")
    loot_items  = roll_boss_loot(zone_id)
    loot_msgs   = apply_loot(player, loot_items)
    player.stats["gold_earned"] = player.stats.get("gold_earned", 0) + player.inventory["Gold"] - gold_before

    total_xp = int(boss.xp_value * player.next_fight_xp_mult * player.get_xp_bonus_mult())
    player.next_fight_xp_mult = 1.0
    player.xp += total_xp
    lvl_msgs = player.check_level_up()

    if loot_msgs:
        console.print("  [bold yellow]💰 Boss-Beute:[/bold yellow]")
        for m in loot_msgs:
            console.print(f"  {m}")
    for m in lvl_msgs:
        console.print(f"  {m}")
    console.print(f"\n  [bold green]+{total_xp} XP[/bold green]")

    pots_used = player.stats.get("potions_used", 0) - pots_before
    for m in check_all(player, {"event": "victory", "enemies": [boss], "potions_used": pots_used}):
        console.print(f"  {m}")
    for m in check_all(player, {"event": "level_up", "level": player.level}):
        console.print(f"  {m}")

    # Nächste Zone freigeschaltet?
    idx = ZONE_ORDER.index(zone_id)
    if idx + 1 < len(ZONE_ORDER):
        next_zid  = ZONE_ORDER[idx + 1]
        next_zdef = ZONE_DEFS[next_zid]
        if player.level >= next_zdef["unlock_level"]:
            console.print(f"\n  [bold cyan]🗺️  Neue Zone freigeschaltet: {_esc(next_zdef['emoji'])} {_esc(next_zdef['name'])}![/bold cyan]")
        else:
            console.print(f"\n  [dim]🗺️  {_esc(next_zdef['emoji'])} {_esc(next_zdef['name'])} — ab Level {next_zdef['unlock_level']} zugänglich.[/dim]")

    input("\n(ENTER)")
    return "victory"


def show_world_map(player):
    """
    Interaktive Weltkarte zur Zonen-Auswahl.
    Setzt player.current_zone und gibt None zurück.
    """
    _legacy_unlock_fix(player)

    _STATUS_ICONS = {
        "locked":      "🔒",
        "available":   "🟢",
        "in_progress": "🔵",
        "boss_ready":  "🔥",
        "completed":   "✅",
    }
    _STATUS_COLORS = {
        "locked":      "dim",
        "available":   "green",
        "in_progress": "cyan",
        "boss_ready":  "bold bright_red",
        "completed":   "green",
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
            icon   = _STATUS_ICONS[status]
            c      = _STATUS_COLORS[status]
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
                console.print(f"  [{c}]{icon} [[{i+1}]]{active} {_esc(zdef['emoji'])} {_esc(zdef['name']):<16} {_esc(lock_info)}[/{c}]")
            elif status == "completed":
                console.print(f"  [{c}]{icon} [[{i+1}]]{active} {_esc(zdef['emoji'])} {_esc(zdef['name']):<16} Boss besiegt ✓[/{c}]")
            elif status == "boss_ready":
                console.print(f"  [{c}]{icon} [[{i+1}]]{active} {_esc(zdef['emoji'])} {_esc(zdef['name']):<16} 🔥 BOSS BEREIT  ({done}/{req})[/{c}]")
            else:
                console.print(f"  [{c}]{icon} [[{i+1}]]{active} {_esc(zdef['emoji'])} {_esc(zdef['name']):<16} {done}/{req} Dungeons[/{c}]")

        console.print("\n  [[1-5]] Zone wählen   [[Z]] Zurück")
        choice = input("\nDeine Wahl: ").strip().lower()

        if choice == "z":
            return

        if not choice.isdigit() or not (1 <= int(choice) <= len(ZONE_ORDER)):
            continue

        idx    = int(choice) - 1
        zid    = ZONE_ORDER[idx]
        status = statuses[zid]

        if status == "locked":
            console.print("\n  [dim]🔒 Diese Zone ist noch gesperrt.[/dim]")
            input("  (ENTER)")
            continue

        if zid != cur_zone:
            player.current_zone           = zid
            player.schwarzmarkt_available = True
            player.shop_stock             = []
            clear_screen()
            zdef = ZONE_DEFS[zid]
            print_header(f"{_esc(zdef['emoji'])}  {_esc(zdef['name'])}")
            for line in ZONE_FLAVOR.get(zid, []):
                console.print(f"  {_esc(line)}")
            console.print(f"\n  [green]✅ Zone gewechselt zu: {_esc(zdef['emoji'])} {_esc(zdef['name'])}[/green]")
            input("\n(ENTER)")
        return


def victory_screen(player, meta):
    """Sieg-Screen nach dem Besiegen aller Zonen-Bosse. Beendet den Run → Hub."""
    from core.save import save_meta, delete_run, sync_achievements
    from systems.achievements import ACHIEVEMENTS

    clear_screen()
    console.print(Panel(
        "[bold yellow]🏆  ALLE ZONEN BEZWUNGEN!  🏆[/bold yellow]",
        border_style="yellow",
        expand=True,
        padding=(0, 0),
    ))
    console.print()
    console.print("  [bold]Du hast alle 5 Zonen des Reiches bezwungen.[/bold]")
    console.print("  Malachar, der Herr der Finsternis, ist gefallen.")
    console.print("  [dim]Das Reich ist gerettet — vorerst.[/dim]\n")
    console.print("─" * 52)

    s = player.stats
    console.print(f"  ⚔️  Kämpfe gewonnen      : [cyan]{s.get('fights', 0)}[/cyan]")
    console.print(f"  💀  Gegner besiegt       : [cyan]{s.get('kills', 0)}[/cyan]")
    console.print(f"  🗡️  Schaden ausgeteilt   : [cyan]{s.get('damage_dealt', 0)}[/cyan]")
    console.print(f"  🛡️  Schaden erhalten     : [cyan]{s.get('damage_taken', 0)}[/cyan]")
    console.print(f"  🏰  Dungeons abgeschl.   : [cyan]{s.get('dungeons_completed', 0)}[/cyan]")
    console.print(f"  💰  Gold verdient        : [yellow]{s.get('gold_earned', 0)}[/yellow]")
    console.print(f"  🧪  Tränke benutzt       : [cyan]{s.get('potions_used', 0)}[/cyan]")
    console.print(f"  📈  Errungenschaften     : [cyan]{len(getattr(player, 'achievements', set()))}/{len(ACHIEVEMENTS)}[/cyan]")
    console.print("─" * 52)

    from systems.achievements import check_all
    for m in check_all(player, {"event": "run_won"}):
        console.print(f"  {m}")

    sync_achievements(player, meta)
    ls = meta.setdefault("lifetime_stats", {})
    ls["runs_won"] = ls.get("runs_won", 0) + 1
    save_meta(meta)
    delete_run()

    console.print("\n  [bold green]Der Run ist abgeschlossen — zurück zur Zuflucht.[/bold green]")
    input("\n(ENTER)")
