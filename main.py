import random
from player import Character
from utils import clear_screen, print_header
from combat import generate_enemy_group, combat, collect_loot
from pause import camp_menu
from save import load_game, save_exists
from events import trigger_event

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


def main():
    clear_screen()

    if save_exists():
        print("Spielstand gefunden!")
        choice = input("[L] Laden  [N] Neues Spiel: ").lower()
        if choice == 'l':
            player = load_game()
        else:
            diff   = _choose_difficulty()
            start_hp = DIFFICULTY_SETTINGS[diff]["start_hp"]
            player = Character("Hero", hp=start_hp, attack=10)
            player.difficulty = diff
    else:
        diff   = _choose_difficulty()
        start_hp = DIFFICULTY_SETTINGS[diff]["start_hp"]
        player = Character("Hero", hp=start_hp, attack=10)
        player.difficulty = diff

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

            total_xp = int(sum(e.xp_value for e in enemy_group) * player.next_fight_xp_mult)
            player.next_fight_xp_mult = 1.0
            print(f"\nGruppe besiegt! Du erhältst {total_xp} XP!")
            player.xp += total_xp
            player.check_level_up()
            input("\nDu ziehst weiter... (ENTER)")

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
