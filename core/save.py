import json
import os
from core.player import Character
from ui.utils import console

_ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_DIR  = os.path.join(_ROOT, "saves")
META_PATH = os.path.join(SAVE_DIR, "meta_save.json")
RUN_PATH  = os.path.join(SAVE_DIR, "run_save.json")


# ── Meta-Save (permanent, überlebt jeden Run) ─────────────────

def _default_meta() -> dict:
    return {
        "runenessenz":    0,
        "achievements":   [],
        "spiegel_state":  {},   # v3.0 Phase 3
        "unlocked_runen": [],   # v3.0 Phase 4
        "boss_runen_dropped": [],   # Zonen-Bosse, die ihre Rune bereits vergeben haben
        "lifetime_stats": {
            "runs_started":  0,
            "runs_won":      0,
            "runs_lost":     0,
            "essenz_earned": 0,
        },
    }


def load_meta() -> dict:
    if not os.path.exists(META_PATH):
        return _default_meta()
    try:
        with open(META_PATH, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        console.print("  [red]meta_save.json ist beschädigt — starte mit leerem Meta-Stand.[/red]")
        console.print(f"  [dim]Fehler: {e}[/dim]")
        input("  (ENTER)")
        return _default_meta()
    meta = _default_meta()
    lifetime = {**meta["lifetime_stats"], **data.get("lifetime_stats", {})}
    meta.update(data)
    meta["lifetime_stats"] = lifetime
    return meta


def save_meta(meta: dict):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)


# Einzige erlaubten Wege, Runenessenz zu ändern — nie meta["runenessenz"] direkt anfassen.
def add_runenessenz(meta: dict, amount: int):
    meta["runenessenz"] = meta.get("runenessenz", 0) + amount
    ls = meta.setdefault("lifetime_stats", {})
    ls["essenz_earned"] = ls.get("essenz_earned", 0) + amount
    save_meta(meta)


def spend_runenessenz(meta: dict, amount: int) -> bool:
    if meta.get("runenessenz", 0) < amount:
        return False
    meta["runenessenz"] -= amount
    save_meta(meta)
    return True


def sync_achievements(player, meta: dict):
    unlocked = set(meta.get("achievements", [])) | set(getattr(player, "achievements", set()))
    meta["achievements"] = sorted(unlocked)


# ── Run-Save (aktueller Run, bei Tod/Sieg gelöscht) ───────────

def run_exists() -> bool:
    return os.path.exists(RUN_PATH)


def save_run(player, quiet: bool = False):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(RUN_PATH, "w") as f:
        json.dump(player.to_dict(), f, indent=2)
    if not quiet:
        console.print("  [green]💾 Run gespeichert![/green]")


def load_run(meta: dict = None):
    if not run_exists():
        return None
    try:
        with open(RUN_PATH, "r") as f:
            data = json.load(f)
        player = Character.from_dict(data)
    except (json.JSONDecodeError, OSError, KeyError, TypeError) as e:
        console.print("\n  [red]run_save.json ist beschädigt und kann nicht geladen werden.[/red]")
        console.print(f"  [dim]Fehler: {e}[/dim]")
        input("  (ENTER)")
        return None
    if meta is not None:
        player.achievements |= set(meta.get("achievements", []))
    console.print("  [green]📂 Run geladen![/green]")
    return player


def delete_run():
    if os.path.exists(RUN_PATH):
        os.remove(RUN_PATH)
