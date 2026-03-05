from utils import clear_screen, print_header
from save import save_game
from shop import shop_menu
from player import MAX_INVENTORY_SLOTS


def camp_menu(player):
    while True:
        clear_screen()
        print_header("Lagerfeuer - Pause")
        used_slots = player.inventory_count()
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(consumables.values())
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
    from loot_tables import CONSUMABLE_DEFS, JUNK_DEFS
    while True:
        clear_screen()
        print_header("Dein Inventar")
        used_slots = player.inventory_count()
        print(f"🎒 Slots: {used_slots}/{MAX_INVENTORY_SLOTS}")
        print()

        # --- Consumables ---
        consumables = player.inventory.get("Consumables", {})
        print("[ Verbrauchsgegenstände ]")
        if consumables:
            for key, count in consumables.items():
                cdef      = CONSUMABLE_DEFS.get(key, {})
                emoji     = cdef.get("emoji", "🧪")
                desc      = cdef.get("desc", "")
                max_stack = cdef.get("max_stack", 99)
                print(f"  {emoji} {key:<22} {count}/{max_stack:<3}  — {desc}")
        else:
            print("  (keine)")

        print()

        # --- Junk ---
        junk = player.inventory.get("Junk", {})
        print("[ Schrott (nur zum Verkaufen) ]")
        if junk:
            for key, count in junk.items():
                jdef  = JUNK_DEFS.get(key, {})
                emoji = jdef.get("emoji", "🗑️")
                sell  = jdef.get("sell", 1)
                print(f"  {emoji} {key:<22} x{count}  — {sell} Gold/Stk")
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
    from loot_tables import CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_SELL_PRICES

    while True:
        clear_screen()
        print_header("Inventar verkaufen")
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Slots: {player.inventory_count()}/{MAX_INVENTORY_SLOTS}")
        print("-" * 52)

        sell_list = []  # (category, key_or_idx, price_per_unit, current_count, display_name)

        # Consumables
        consumables = player.inventory.get("Consumables", {})
        if consumables:
            print("[ Verbrauchsgegenstände ]")
        for key, count in list(consumables.items()):
            cdef  = CONSUMABLE_DEFS.get(key, {})
            emoji = cdef.get("emoji", "🧪")
            price = cdef.get("sell", 1)
            idx   = len(sell_list)
            total = price * count
            print(f"  [{idx}] {emoji} {key:<22} x{count}  →  {price} Gold/Stk  ({total} Gold gesamt)")
            sell_list.append(("consumable", key, price, count))

        # Junk
        junk = player.inventory.get("Junk", {})
        if junk:
            print("\n[ Schrott ]")
        for key, count in list(junk.items()):
            jdef  = JUNK_DEFS.get(key, {})
            emoji = jdef.get("emoji", "🗑️")
            price = jdef.get("sell", 1)
            idx   = len(sell_list)
            total = price * count
            print(f"  [{idx}] {emoji} {key:<22} x{count}  →  {price} Gold/Stk  ({total} Gold gesamt)")
            sell_list.append(("junk", key, price, count))

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
            sell_list.append(("equipment", item['name'], price, 1))

        if not sell_list:
            print("  Nichts zu verkaufen.")
            input("\n(ENTER)")
            return

        # Gesamtwert berechnen
        total_value = 0
        for entry in sell_list:
            cat, key, price, count = entry
            total_value += price * count

        print(f"\n[A] Alles verkaufen ({total_value} Gold)  |  [Z] Zurück")
        choice = input("\nWas verkaufen? ").lower()

        if choice == 'z':
            break

        elif choice == 'a':
            earned = 0
            for key, count in list(consumables.items()):
                earned += CONSUMABLE_DEFS.get(key, {}).get("sell", 1) * count
            consumables.clear()
            for key, count in list(junk.items()):
                earned += JUNK_DEFS.get(key, {}).get("sell", 1) * count
            junk.clear()
            for item in list(equip_items):
                earned += EQUIPMENT_SELL_PRICES.get(item['name'], 5)
            equip_items.clear()
            player.inventory["Gold"] += earned
            print(f"\n✅ Alles verkauft! +{earned} Gold.")
            print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
            input("(ENTER)")
            break

        elif choice.isdigit():
            idx = int(choice)
            if not (0 <= idx < len(sell_list)):
                print("Ungültige Auswahl.")
                input("ENTER...")
                continue

            cat, key, price, count = sell_list[idx]

            if cat in ("consumable", "junk"):
                store = consumables if cat == "consumable" else junk
                cur   = store.get(key, 0)
                if cur == 0:
                    input("Nicht mehr vorhanden. ENTER...")
                    continue

                if cur > 1:
                    print(f"\nWie viele {key} verkaufen? (1–{cur}, ENTER = alle)")
                    amt_in = input("> ").strip()
                    if amt_in == "":
                        amount = cur
                    elif amt_in.isdigit() and 1 <= int(amt_in) <= cur:
                        amount = int(amt_in)
                    else:
                        print("Ungültige Menge.")
                        input("ENTER...")
                        continue
                else:
                    amount = 1

                earned = price * amount
                store[key] -= amount
                if store[key] <= 0:
                    del store[key]
                player.inventory["Gold"] += earned
                print(f"\n✅ {amount}x {key} verkauft für {earned} Gold.")

            elif cat == "equipment":
                real_idx = next((i for i, e in enumerate(equip_items) if e['name'] == key), None)
                if real_idx is None:
                    input("Item nicht mehr vorhanden. ENTER...")
                    continue
                equip_items.pop(real_idx)
                player.inventory["Gold"] += price
                print(f"\n✅ {key} verkauft für {price} Gold.")

            print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
            input("(ENTER)")
