from utils import clear_screen, print_header
from player import MAX_INVENTORY_SLOTS

SHOP_ITEMS = [
    {"name": "Healing Potion",   "type": "consumable", "key": "Healing Potion",   "amount": 1, "price": 15,  "desc": "Heilt 10 HP"},
    {"name": "Großes Heiltrank", "type": "consumable", "key": "Großes Heiltrank", "amount": 1, "price": 35,  "desc": "Heilt 25 HP"},
    {"name": "Energie-Kristall", "type": "consumable", "key": "Energie-Kristall", "amount": 1, "price": 25,  "desc": "+15 Energie"},
    {"name": "Stärketrank",      "type": "consumable", "key": "Stärketrank",      "amount": 1, "price": 40,  "desc": "+3 ATK (Kampf)"},
    {"name": "Antidot",          "type": "consumable", "key": "Antidot",          "amount": 1, "price": 12,  "desc": "Entfernt Blutung"},
    {"name": "Kurzschwert",      "type": "weapon",     "key": "Kurzschwert",      "attack": 3, "price": 40},
    {"name": "Langschwert",      "type": "weapon",     "key": "Langschwert",      "attack": 6, "price": 80},
    {"name": "Lederrüstung",     "type": "chest",      "key": "Lederrüstung",     "armor": 2,  "price": 35},
    {"name": "Kettenhemd",       "type": "chest",      "key": "Kettenhemd",       "armor": 4,  "price": 70},
]

def shop_menu(player):
    while True:
        clear_screen()
        print_header("Händler")
        used_slots = player.inventory_count()
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots")
        print("-" * 48)

        for i, item in enumerate(SHOP_ITEMS):
            affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"

            # Platz-Check für Anzeige
            if item["type"] == "consumable":
                has_space = player.can_add_consumable(item["key"])
            else:
                has_space = player.has_inventory_space()
            space_warn = "" if has_space else " 🎒VOLL"

            if item["type"] == "consumable":
                desc = f"{item['name']:<22} ({item['desc']:<20})  {item['price']:>3} Gold  {affordable}{space_warn}"
            elif item["type"] == "weapon":
                desc = f"{item['name']:<22} (ATK: +{item['attack']:<2})              {item['price']:>3} Gold  {affordable}{space_warn}"
            else:
                desc = f"{item['name']:<22} (DEF: +{item['armor']:<2})              {item['price']:>3} Gold  {affordable}{space_warn}"

            print(f"[{i+1}] {desc}")

        print(f"\n[0] Verlassen")
        choice = input("\nWas möchtest du kaufen? ")

        if choice == "0":
            break
        if not choice.isdigit():
            continue

        idx = int(choice) - 1
        if not (0 <= idx < len(SHOP_ITEMS)):
            print("Ungültige Auswahl.")
            input("ENTER...")
            continue

        item = SHOP_ITEMS[idx]

        if player.inventory["Gold"] < item["price"]:
            print("Nicht genug Gold!")
            input("ENTER...")
            continue

        # Inventar-Platz prüfen
        if item["type"] == "consumable":
            if not player.can_add_consumable(item["key"]):
                print(f"🎒 Inventar voll! ({used_slots}/{MAX_INVENTORY_SLOTS} Slots belegt)")
                input("ENTER...")
                continue
        else:
            if not player.has_inventory_space():
                print(f"🎒 Inventar voll! ({used_slots}/{MAX_INVENTORY_SLOTS} Slots belegt)")
                input("ENTER...")
                continue

        player.inventory["Gold"] -= item["price"]

        if item["type"] == "consumable":
            if "Consumables" not in player.inventory:
                player.inventory["Consumables"] = {}
            key = item["key"]
            player.inventory["Consumables"][key] = player.inventory["Consumables"].get(key, 0) + item["amount"]
            print(f"✅ Du kaufst {item['amount']}x {item['name']}!")

        elif item["type"] == "weapon":
            equip_item = {"name": item["name"], "type": "weapon", "attack": item["attack"]}
            player.inventory["Equipment"].append(equip_item)
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        elif item["type"] == "chest":
            equip_item = {"name": item["name"], "type": "chest", "armor": item["armor"]}
            player.inventory["Equipment"].append(equip_item)
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        input("ENTER...")
