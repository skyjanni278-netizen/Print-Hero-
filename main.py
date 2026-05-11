import random
from core.player import Character
from ui.utils import clear_screen, print_header
from ui.pause import camp_menu
from core.save import load_game, save_exists
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


def _new_game():
    from content.classes import choose_class, apply_class
    diff     = _choose_difficulty()
    class_id = choose_class()
    from content.classes import CLASS_DEFS
    cdef     = CLASS_DEFS[class_id]
    player   = Character("Hero", hp=cdef["start_hp"], attack=cdef["start_atk"])
    player.difficulty = diff
    apply_class(player, class_id)
    return player


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
    clear_screen()

    if save_exists():
        print("Spielstand gefunden!")
        choice = input("[L] Laden  [N] Neues Spiel: ").lower()
        if choice == 'l':
            player = load_game()
        else:
            player = _new_game()
    else:
        player = _new_game()

    while player.is_alive():
        camp_menu(player)

        result = run_dungeon(player)

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
