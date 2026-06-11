from ui.utils import clear_screen, print_header, console
from rich.markup import escape as _esc
from ui.pause import camp_menu
from core.save import load_meta, save_meta, load_run, save_run, delete_run, sync_achievements
from systems.hub import hub_menu
from systems.dungeon import run_dungeon
from systems.world_map import run_zone_boss, check_all_zones_cleared, victory_screen
from systems.achievements import check_all, ACHIEVEMENTS


def _choose_difficulty():
    console.print("\n  [bold]Wähle deinen Schwierigkeitsgrad:[/bold]")
    console.print("  [[E]] [green]Einfach[/green]  — Gegner schwächer,  +5 Start-HP")
    console.print("  [[N]] Normal   — Standardwerte")
    console.print("  [[H]] [red]Schwer[/red]   — Gegner stärker,    -5 Start-HP")
    mapping = {"e": "easy", "n": "normal", "h": "hard"}
    while True:
        c = input("  Deine Wahl [E/N/H]: ").lower()
        if c in mapping:
            return mapping[c]


def _new_run(meta):
    from core.player import Character
    from content.classes import choose_class, apply_class, CLASS_DEFS
    from config import DIFFICULTY_SETTINGS

    diff     = _choose_difficulty()
    class_id = choose_class()
    cdef     = CLASS_DEFS[class_id]
    player   = Character("Hero", hp=cdef["start_hp"], attack=cdef["start_atk"])
    player.difficulty = diff
    apply_class(player, class_id)

    from ui.runen_ui import choose_klassen_variante, choose_startkit, essenz_shop
    from systems.runen import apply_klassen_variante, rune_unlocked
    variante = choose_klassen_variante(meta, class_id)
    if variante:
        for m in apply_klassen_variante(player, variante):
            console.print(f"  [cyan]{m}[/cyan]")
        input("  (ENTER)")

    hp_delta = DIFFICULTY_SETTINGS.get(diff, {}).get("start_hp", 30) - 30
    if hp_delta:
        player.max_hp = max(1, player.max_hp + hp_delta)
        player.hp     = player.max_hp

    from systems.spiegel import apply_spiegel_effects
    spiegel_msgs = apply_spiegel_effects(player, meta)
    if spiegel_msgs:
        console.print("\n  [bold cyan]🪞 Der Spiegel wirkt:[/bold cyan]")
        for m in spiegel_msgs:
            console.print(f"  {m}")
        input("  (ENTER)")

    choose_startkit(meta, player)
    if rune_unlocked(meta, "haendlernetzwerk"):
        essenz_shop(meta, player)
    if rune_unlocked(meta, "schmiedegeheimnis"):
        player.schmied_gratis_upgrade = True
        console.print("\n  [cyan]🔨 Schmiedegeheimnis: Dein erstes Equipment-Upgrade in diesem Run ist gratis![/cyan]")
        input("  (ENTER)")

    player.achievements = set(meta.get("achievements", []))
    ls = meta.setdefault("lifetime_stats", {})
    ls["runs_started"] = ls.get("runs_started", 0) + 1
    save_meta(meta)
    save_run(player, quiet=True)
    return player


