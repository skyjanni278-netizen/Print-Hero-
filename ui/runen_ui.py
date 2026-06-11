import json
import os
from ui.utils import clear_screen, print_header, console
from rich.markup import escape as _esc
from systems.runen import (
    RUNEN_DEFS, KATEGORIE_LABELS,
    rune_unlocked, available_startkits, apply_startkit, apply_klassen_variante,
)


def runen_overview(meta):
    clear_screen()
    print_header("🧿 Runen")
    unlocked = set(meta.get("unlocked_runen", []))
    console.print(f"  [dim]Gefundene Runen schalten dauerhaft neue Optionen frei.[/dim]")
    console.print(f"  Fortschritt: [bold cyan]{len(unlocked)}/{len(RUNEN_DEFS)}[/bold cyan]")
    for kat, label in KATEGORIE_LABELS.items():
        console.print(f"\n  [bold]{label}[/bold]")
        for rid, d in RUNEN_DEFS.items():
            if d["kategorie"] != kat:
                continue
            if rid in unlocked:
                console.print(f"    ✅ {d['emoji']} [bold]{_esc(d['name'])}[/bold] — [dim]{_esc(d['desc'])}[/dim]")
            else:
                console.print(f"    [dim]🔒 ???  — noch nicht gefunden[/dim]")
    console.print("\n  [dim]Drops: Zonen-Boss garantiert (1× pro Boss), Dungeon-Boss 25%, Elite 5%, Schatztruhe 15%[/dim]")
    input("\n  (ENTER)")


# ── Klassen-Variante beim Run-Start ───────────────────────────────────────────

_VARIANTEN = {"warrior": ("berserker_erbe", "berserker"), "rogue": ("meuchler_erbe", "meuchler")}


def choose_klassen_variante(meta, class_id: str):
    entry = _VARIANTEN.get(class_id)
    if not entry or not rune_unlocked(meta, entry[0]):
        return None
    rid, variante = entry
    d = RUNEN_DEFS[rid]
    from content.classes import CLASS_DEFS
    cdef = CLASS_DEFS[class_id]
    console.print(f"\n  [bold]Du hast die Rune {d['emoji']} {_esc(d['name'])} — wähle deine Spielart:[/bold]")
    console.print(f"  [[1]] {cdef['emoji']} {_esc(cdef['name'])} (Standard)")
    console.print(f"  [[2]] {d['emoji']} [bold]{_esc(d['name'])}[/bold] — [dim]{_esc(d['desc'])}[/dim]")
    while True:
        ch = input("  Deine Wahl [1/2]: ").strip()
        if ch == "1":
            return None
        if ch == "2":
            return variante


# ── Startkit-Wahl beim Run-Start ──────────────────────────────────────────────

def choose_startkit(meta, player):
    kits = available_startkits(meta, player.player_class)
    if not kits:
        return
    clear_screen()
    print_header("🎒 Startkit wählen")
    console.print("  [dim]Deine gefundenen Runen erlauben dir eine Startausrüstung.[/dim]\n")
    for i, rid in enumerate(kits):
        d = RUNEN_DEFS[rid]
        console.print(f"  [[{i+1}]] {d['emoji']} [bold]{_esc(d['name'])}[/bold] — [dim]{_esc(d['desc'])}[/dim]")
    console.print("  [[0]] Ohne Startkit beginnen")
    while True:
        ch = input("\n  Deine Wahl: ").strip()
        if ch == "0":
            return
        if ch.isdigit() and 1 <= int(ch) <= len(kits):
            rid = kits[int(ch) - 1]
            break
    console.print()
    for m in apply_startkit(player, rid):
        console.print(f"  [green]{m}[/green]")
    input("\n  (ENTER)")


# ── Essenz-Händlerin (Händlernetzwerk) ────────────────────────────────────────

_ESSENZ_KATALOG = [
    ("Healing Potion",   8),
    ("Antidot",          6),
    ("Energie-Kristall", 12),
    ("Großes Heiltrank", 15),
    ("Stärketrank",      15),
    ("Phönixfeder",      30),
]


