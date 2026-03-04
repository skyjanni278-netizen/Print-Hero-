import random
from player import Character
from utils import clear_screen, print_header
from combat import generate_enemy_group, combat
from pause import camp_menu
from save import load_game, save_exists


def main():
    clear_screen()
    player = Character("Hero", hp=30, attack=10)

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

        if result == "victory":
            clear_screen()
            print_header("Kampf-Ergebnis")
            print("\nBeute:")
            loot_found = False

            for enemy in enemy_group:
                if random.random() < 0.5:
                    for item_name, (min_qty, max_qty) in enemy.loot_table.items():
                        amount = random.randint(min_qty, max_qty)
                        if amount > 0:
                            player.add_loot(item_name, amount)
                            loot_found = True

                # Equipment drop
                if hasattr(enemy, "equipment_table") and random.random() < enemy.equipment_drop_chance:
                    slot = random.choice(["weapon", "chest"])
                    pick = random.choice(enemy.equipment_table[slot])
                    if slot == "weapon":
                        item = {"name": pick[0], "type": "weapon", "attack": pick[1]}
                    else:
                        item = {"name": pick[0], "type": "chest", "armor": pick[1]}
                    print(f"✨ WOW! {enemy.name} hat {item['name']} fallen gelassen!")
                    player.inventory["Equipment"].append(item)
                    loot_found = True

            if not loot_found:
                print("- Keine Beute gefunden -")

            total_xp = sum(e.xp_value for e in enemy_group)
            print(f"\nGruppe besiegt! Du erhältst {total_xp} XP!")
            player.xp += total_xp
            player.check_level_up()
            input("\nDu ziehst weiter... (ENTER)")

        elif result == "defeat":
            print(f"\nGame Over! {player.name} wurde besiegt.")
            break

        elif result == "fled":
            input("\nDu ziehst weiter... (ENTER)")


if __name__ == "__main__":
    main()
