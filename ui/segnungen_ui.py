from ui.utils import clear_screen, print_header, console
from rich.markup import escape as _esc
from systems.segnungen import (
    SEGNUNGEN_POOL, SYNERGIEN,
    roll_segnung_choices, apply_segnung, get_active_synergien,
)


def choose_segnung_menu(player):
    choices = roll_segnung_choices(player)
    if not choices:
        console.print("\n  [dim]✨ Du trägst bereits alle verfügbaren Segnungen.[/dim]")
        input("  (ENTER)")
        return

    from content.classes import CLASS_DEFS
    owned = set(player.active_segnungen)

    clear_screen()
    print_header("✨ Wähle eine Segnung")
    console.print("  [dim]Gilt nur für diesen Run — wähle weise.[/dim]\n")

    for i, sid in enumerate(choices):
        d = SEGNUNGEN_POOL[sid]
        class_tag = ""
        if d["class"]:
            cname     = CLASS_DEFS.get(d["class"], {}).get("name", "")
            class_tag = f" [magenta]({_esc(cname)})[/magenta]"
        syn_tag = ""
        for pair, sdef in SYNERGIEN.items():
            if sid in pair:
                other = pair[0] if pair[1] == sid else pair[1]
                if other in owned:
                    syn_tag = f"\n       [bold cyan]🔗 Synergie: {_esc(sdef['name'])} — {_esc(sdef['desc'])}[/bold cyan]"
        console.print(f"  [[{i+1}]] {d['emoji']} [bold]{_esc(d['name'])}[/bold]{class_tag}")
        console.print(f"       [dim]{_esc(d['desc'])}[/dim]{syn_tag}")
        console.print()

    while True:
        ch = input(f"  Deine Wahl [1-{len(choices)}]: ").strip()
        if ch.isdigit() and 1 <= int(ch) <= len(choices):
            sid = choices[int(ch) - 1]
            break

    console.print()
    for m in apply_segnung(player, sid):
        console.print(f"  {m}")
    input("\n  (ENTER)")


def show_segnungen_overview(player):
    clear_screen()
    print_header("✨ Aktive Segnungen")
    segs = player.active_segnungen
    if not segs:
        console.print("  [dim]Noch keine Segnungen in diesem Run.[/dim]")
        console.print("  [dim]Segnungen erhältst du nach jedem abgeschlossenen Dungeon.[/dim]")
    else:
        for sid in segs:
            d = SEGNUNGEN_POOL.get(sid)
            if not d:
                continue
            console.print(f"  {d['emoji']} [bold]{_esc(d['name'])}[/bold] — [dim]{_esc(d['desc'])}[/dim]")
        synergien = get_active_synergien(player)
        if synergien:
            console.print("\n  [bold cyan]🔗 Aktive Synergien:[/bold cyan]")
            for _, sdef in synergien:
                console.print(f"  [cyan]{_esc(sdef['name'])} — {_esc(sdef['desc'])}[/cyan]")
    input("\n  (ENTER)")
