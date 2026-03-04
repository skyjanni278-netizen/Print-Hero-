import random
from monsters import Zombie, Slime, Goblin, Skeleton, Dragon, roll_rank
from utils import clear_screen, print_header
from loot_tables import roll_loot, apply_loot


def generate_enemy_group(player):
    count = random.randint(1, 3)
    return [create_enemy(player) for _ in range(count)]


def create_enemy(player):
    """Wählt einen zufälligen Mob-Typ und würfelt seinen Rang."""
    if player.level < 3:
        classes = [Zombie, Slime, Goblin]
        weights = [15, 50, 20]
    elif player.level < 5:
        classes = [Zombie, Slime, Goblin, Skeleton]
        weights = [30, 25, 25, 20]
    else:
        classes = [Zombie, Slime, Goblin, Skeleton, Dragon]
        weights = [25, 13, 17, 25, 13]

    mob_class = random.choices(classes, weights=weights, k=1)[0]
    rank      = roll_rank(player.level)
    return mob_class(rank=rank)


def combat(player, enemy_list):
    while player.is_alive() and any(e.is_alive() for e in enemy_list):
        clear_screen()
        print_header("Kampf-Modus")

        # Player stats
        print(f"{player.name:<4} HP: {player.hp}/{player.max_hp} | Energie: {player.energy}/{player.max_energy}")
        print(f"     LVL: {player.level}    | XP: {player.xp}/{player.xp_to_level_up}")
        print("-" * 30)
        print("Inventar: ")
        print(f" Heilflaschen: {player.inventory.get('Healing Potions', 0)} | Gold: {player.inventory.get('Gold', 0)}")
        print("-" * 30)

        # Show all enemies
        print("GEGNER:")
        for i, e in enumerate(enemy_list):
            rank_label = f"[Rang {e.rank}]" if hasattr(e, "rank") else ""
            status = f"HP: {e.hp}/{e.max_hp}" if e.is_alive() else "BESIEGT"
            print(f"[{i+1}] {e.name:<22} {rank_label:<10} {status}")

        print("=" * 30)
        choice = input("\n[A] Angreifen, [S] Himmelsschlag 20 E, [R] Rundumschlag 15 E, [C] Cleave 10 E \n[H] Heilen, [F] Fliehen \n[Q] Beenden \nDeine Wahl: ").lower()

        if choice not in ['a', 's', 'r', 'c', 'h', 'f', 'q']:
            print("\nUngültige Taste! Bitte wähle eine der angezeigten Optionen.")
            input("ENTER...")
            continue

        # Target selection for single-target attacks
        if choice in ['a', 's', 'c']:
            try:
                target_index = int(input("Welchen Gegner angreifen? (Nummer): ")) - 1
                clear_screen()
                print_header("Kampf-Ergebnis")
                if 0 <= target_index < len(enemy_list) and enemy_list[target_index].is_alive():
                    target = enemy_list[target_index]
                    if choice == 'a':
                        print(player.attack_target(target))
                    elif choice == 's':
                        print(player.heavenstrike(target))
                    elif choice == 'c':
                        print(player.cleave(target))
                else:
                    print("Ungültiges Ziel oder Gegner bereits besiegt!")
                    input("ENTER...")
                    continue
            except ValueError:
                print("Bitte gib eine gültige Zahl ein!")
                input("ENTER...")
                continue

        elif choice == 'r':
            clear_screen()
            print_header("Kampf-Ergebnis")
            living_enemies = [e for e in enemy_list if e.is_alive()]
            print(player.whirlwind(living_enemies))

        elif choice == 'h':
            clear_screen()
            print_header("Kampf-Ergebnis")
            heal(player)

        elif choice == 'f':
            clear_screen()
            print("Du fliehst aus dem Kampf!")
            return "fled"

        elif choice == 'q':
            clear_screen()
            print("Du verlässt das Spiel. Auf Wiedersehen!")
            exit()

        # Bleed tick
        for e in enemy_list:
            if e.is_alive():
                bleed_msg = e.check_bleed()
                if bleed_msg:
                    print(bleed_msg)

        # Enemy attacks
        for e in enemy_list:
            if not player.is_alive():
                break
            if e.is_alive():
                print(e.attack_target(player))

        player.regenerate()
        input("\nNächste Runde (ENTER)...")

    if not any(e.is_alive() for e in enemy_list):
        return "victory"
    return "defeat"


def collect_loot(player, enemy_group) -> list:
    """
    Sammelt Loot von allen besiegten Gegnern über das zentrale Loot-System.
    Gibt alle Loot-Zeilen als Liste von Strings zurück.
    """
    all_messages = []
    for enemy in enemy_group:
        rank       = getattr(enemy, "rank", 1)
        rolls      = getattr(enemy, "loot_rolls", 1)
        loot_items = roll_loot(rank=rank, rolls=rolls)
        msgs       = apply_loot(player, loot_items)
        if msgs:
            all_messages.append(f"\n  [{enemy.name}]")
            all_messages.extend(msgs)
    return all_messages


def heal(player):
    if player.inventory.get("Healing Potions", 0) > 0:
        heal_amount = 10
        print(f"{player.name} benutzt eine Heilflasche und heilt sich um {heal_amount} HP!")
        player.hp = min(player.max_hp, player.hp + heal_amount)
        player.inventory["Healing Potions"] -= 1
    else:
        print("Keine Heilflaschen mehr!")
