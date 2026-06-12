from ui.utils import clear_screen, print_header, console
from rich.markup import escape as _esc
from systems.spiegel import SPIEGEL_DEFS, get_variant, switch_cost, buy_or_switch


def _print_upgrade(idx: int, uid: str, meta):
    d   = SPIEGEL_DEFS[uid]
    cur = get_variant(meta, uid)
    if cur is None:
        cost_tag = f"[dim]Kosten: {d['cost']} 💠[/dim]"
    else:
        cost_tag = f"[dim]Wechsel: {switch_cost(uid)} 💠[/dim]"
    a_mark = "[bold green]●[/bold green]" if cur == "A" else "[dim]○[/dim]"
    b_mark = "[bold green]●[/bold green]" if cur == "B" else "[dim]○[/dim]"
    console.print(f"  [[{idx}]] {d['emoji']} [bold]{_esc(d['name'])}[/bold]  {cost_tag}")
    console.print(f"        {a_mark} [[A]] {_esc(d['a'])}")
    console.print(f"        {b_mark} [[B]] {_esc(d['b'])}")


def spiegel_menu(meta):
    ids = list(SPIEGEL_DEFS)
    while True:
        clear_screen()
        print_header("🪞 Der Spiegel")
        console.print("  [dim]Permanente Upgrades für alle künftigen Runs. Jedes Upgrade hat[/dim]")
        console.print("  [dim]zwei Varianten — A oder B. Ein Wechsel kostet 30% des Preises.[/dim]\n")
        console.print(f"  💠 Runenessenz: [bold cyan]{meta.get('runenessenz', 0)}[/bold cyan]")
        console.print("─" * 62)
        for i, uid in enumerate(ids):
            _print_upgrade(i + 1, uid, meta)
            console.print()
        console.print("  [[0]] Zurück zur Zuflucht")

        choice = input("\nWelches Upgrade? ").strip()
        if choice == "0":
            return
        if not choice.isdigit() or not (1 <= int(choice) <= len(ids)):
            continue

        uid = ids[int(choice) - 1]
        d   = SPIEGEL_DEFS[uid]
        cur = get_variant(meta, uid)
        console.print(f"\n  {d['emoji']} [bold]{_esc(d['name'])}[/bold]")
        console.print(f"    [[A]] {_esc(d['a'])}" + ("  [green](aktiv)[/green]" if cur == "A" else ""))
        console.print(f"    [[B]] {_esc(d['b'])}" + ("  [green](aktiv)[/green]" if cur == "B" else ""))
        variant = input("  Variante wählen [A/B, ENTER = abbrechen]: ").strip().upper()
        if variant not in ("A", "B"):
            continue

        ok, msg = buy_or_switch(meta, uid, variant)
        color = "green" if ok else "red"
        console.print(f"\n  [{color}]{msg}[/{color}]")
        if ok:
            from systems.achievements import check_meta
            for m in check_meta(meta):
                console.print(f"  {m}")
        input("  (ENTER)")