def _handle_defeat(player, meta):
    from content.items import EQUIPMENT_DEFS, RARITY_LABEL
    from systems.zones import ZONE_DEFS

    player.stats["deaths"] += 1
    clear_screen()
    print_header("💀 Game Over")
    console.print(f"\n  [bold red]{_esc(player.name)} wurde besiegt.[/bold red]")

    zone_id   = getattr(player, "current_zone", "wald")
    zone_name = ZONE_DEFS.get(zone_id, {}).get("name", zone_id)
    zone_emoji= ZONE_DEFS.get(zone_id, {}).get("emoji", "")
    console.print(f"  Gefallen in: {_esc(zone_emoji)} {_esc(zone_name)}  |  Level {player.level}\n")

    console.print("─" * 46)
    s = player.stats
    console.print(f"  ⚔️  Kämpfe gewonnen      : [cyan]{s.get('fights', 0)}[/cyan]")
    console.print(f"  💀  Gegner besiegt       : [cyan]{s.get('kills', 0)}[/cyan]")
    console.print(f"  🗡️  Schaden ausgeteilt   : [cyan]{s.get('damage_dealt', 0)}[/cyan]")
    console.print(f"  🛡️  Schaden erhalten     : [cyan]{s.get('damage_taken', 0)}[/cyan]")
    console.print(f"  🏰  Dungeons fertig      : [cyan]{s.get('dungeons_completed', 0)}[/cyan]")
    console.print(f"  💰  Gold verdient        : [yellow]{s.get('gold_earned', 0)}[/yellow]")
    console.print(f"  🧪  Tränke benutzt       : [cyan]{s.get('potions_used', 0)}[/cyan]")

    all_equip = list(player.inventory.get("Equipment", [])) + list(player.equipment.values())
    best = max(
        (e for e in all_equip if e["name"] not in {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}),
        key=lambda e: EQUIPMENT_DEFS.get(e["name"], {}).get("attack", 0) + EQUIPMENT_DEFS.get(e["name"], {}).get("armor", 0),
        default=None,
    )
    if best:
        edef = EQUIPMENT_DEFS.get(best["name"], {})
        _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
        console.print(f"\n  Bestes Item: {rbadge} {_esc(edef.get('emoji','⚔️'))} {_esc(best['name'])}")

    if getattr(player, "spiegel", {}).get("zweites_leben") == "B":
        from core.save import add_runenessenz
        gold_bonus = int(player.inventory.get("Gold", 0) * 0.20)
        if gold_bonus > 0:
            add_runenessenz(meta, gold_bonus)
            console.print(f"\n  [bold cyan]🪞🕊️ Zweites Leben: 20% deines Goldes gerettet — +{gold_bonus} Runenessenz![/bold cyan]")

    console.print(f"\n  Errungenschaften: [cyan]{len(getattr(player, 'achievements', set()))}/{len(ACHIEVEMENTS)}[/cyan]")
    console.print(f"  💠 Runenessenz gesamt: [bold cyan]{meta.get('runenessenz', 0)}[/bold cyan]  [dim](bleibt erhalten)[/dim]")
    console.print("─" * 46)

    sync_achievements(player, meta)
    ls = meta.setdefault("lifetime_stats", {})
    ls["runs_lost"] = ls.get("runs_lost", 0) + 1
    save_meta(meta)
    delete_run()

    console.print("\n  [dim]Dein Run endet hier — die Runenessenz bleibt dir erhalten.[/dim]")
    input("\n(ENTER) Zurück zur Zuflucht")


def _run_loop(player, meta):
    while player.is_alive():
        action = camp_menu(player, meta)

        if action == "quit":
            save_run(player, quiet=True)
            sync_achievements(player, meta)
            save_meta(meta)
            console.print("  [dim]Run gespeichert — zurück zur Zuflucht.[/dim]")
            return

        player.shop_stock = []

        if action == "boss":
            result = run_zone_boss(player, player.current_zone, meta)
        else:
            result = run_dungeon(player, meta)

        sync_achievements(player, meta)
        save_meta(meta)

        if result == "defeat":
            _handle_defeat(player, meta)
            return

        if result in ("completed", "victory"):
            for m in check_all(player, {"event": "gold_check"}):
                console.print(f"  {m}")

            if check_all_zones_cleared(player):
                victory_screen(player, meta)
                return


def main():
    meta = load_meta()
    while True:
        action = hub_menu(meta)

        if action == "quit":
            clear_screen()
            console.print("  [dim]Du verlässt die Zuflucht. Auf Wiedersehen![/dim]")
            break

        if action == "continue_run":
            player = load_run(meta)
            if player is None:
                continue
        else:
            player = _new_run(meta)

        _run_loop(player, meta)


if __name__ == "__main__":
    main()
