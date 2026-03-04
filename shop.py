from utils import clear_screen, print_header

# Alle Waren die der Händler verkauft
SHOP_ITEMS = [
    {"name": "Healing Potion",      "type": "consumable", "key": "Healing Potions", "amount": 1,  "effect": "heal",   "value": 10,  "price": 15},
    {"name": "Großes Heiltrank",    "type": "consumable", "key": "Healing Potions", "amount": 3,  "effect": "heal",   "value": 10,  "price": 35},
    {"name": "Kurzschwert",         "type": "weapon",     "key": "Kurzschwert",     "attack": 3,                                    "price": 40},
    {"name": "Langschwert",         "type": "weapon",     "key": "Langschwert",     "attack": 6,                                    "price": 80},
    {"name": "Lederrüstung",        "type": "chest",      "key": "Lederrüstung",    "armor": 2,                                     "price": 35},
    {"name": "Kettenhemd",          "type": "chest",      "key": "Kettenhemd",      "armor": 4,                                     "price": 70},
]

def shop_menu(player):
    while True:
        clear_screen()
        print_header("Händler")
        print(f"Dein Gold: {player.inventory['Gold']} 🪙")
        print("-" * 40)

        for i, item in enumerate(SHOP_ITEMS):
            affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"
            
            if item["type"] == "consumable":
                desc = f"{item['name']:<22} ({item['amount']}x Heiltrank)   {item['price']} Gold  {affordable}"
            elif item["type"] == "weapon":
                desc = f"{item['name']:<22} (ATK: +{item['attack']})          {item['price']} Gold  {affordable}"
            else:
                desc = f"{item['name']:<22} (DEF: +{item['armor']})          {item['price']} Gold  {affordable}"
            
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

        # Kauf durchführen
        player.inventory["Gold"] -= item["price"]

        if item["type"] == "consumable":
            player.inventory["Healing Potions"] = player.inventory.get("Healing Potions", 0) + item["amount"]
            print(f"✅ Du kaufst {item['amount']}x Heiltrank!")

        elif item["type"] == "weapon":
            equip_item = {"name": item["name"], "type": "weapon", "attack": item["attack"]}
            player.inventory["Equipment"].append(equip_item)
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        elif item["type"] == "chest":
            equip_item = {"name": item["name"], "type": "chest", "armor": item["armor"]}
            player.inventory["Equipment"].append(equip_item)
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        input("ENTER...")