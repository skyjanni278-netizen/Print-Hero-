import random
from player import Character
from utils import clear_screen, print_header
from combat import generate_enemy_group, combat, collect_loot
from pause import camp_menu
from save import load_game, save_exists


def main():
    clear_screen()

    if save_exists():
        print("Spielstand gefunden!")
        choice = input("[L] Laden  [N] Neues Spiel: ").lower()
        player = load_game() if choice == 'l' else Character("Hero", hp=30, attack=10)
    else:
        player = Character("Hero", hp=30, attack=10)

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

            gold_before = player.inventory["Gold"]
            loot_lines = collect_loot(player, enemy_group)
            player.stats["gold_earned"] += player.inventory["Gold"] - gold_before

            if loot_lines:
                print("\nBeute:")
                for line in loot_lines:
                    print(line)
            else:
                print("\n- Keine Beute gefunden -")

            total_xp = sum(e.xp_value for e in enemy_group)
            print(f"\nGruppe besiegt! Du erhältst {total_xp} XP!")
            player.xp += total_xp
            player.check_level_up()
            input("\nDu ziehst weiter... (ENTER)")

        elif result == "defeat":
            player.stats["deaths"] += 1
            print(f"\nGame Over! {player.name} wurde besiegt.")
            break

        elif result == "fled":
            input("\nDu ziehst weiter... (ENTER)")


if __name__ == "__main__":
    main()
