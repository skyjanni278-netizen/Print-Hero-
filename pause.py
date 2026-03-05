from utils import clear_screen, print_header
from save import save_game
from shop import shop_menu

def camp_menu(player):
    while True:
        clear_screen()
        print_header("Lagerfeuer - Pause")
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(v for v in consumables.values())
        print(f"Spieler: {player.name} | HP: {player.hp}/{player.max_hp} | Gold: {player.inventory['Gold']}")
        print(f"Waffe: {player.equipment['weapon']['name']} (+{player.equipment['weapon']['attack']} DMG)")
        print(f"Rüstung: {player.equipment['chest']['name']} (+{player.equipment['chest']['armor']} DEF)")
        print(f"💊 Gegenstände: {total_consumables}")
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
    while True:
        clear_screen()
        print_header("Dein Inventar")

        # --- Consumables anzeigen ---
        consumables = player.inventory.get("Consumables", {})
        from loot_tables import CONSUMABLE_DEFS
        print("[ Verbrauchsgegenstände ]")
        if consumables:
            for key, count in consumables.items():
                cdef = CONSUMABLE_DEFS.get(key, {})
                emoji = cdef.get("emoji", "🧪")
                desc  = cdef.get("desc", "")
                print(f"  {emoji} {key:<22} x{count}  — {desc}")
        else:
            print("  (keine)")

        print()

        # --- Equipment anzeigen ---
        equip_items = player.inventory["Equipment"]
        print("[ Ausrüstung ]")
        if equip_items:
            for i, item in enumerate(equip_items):
                value = item['attack'] if item['type'] == 'weapon' else item['armor']
                type_label = "ATK" if item['type'] == 'weapon' else "DEF"
                print(f"  [{i}] {item['name']} ({type_label}: +{value})")
        else:
            print("  (keine)")

        print(f"\n[Nummer] Ausrüstung anlegen  |  [Z] Zurück")
        choice = input("\nDeine Wahl: ").lower()

        if choice == 'z':
            break

        if choice.isdigit():
            idx = int(choice)
            if idx < len(equip_items):
                new_item = equip_items.pop(idx)
                slot = new_item["type"]
                old_item = player.equipment[slot]
                if old_item["name"] not in ("Fäuste", "Lumpen"):
                    equip_items.append(old_item)
                player.equipment[slot] = new_item
                print(f"\nDu trägst nun {new_item['name']}!")
                input("(ENTER)")
