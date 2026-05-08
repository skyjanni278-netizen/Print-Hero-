import random
from player import Character
from utils import clear_screen, print_header
from combat import generate_enemy_group, combat, collect_loot
from pause import camp_menu
from save import load_game, save_exists
from events import trigger_event
from achievements import check_all

DIFFICULTY_SETTINGS = {
    "easy":   {"hp_mult": 0.80, "atk_mult": 0.85, "start_hp": 35, "label": "Einfach  🟢"},
    "normal": {"hp_mult": 1.00, "atk_mult": 1.00, "start_hp": 30, "label": "Normal   🟡"},
    "hard":   {"hp_mult": 1.25, "atk_mult": 1.20, "start_hp": 25, "label": "Schwer   🔴"},
}


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
    from classes import choose_class, apply_class
    diff     = _choose_difficulty()
    class_id = choose_class()
    from classes import CLASS_DEFS
    cdef     = CLASS_DEFS[class_id]
    player   = Character("Hero", hp=cdef["start_hp"], attack=cdef["start_atk"])
    player.difficulty = diff
    apply_class(player, class_id)
    return player


def _offer_ng_plus(player):
    from utils import clear_screen, print_header
    from loot_tables import EQUIPMENT_DEFS
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
        enemy_group = generate_enemy_group(player)
        clear_screen()
        print(f"--- Eine Gruppe erscheint: {', '.join(e.name for e in enemy_group)}! ---")
        input("Bereit machen... (ENTER)")

        result = combat(player, enemy_group)
        player.reset_combat_modifiers()  # Temporäre Kampfboni zurücksetzen

        if result == "victory":
            clear_screen()
            print_header("Kampf-Ergebnis")

            player.stats["fights"] += 1
            player.stats["kills"]  += len(enemy_group)

            potions_before = sum(player.inventory.get("Consumables", {}).values())
            gold_before    = player.inventory["Gold"]
            loot_lines     = collect_loot(player, enemy_group)
            player.stats["gold_earned"] += player.inventory["Gold"] - gold_before

            # Achievement: Legendary-Loot Check
            from loot_tables import EQUIPMENT_DEFS
            got_leg = any(
                EQUIPMENT_DEFS.get(i["name"], {}).get("rarity") == "legendary"
                for i in player.inventory.get("Equipment", [])
            )

            if loot_lines:
                print("\nBeute:")
                for line in loot_lines:
                    print(line)
            else:
                print("\n- Keine Beute gefunden -")

            total_xp = int(sum(e.xp_value for e in enemy_group) * player.next_fight_xp_mult)
            player.next_fight_xp_mult = 1.0
            print(f"\nGruppe besiegt! Du erhältst {total_xp} XP!")
            player.xp += total_xp
            player.check_level_up()

            # Achievement-Checks
            potions_after = sum(player.inventory.get("Consumables", {}).values())
            ach_msgs = check_all(player, {
                "event": "victory",
                "enemies": enemy_group,
                "potions_before": potions_before,
                "potions_after":  potions_after,
            })
            ach_msgs += check_all(player, {"event": "level_up", "level": player.level})
            ach_msgs += check_all(player, {"event": "loot", "got_legendary": got_leg})
            ach_msgs += check_all(player, {"event": "gold_check"})
            for m in ach_msgs:
                print(m)

            input("\nDu ziehst weiter... (ENTER)")

            if player.level >= 10:
                _offer_ng_plus(player)

            player.fights_until_event -= 1
            if player.fights_until_event <= 0:
                trigger_event(player)
                player.fights_until_event = random.randint(2, 3)

        elif result == "defeat":
            player.stats["deaths"] += 1
            print(f"\nGame Over! {player.name} wurde besiegt.")
            break

        elif result == "fled":
            input("\nDu ziehst weiter... (ENTER)")


if __name__ == "__main__":
    main()
