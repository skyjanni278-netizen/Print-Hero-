import random
from core.player import Character
from ui.utils import clear_screen, print_header
from ui.pause import camp_menu
from core.save import load_game, get_save_slots
from systems.dungeon import run_dungeon
from systems.world_map import run_zone_boss, check_all_zones_cleared, endscreen
from systems.achievements import check_all
from config import DIFFICULTY_SETTINGS


def _choose_difficulty():
    print("\nWähle deinen Schwierigkeitsgrad:")
    print("  [E] Einfach  — Gegner schwächer,  +5 Start-HP")
    print("  [N] Normal   — Standardwerte")
    print("  [H] Schwer   — Gegner stärker,    -5 Start-HP")
    mapping = {"e": "easy", "n": "normal", "h": "hard"}
    while True:
        c = input("Deine Wahl [E/N/H]: ").lower()
        if c in mapping:
            return mapping[c]


def _new_game(slot: int):
    from content.classes import choose_class, apply_class, CLASS_DEFS
    diff     = _choose_difficulty()
    class_id = choose_class()
    cdef     = CLASS_DEFS[class_id]
    player   = Character("Hero", hp=cdef["start_hp"], attack=cdef["start_atk"])
    player.difficulty = diff
    apply_class(player, class_id)
    player.save_slot = slot
    return player


def _slot_menu():
    from content.classes import CLASS_DEFS
    from config import DIFFICULTY_SETTINGS
    while True:
        clear_screen()
        print_header("🗡️  Print-Hero  —  Spielstand wählen")
        slots = get_save_slots()
        for info in slots:
            s = info["slot"]
            if info["exists"]:
                pclass  = info.get("player_class", "warrior")
                emoji   = CLASS_DEFS.get(pclass, {}).get("emoji", "")
                ng      = info.get("ng_plus", 0)
                ng_tag  = f" NG+{ng}" if ng > 0 else ""
                diff    = DIFFICULTY_SETTINGS.get(info.get("difficulty", "normal"), {}).get("label", "Normal")
                print(f"  [{s}] Slot {s}:  {emoji} Level {info['level']}{ng_tag}  |  {diff}")
            else:
                print(f"  [{s}] Slot {s}:  — Leer —  [Neues Spiel]")
        print("\n  [Q] Beenden")
        choice = input("\nDeine Wahl: ").strip().lower()
        if choice == "q":
            exit()
        if choice.isdigit() and 1 <= int(choice) <= 3:
            slot = int(choice)
            info = slots[slot - 1]
            if info["exists"]:
                clear_screen()
                print_header(f"Slot {slot}")
                pclass = info.get("player_class", "warrior")
                emoji  = CLASS_DEFS.get(pclass, {}).get("emoji", "")
                ng     = info.get("ng_plus", 0)
                ng_tag = f" NG+{ng}" if ng > 0 else ""
                print(f"  {emoji} Level {info['level']}{ng_tag}")
                print("\n  [L] Laden   [N] Neu starten (überschreibt Slot)   [Z] Zurück")
                c = input("\nDeine Wahl: ").strip().lower()
                if c == "l":
                    return load_game(slot)
                elif c == "n":
                    return _new_game(slot)
            else:
                return _new_game(slot)


def _handle_defeat(player):
    player.stats["deaths"] += 1
    clear_screen()
    print_header("💀 Game Over")
    print(f"\n  {player.name} wurde besiegt.\n")
    print(f"  Kämpfe gewonnen : {player.stats.get('fights', 0)}")
    print(f"  Gegner besiegt  : {player.stats.get('kills', 0)}")
    print(f"  Dungeons fertig : {player.stats.get('dungeons_completed', 0)}")
    input("\n(ENTER)")


def main():
    player = _slot_menu()

    while player.is_alive():
        action = camp_menu(player)

        if action == "quit":
            break

        player.shop_stock = []

        if action == "boss":
            result = run_zone_boss(player, player.current_zone)
        else:
            result = run_dungeon(player)

        if result == "defeat":
            _handle_defeat(player)
            break

        if result in ("completed", "victory"):
            for m in check_all(player, {"event": "gold_check"}):
                print(m)

            if check_all_zones_cleared(player):
                outcome = endscreen(player)
                if outcome == "ng_plus":
                    continue
                # "continue" → freies Erkunden, Loop geht weiter


if __name__ == "__main__":
    main()
