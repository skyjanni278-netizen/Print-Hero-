from ui.utils import clear_screen, print_header, console

# ── Dunkelsiegel (optionale Schwierigkeitsmodifikatoren, v3.3) ────────────────
# Siegel-IDs werden in meta["next_run_siegel"] und player.aktive_siegel
# serialisiert — umbenennen bricht Spielstände und laufende Runs.

SIEGEL_DEFS = {
    "blut": {
        "name":  "Siegel I — Fluch des Blutes",
        "emoji": "💀",
        "malus": "Gegner haben +20% HP",
        "bonus": 0.40,
    },
    "stille": {
        "name":  "Siegel II — Stille",
        "emoji": "💀",
        "malus": "Kein Händler im Camp, kein Wandernder Händler",
        "bonus": 0.60,
    },
    "verhaengnis": {
        "name":  "Siegel III — Verhängnis",
        "emoji": "💀",
        "malus": "Zweites Leben (Spiegel) rettet dich nicht",
        "bonus": 0.80,
    },
}

COSMETIC_ID = "dunkelkrone"


def siegel_active(player, sid: str) -> bool:
    return sid in getattr(player, "aktive_siegel", [])


def all_siegel_active(player) -> bool:
    return set(SIEGEL_DEFS) <= set(getattr(player, "aktive_siegel", []))


def siegel_essenz_mult(player) -> float:
    return 1.0 + sum(SIEGEL_DEFS[s]["bonus"]
                     for s in getattr(player, "aktive_siegel", []) if s in SIEGEL_DEFS)


def essenz_bonus_tag(player) -> str:
    mult = siegel_essenz_mult(player)
    return f" [red]💀 +{int(round((mult - 1.0) * 100))}%[/red]" if mult > 1.0 else ""


# Beim Run-Start: Auswahl aus dem Meta auf den Run übertragen.
def apply_siegel(player, meta) -> list:
    player.aktive_siegel = [s for s in meta.get("next_run_siegel", []) if s in SIEGEL_DEFS]
    msgs = []
    for sid in player.aktive_siegel:
        d = SIEGEL_DEFS[sid]
        msgs.append(f"{d['emoji']} [bold]{d['name']}[/bold] — {d['malus']}")
    if player.aktive_siegel:
        bonus = int(round((siegel_essenz_mult(player) - 1.0) * 100))
        msgs.append(f"💠 Runenessenz-Bonus in diesem Run: [bold cyan]+{bonus}%[/bold cyan]")
    return msgs


def siegel_menu(meta):
    from core.save import save_meta
    while True:
        clear_screen()
        print_header("💀 Dunkelsiegel")
        console.print("  [dim]Optionale Herausforderungen — stackbar, gelten für künftige Runs[/dim]")
        console.print("  [dim]und bleiben aktiv, bis du sie wieder ablegst.[/dim]\n")

        selected = meta.setdefault("next_run_siegel", [])
        ids = list(SIEGEL_DEFS)
        for i, sid in enumerate(ids):
            d    = SIEGEL_DEFS[sid]
            mark = "[bold red]● AKTIV[/bold red]" if sid in selected else "[dim]○[/dim]"
            console.print(f"  [[{i+1}]] {d['emoji']} [bold]{d['name']}[/bold]  {mark}")
            console.print(f"        [red]{d['malus']}[/red]  →  [cyan]+{int(d['bonus']*100)}% Runenessenz[/cyan]")
            console.print()

        total = sum(int(SIEGEL_DEFS[s]["bonus"] * 100) for s in selected)
        if total:
            console.print(f"  Gesamt-Bonus: [bold cyan]+{total}% Runenessenz[/bold cyan]")
        console.print("  [dim]Sieg mit allen 3 Siegeln: besondere Belohnung in der Zuflucht.[/dim]\n")
        console.print("  [[1-3]] Siegel an-/ablegen   [[0]] Zurück")

        choice = input("\nDeine Wahl: ").strip()
        if choice == "0":
            save_meta(meta)
            return
        if choice.isdigit() and 1 <= int(choice) <= len(ids):
            sid = ids[int(choice) - 1]
            if sid in selected:
                selected.remove(sid)
            else:
                selected.append(sid)
