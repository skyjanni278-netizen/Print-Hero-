from utils import clear_screen, print_header
from save import save_game
from shop import shop_menu
from player import MAX_INVENTORY_SLOTS


def camp_menu(player):
    while True:
        clear_screen()
        print_header("Lagerfeuer - Pause")
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(v for v in consumables.values())
        used_slots = player.inventory_count()
        print(f"Spieler: {player.name} | HP: {player.hp}/{player.max_hp} | Gold: {player.inventory['Gold']} 🪙")
        print(f"Waffe:   {player.equipment['weapon']['name']} (+{player.equipment['weapon']['attack']} DMG)")
        print(f"Rüstung: {player.equipment['chest']['name']} (+{player.equipment['chest']['armor']} DEF)")
        print(f"🎒 Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots  |  💊 Gegenstände: {total_consumables}")
        print("-" * 30)
        print("[I] Inventar & Ausrüsten")
        print("[V] Inventar verkaufen")
        print("[K] Händler besuchen")
        print("[S] Speichern")
        print("[W] Weiter zum nächsten Kampf")
        print("[Q] Beenden")

        choice = input("\nDeine Wahl: ").lower()
        if choice == 'i':
            inventory_menu(player)
        elif choice == 'v':
            sell_menu(player)
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
        used_slots = player.inventory_count()
        print(f"🎒 Slots: {used_slots}/{MAX_INVENTORY_SLOTS}")
        print()

        # --- Consumables ---
        consumables = player.inventory.get("Consumables", {})
        from loot_tables import CONSUMABLE_DEFS
        print("[ Verbrauchsgegenstände ]")
        if consumables:
            for key, count in consumables.items():
                cdef  = CONSUMABLE_DEFS.get(key, {})
                emoji = cdef.get("emoji", "🧪")
                desc  = cdef.get("desc", "")
                print(f"  {emoji} {key:<22} x{count}  — {desc}")
        else:
            print("  (keine)")

        print()

        # --- Equipment ---
        equip_items = player.inventory["Equipment"]
        print("[ Ausrüstung (Nummer zum Anlegen) ]")
        if equip_items:
            for i, item in enumerate(equip_items):
                value      = item['attack'] if item['type'] == 'weapon' else item['armor']
                type_label = "ATK" if item['type'] == 'weapon' else "DEF"
                print(f"  [{i}] {item['name']} ({type_label}: +{value})")
        else:
            print("  (keine)")

        print(f"\n[Nummer] Anlegen  |  [Z] Zurück")
        choice = input("\nDeine Wahl: ").lower()

        if choice == 'z':
            break

        if choice.isdigit():
            idx = int(choice)
            if idx < len(equip_items):
                new_item = equip_items.pop(idx)
                slot     = new_item["type"]
                old_item = player.equipment[slot]
                if old_item["name"] not in ("Fäuste", "Lumpen"):
                    equip_items.append(old_item)
                player.equipment[slot] = new_item
                print(f"\nDu trägst nun {new_item['name']}!")
                input("(ENTER)")


def sell_menu(player):
    """Verkauf-Menü: Consumables und Equipment gegen Gold verkaufen."""
    from loot_tables import CONSUMABLE_DEFS, EQUIPMENT_SELL_PRICES

    while True:
        clear_screen()
        print_header("Inventar verkaufen")
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Slots: {player.inventory_count()}/{MAX_INVENTORY_SLOTS}")
        print("-" * 48)

        # Alle verkäuflichen Items sammeln und nummerieren
        sell_list = []  # (label, sell_fn, preview_gold)

        # Consumables
        consumables = player.inventory.get("Consumables", {})
        if consumables:
            print("[ Verbrauchsgegenstände ]")
        for key, count in list(consumables.items()):
            cdef  = CONSUMABLE_DEFS.get(key, {})
            emoji = cdef.get("emoji", "🧪")
            price = cdef.get("sell", 1)
            total = price * count
            idx   = len(sell_list)
            print(f"  [{idx}] {emoji} {key:<22} x{count}  →  {price} Gold/Stk  ({total} Gold gesamt)")
            sell_list.append(("consumable", key, price, count))

        # Equipment
        equip_items = player.inventory["Equipment"]
        if equip_items:
            print("\n[ Ausrüstung ]")
        for i, item in enumerate(equip_items):
            value      = item['attack'] if item['type'] == 'weapon' else item['armor']
            type_label = "ATK" if item['type'] == 'weapon' else "DEF"
            price      = EQUIPMENT_SELL_PRICES.get(item['name'], 5)
            idx        = len(sell_list)
            print(f"  [{idx}] {item['name']:<22} ({type_label}: +{value})  →  {price} Gold")
            sell_list.append(("equipment", i, price, item['name']))

        if not sell_list:
            print("  Nichts zu verkaufen.")
            input("\n(ENTER)")
            return

        print(f"\n[A] Alles verkaufen  |  [Z] Zurück")
        choice = input("\nWas verkaufen? ").lower()

        if choice == 'z':
            break

        elif choice == 'a':
            # Alles auf einmal verkaufen
            total_gold = 0
            # Consumables
            for key, count in list(consumables.items()):
                price = CONSUMABLE_DEFS.get(key, {}).get("sell", 1)
                total_gold += price * count
            consumables.clear()
            # Equipment
            for item in list(equip_items):
                total_gold += EQUIPMENT_SELL_PRICES.get(item['name'], 5)
            equip_items.clear()
            player.inventory["Gold"] += total_gold
            print(f"\n✅ Alles verkauft! Du erhältst {total_gold} Gold.")
            print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
            input("(ENTER)")
            break

        elif choice.isdigit():
            idx = int(choice)
            if not (0 <= idx < len(sell_list)):
                print("Ungültige Auswahl.")
                input("ENTER...")
                continue

            entry = sell_list[idx]

            if entry[0] == "consumable":
                _, key, price, count = entry
                # Einzeln oder alle verkaufen?
                if count > 1:
                    print(f"\nWie viele {key} verkaufen? (1–{count}, ENTER = alle)")
                    amt_input = input("> ").strip()
                    if amt_input == "":
                        amount = count
                    elif amt_input.isdigit() and 1 <= int(amt_input) <= count:
                        amount = int(amt_input)
                    else:
                        print("Ungültige Menge.")
                        input("ENTER...")
                        continue
                else:
                    amount = 1

                earned = price * amount
                consumables[key] -= amount
                if consumables[key] <= 0:
                    del consumables[key]
                player.inventory["Gold"] += earned
                print(f"\n✅ {amount}x {key} verkauft für {earned} Gold.")
                print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
                input("(ENTER)")

            elif entry[0] == "equipment":
                _, equip_idx, price, name = entry
                # equip_idx kann sich durch vorherige Verkäufe verschoben haben — neu suchen
                real_idx = next((i for i, e in enumerate(equip_items) if e['name'] == name), None)
                if real_idx is None:
                    print("Item nicht mehr vorhanden.")
                    input("ENTER...")
                    continue
                equip_items.pop(real_idx)
                player.inventory["Gold"] += price
                print(f"\n✅ {name} verkauft für {price} Gold.")
                print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
                input("(ENTER)")
