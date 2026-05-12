import random
from core.player import Character
from ui.utils import clear_screen, print_header
from ui.pause import camp_menu
from core.save import load_game, get_save_slots
from systems.dungeon import run_dungeon
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


def _offer_ng_plus(player):
    from content.loot_tables import EQUIPMENT_DEFS
    clear_screen()
    print_header("⭐ New Game+ verfügbar!")
    ng_next = player.ng_plus + 1
    mult    = round(1.3 ** ng_next, 2)
    kept = [i["name"] for i in player.inventory["Equipment"]
            if EQUIPMENT_DEFS.get(i["name"], {}).get("rarity") == "legendary"]
    print(f"Du hast Level 10 erreicht! Starte New Game+ Runde {ng_next}.")
    print(f"\nGegnerskalierung: ×{mult} HP und ATK")
    print(f"Du behältst: {player.inventory['Gold']} Gold")
    if kept:
        print(f"Legendäre Items: {', '.join(kept)}")
    else:
        print("Legendäre Items: keine im Inventar")
    print("\nAlles andere (Level, Skills, Equipment) wird zurückgesetzt.")
    print("\n[J] New Game+ starten   [N] Weiterspielen (kein Reset)")
    while True:
        c = input("\nDeine Wahl: ").lower()
        if c == 'j':
            player.start_ng_plus()
            for m in check_all(player, {"event": "ng_plus"}):
                print(m)
            clear_screen()
            print_header("⭐ New Game+ gestartet!")
            print(f"Runde {player.ng_plus} beginnt. Viel Erfolg, Held!")
            input("(ENTER)")
            break
        elif c == 'n':
            break


def _handle_defeat(player):
    player.stats["deaths"] += 1
    print(f"\nGame Over! {player.name} wurde besiegt.")


def main():
    player = _slot_menu()

    while player.is_alive():
        camp_menu(player)

        result = run_dungeon(player)
        player.shop_stock = []  # Sortiment erneuert sich nach jedem Dungeon

        if result == "defeated":
            _handle_defeat(player)
            break
        elif result == "completed":
            ach_msgs = check_all(player, {"event": "gold_check"})
            for m in ach_msgs:
                print(m)
            if player.level >= 10:
                _offer_ng_plus(player)
        # 'fled' → zurück zum Lagerfeuer


if __name__ == "__main__":
    main()
