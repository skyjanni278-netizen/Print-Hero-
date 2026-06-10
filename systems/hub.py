from ui.utils import clear_screen, print_header, console
from core.save import run_exists, delete_run


def _lifetime_stats(meta):
    clear_screen()
    print_header("📊 Statistiken (Gesamt)")
    ls = meta.get("lifetime_stats", {})
    console.print(f"  🏃 Runs gestartet     : [cyan]{ls.get('runs_started', 0)}[/cyan]")
    console.print(f"  🏆 Runs gewonnen      : [cyan]{ls.get('runs_won', 0)}[/cyan]")
    console.print(f"  💀 Runs verloren      : [cyan]{ls.get('runs_lost', 0)}[/cyan]")
    console.print(f"  💠 Essenz gesammelt   : [cyan]{ls.get('essenz_earned', 0)}[/cyan]")
    input("\n(ENTER)")


def hub_menu(meta) -> str:
    """
    Zuflucht zwischen den Runs.
    Rückgabe: 'new_run' | 'continue_run' | 'quit'
    """
    from systems.achievements import ACHIEVEMENTS, achievements_menu
    while True:
        clear_screen()
        print_header("🏕️  Die Zuflucht")
        ls  = meta.get("lifetime_stats", {})
        ach = len(meta.get("achievements", []))
        console.print(f"  💠 Runenessenz: [bold cyan]{meta.get('runenessenz', 0)}[/bold cyan]")
        console.print(f"  🏃 Runs: {ls.get('runs_started', 0)}  |  🏆 Siege: {ls.get('runs_won', 0)}  |  📜 Errungenschaften: {ach}/{len(ACHIEVEMENTS)}")
        console.print("─" * 50)
        has_run = run_exists()
        if has_run:
            console.print("  [[F]] [bold green]Run fortsetzen[/bold green]")
            console.print("  [[N]] Neuen Run starten [dim](verwirft den aktuellen Run)[/dim]")
        else:
            console.print("  [[N]] [bold green]Neuen Run starten[/bold green]")
        console.print("  [[E]] Errungenschaften")
        console.print("  [[T]] Statistiken")
        console.print("  [[Q]] Beenden")

        choice = input("\nDeine Wahl: ").strip().lower()
        if choice == "f" and has_run:
            return "continue_run"
        elif choice == "n":
            if has_run:
                c = input("  Aktuellen Run wirklich verwerfen? [J/N]: ").strip().lower()
                if c != "j":
                    continue
                delete_run()
            return "new_run"
        elif choice == "e":
            achievements_menu(set(meta.get("achievements", [])))
        elif choice == "t":
            _lifetime_stats(meta)
        elif choice == "q":
            return "quit"
