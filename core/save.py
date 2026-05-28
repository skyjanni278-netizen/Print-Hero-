import json
import os
from core.player import Character
from ui.utils import console

_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR = os.path.join(_ROOT, "saves")


def _slot_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"savegame_{slot}.json")


def get_save_slots() -> list:
    """Gibt Info-Dicts für alle 3 Slots zurück."""
    slots = []
    for s in (1, 2, 3):
        path = _slot_path(s)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    d = json.load(f)
                slots.append({
                    "slot": s, "exists": True,
                    "name": d.get("name", "?"),
                    "level": d.get("level", 1),
                    "player_class": d.get("player_class", "warrior"),
                    "ng_plus": d.get("ng_plus", 0),
                    "difficulty": d.get("difficulty", "normal"),
                })
            except (json.JSONDecodeError, KeyError, TypeError):
                slots.append({
                    "slot": s, "exists": True, "corrupt": True,
                    "name": "??? (beschädigt)", "level": 0,
                    "player_class": "?", "ng_plus": 0, "difficulty": "?",
                })
        else:
            slots.append({"slot": s, "exists": False})
    return slots


def save_game(player):
    os.makedirs(SAVE_DIR, exist_ok=True)
    slot = getattr(player, "save_slot", 1)
    path = _slot_path(slot)
    with open(path, "w") as f:
        json.dump(player.to_dict(), f, indent=2)
    console.print(f"  [green]💾 Spielstand {slot} gespeichert![/green]")


def load_game(slot: int = 1):
    path = _slot_path(slot)
    # Legacy-Fallback für alten einzelnen Spielstand
    if not os.path.exists(path):
        legacy = os.path.join(SAVE_DIR, "savegame.json")
        if os.path.exists(legacy):
            path = legacy
        elif os.path.exists("savegame.json"):
            path = "savegame.json"
        else:
            return None
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        console.print(f"\n  [red]Spielstand {slot} ist beschädigt und kann nicht geladen werden.[/red]")
        console.print(f"  [dim]Fehler: {e}[/dim]")
        input("  (ENTER)")
        return None
    try:
        player = Character.from_dict(data, slot=slot)
    except (KeyError, TypeError) as e:
        console.print(f"\n  [red]Spielstand {slot} hat ein ungültiges Format.[/red]")
        console.print(f"  [dim]Fehler: {e}[/dim]")
        input("  (ENTER)")
        return None
    console.print(f"  [green]📂 Spielstand {slot} geladen![/green]")
    return player


def save_exists():
    return (
        any(os.path.exists(_slot_path(s)) for s in (1, 2, 3))
        or os.path.exists(os.path.join(SAVE_DIR, "savegame.json"))
        or os.path.exists("savegame.json")
    )