def essenz_shop(meta, player):
    from core.save import spend_runenessenz
    from content.items import CONSUMABLE_DEFS
    while True:
        clear_screen()
        print_header("🧺 Essenz-Händlerin")
        console.print("  [dim]\"Runenessenz gegen Vorräte — ein fairer Tausch, oder?\"[/dim]\n")
        console.print(f"  💠 Runenessenz: [bold cyan]{meta.get('runenessenz', 0)}[/bold cyan]\n")
        for i, (key, price) in enumerate(_ESSENZ_KATALOG):
            cdef  = CONSUMABLE_DEFS.get(key, {})
            emoji = cdef.get("emoji", "🧪")
            desc  = cdef.get("desc", "")
            cur   = player.inventory.get("Consumables", {}).get(key, 0)
            can_afford = meta.get("runenessenz", 0) >= price
            price_col  = "cyan" if can_afford else "red"
            console.print(f"  [[{i+1}]] {_esc(emoji)} {_esc(key):<22} (×{cur})  [dim]{_esc(desc):<20}[/dim] [{price_col}]{price} 💠[/{price_col}]")
        console.print("\n  [[0]] Weiter zum Run")
        ch = input("\n  Was kaufen? ").strip()
        if ch == "0" or not ch.isdigit():
            return
        idx = int(ch) - 1
        if not (0 <= idx < len(_ESSENZ_KATALOG)):
            continue
        key, price = _ESSENZ_KATALOG[idx]
        if meta.get("runenessenz", 0) < price:
            console.print("  [red]Nicht genug Runenessenz![/red]")
            input("  (ENTER)")
            continue
        if not player.can_add_consumable(key):
            console.print("  [red]Inventar voll oder Stapel bereits voll![/red]")
            input("  (ENTER)")
            continue
        player.add_consumable(key, 1)
        spend_runenessenz(meta, price)
        console.print(f"  [green]✅ {_esc(key)} gekauft![/green]")
        input("  (ENTER)")


# ── Orakel (Orakelwissen) ─────────────────────────────────────────────────────

def orakel_menu(meta):
    from core.save import RUN_PATH
    from core.player import Character
    from systems.zones import ZONE_DEFS, ZONE_ORDER, scale_enemy
    from systems.world_map import ZONE_BOSS_DEFS

    clear_screen()
    print_header("🔮 Das Orakel")
    if not os.path.exists(RUN_PATH):
        console.print("  [dim]Das Orakel schweigt — starte zuerst einen Run.[/dim]")
        input("\n  (ENTER)")
        return
    try:
        with open(RUN_PATH, "r") as f:
            player = Character.from_dict(json.load(f))
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        console.print("  [red]Das Orakel kann deinen Run nicht deuten.[/red]")
        input("\n  (ENTER)")
        return

    next_zone = next(
        (z for z in ZONE_ORDER
         if not player.zone_progress.get(z, {}).get("boss_defeated", False)),
        None,
    )
    if next_zone is None:
        console.print("  [dim]\"Alle Wächter sind gefallen. Ich habe dir nichts mehr zu zeigen.\"[/dim]")
        input("\n  (ENTER)")
        return

    bdef = ZONE_BOSS_DEFS[next_zone]
    zdef = ZONE_DEFS[next_zone]
    boss = zdef["boss_class"](rank=5)
    boss.name   = bdef["name"]
    boss.max_hp = max(1, int(boss.max_hp * bdef.get("hp_mult", 2.5)))
    boss.hp     = boss.max_hp
    boss.attack = max(1, int(boss.attack * bdef.get("atk_mult", 1.0)))
    scale_enemy(boss, player)

    console.print("  [dim]Das Orakel blickt in den Nebel und zeigt dir deinen nächsten Wächter...[/dim]\n")
    console.print(f"  {_esc(bdef['emoji'])} [bold]{_esc(bdef['name'])}[/bold]  —  Zone: {_esc(zdef.get('emoji',''))} {_esc(zdef.get('name', next_zone))}")
    console.print(f"     ❤️ HP : [red]{boss.max_hp}[/red]")
    console.print(f"     ⚔️ ATK: [yellow]{boss.attack}[/yellow]")
    console.print(f"     [dim]Boss-Fähigkeit: ~30% Chance pro Runde[/dim]")
    console.print(f"\n  [dim](Werte basieren auf deinem aktuellen Run — Level {player.level})[/dim]")
    input("\n  (ENTER)")
