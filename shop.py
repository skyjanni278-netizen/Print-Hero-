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
    from loot_tables import CONSUMABLE_DEFS
    while True:
        clear_screen()
        print_header("Händler")
        used_slots = player.inventory_count()
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots")
        print("-" * 52)

        for i, item in enumerate(SHOP_ITEMS):
            affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"

            if item["type"] == "consumable":
                has_space  = player.can_add_consumable(item["key"])
                cur        = player.inventory.get("Consumables", {}).get(item["key"], 0)
                max_stack  = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                stack_info = f"({cur}/{max_stack})"
                warn       = "" if has_space else " 🎒VOLL"
                desc = f"{item['name']:<22} {stack_info:<8} {item['desc']:<20}  {item['price']:>3} Gold  {affordable}{warn}"
            else:
                has_space = player.has_inventory_space()
                warn      = "" if has_space else " 🎒VOLL"
                if item["type"] == "weapon":
                    desc = f"{item['name']:<22}          ATK +{item['attack']:<2}              {item['price']:>3} Gold  {affordable}{warn}"
                else:
                    desc = f"{item['name']:<22}          DEF +{item['armor']:<2}              {item['price']:>3} Gold  {affordable}{warn}"

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
            print("❌ Nicht genug Gold!")
            input("ENTER...")
            continue

        if item["type"] == "consumable":
            added = player.add_consumable(item["key"], item["amount"])
            if added == 0:
                max_stack = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                cur = player.inventory.get("Consumables", {}).get(item["key"], 0)
                if cur >= max_stack:
                    print(f"❌ Stapel voll! ({cur}/{max_stack})")
                else:
                    print(f"🎒 Inventar voll! ({player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots)")
                input("ENTER...")
                continue
            player.inventory["Gold"] -= item["price"]
            print(f"✅ Du kaufst {added}x {item['name']}!")

        elif item["type"] in ("weapon", "chest"):
            if not player.has_inventory_space():
                print(f"🎒 Inventar voll! ({player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots)")
                input("ENTER...")
                continue
            player.inventory["Gold"] -= item["price"]
            if item["type"] == "weapon":
                player.inventory["Equipment"].append({"name": item["name"], "type": "weapon", "attack": item["attack"]})
            else:
                player.inventory["Equipment"].append({"name": item["name"], "type": "chest",  "armor":  item["armor"]})
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        input("ENTER...")
