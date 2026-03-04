from utils import clear_screen, print_header
from save import save_game
from shop import shop_menu

def camp_menu(player):
    while True:
        clear_screen()
        print_header("Lagerfeuer - Pause")
        print(f"Spieler: {player.name} | HP: {player.hp}/{player.max_hp} | Gold: {player.inventory['Gold']}")
        print(f"Waffe: {player.equipment['weapon']['name']} (+{player.equipment['weapon']['attack']} DMG)")
        print(f"Rüstung: {player.equipment['chest']['name']} (+{player.equipment['chest']['armor']} DEF)")
        print("-" * 30)
        print("[I] Inventar & Ausrüsten")
        print("[K] Händler besuchen")
        print("[S] Speichern")
        print("[W] Weiter zum nächsten Kampf")
        print("[Q] Beenden")

        choice = input("\nDeine Wahl: ").lower()
        if choice == 'i':
            inventory_menu(player)
        elif choice == 'k':
            shop_menu(player)
        elif choice == 's':
            save_game(player)
            input("(ENTER)")
        elif choice == 'q':
            clear_screen()
            print("Du verlässt das Spiel. Auf Wiedersehen!")
            exit()
        elif choice == 'w':
            break


def inventory_menu(player):
    clear_screen()
    print_header("Dein Inventar")
    items = player.inventory["Equipment"]

    if not items:
        print("Dein Rucksack ist leer.")
        input("\nZurück... (ENTER)")
        return

    for i, item in enumerate(items):
        value = item['attack'] if item['type'] == 'weapon' else item['armor']
        type_label = "ATK" if item['type'] == 'weapon' else "DEF"
        print(f"[{i}] {item['name']} ({type_label}: +{value})")

    print(f"[{len(items)}] Zurück")

    choice = input("\nWas möchtest du anlegen? ")
    if choice.isdigit():
        idx = int(choice)
        if idx < len(items):
            new_item = items.pop(idx)
            slot = new_item["type"]

            # Put old item back into inventory
            old_item = player.equipment[slot]
            if old_item["name"] not in ("Fäuste", "Lumpen"):
                items.append(old_item)

            # Equip new item
            player.equipment[slot] = new_item
            print(f"\nDu trägst nun {new_item['name']}!")
            input("(ENTER)")
