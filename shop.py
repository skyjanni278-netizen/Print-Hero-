from utils import clear_screen, print_header
from player import MAX_INVENTORY_SLOTS

# Shop verkauft Equipment bis Rare — Epic/Legendary nur durch Loot
SHOP_ITEMS = [
    # Consumables
    {"name": "Healing Potion",   "type": "consumable", "key": "Healing Potion",   "amount": 1, "price": 15,  "desc": "Heilt 10 HP"},
    {"name": "Großes Heiltrank", "type": "consumable", "key": "Großes Heiltrank", "amount": 1, "price": 35,  "desc": "Heilt 25 HP"},
    {"name": "Energie-Kristall", "type": "consumable", "key": "Energie-Kristall", "amount": 1, "price": 25,  "desc": "+15 Energie"},
    {"name": "Stärketrank",      "type": "consumable", "key": "Stärketrank",      "amount": 1, "price": 40,  "desc": "+3 ATK (Kampf)"},
    {"name": "Antidot",          "type": "consumable", "key": "Antidot",          "amount": 1, "price": 12,  "desc": "Entfernt Blutung"},
    # Waffen (Common→Rare)
    {"name": "Kurzschwert",      "type": "equipment",  "key": "Kurzschwert",      "price":  40},
    {"name": "Langschwert",      "type": "equipment",  "key": "Langschwert",      "price":  80},
    {"name": "Kriegshammer",     "type": "equipment",  "key": "Kriegshammer",     "price": 120},
    {"name": "Runenschwert",     "type": "equipment",  "key": "Runenschwert",     "price": 200},
    # Rüstungen (Common→Rare)
    {"name": "Lederrüstung",     "type": "equipment",  "key": "Lederrüstung",     "price":  35},
    {"name": "Kettenhemd",       "type": "equipment",  "key": "Kettenhemd",       "price":  70},
    {"name": "Plattenpanzer",    "type": "equipment",  "key": "Plattenpanzer",    "price": 120},
    {"name": "Runenrüstung",     "type": "equipment",  "key": "Runenrüstung",     "price": 200},
    # Helme (Common→Rare)
    {"name": "Lederkappe",       "type": "equipment",  "key": "Lederkappe",       "price":  25},
    {"name": "Eisenhelm",        "type": "equipment",  "key": "Eisenhelm",        "price":  45},
    {"name": "Stahlhelm",        "type": "equipment",  "key": "Stahlhelm",        "price":  90},
    {"name": "Runenhelm",        "type": "equipment",  "key": "Runenhelm",        "price": 180},
    # Schuhe (Common→Rare)
    {"name": "Lederstiefel",          "type": "equipment",  "key": "Lederstiefel",          "price":  20},
    {"name": "Eisenstiefel",          "type": "equipment",  "key": "Eisenstiefel",          "price":  40},
    {"name": "Schnellläuferstiefel",  "type": "equipment",  "key": "Schnellläuferstiefel",  "price":  85},
    {"name": "Runenstiefel",          "type": "equipment",  "key": "Runenstiefel",          "price": 170},
]

SLOT_LABEL = {"weapon": "Waffe", "chest": "Rüstung", "head": "Helm"}

def shop_menu(player):
    from loot_tables import CONSUMABLE_DEFS, EQUIPMENT_DEFS, RARITY_LABEL

    # Sortiere nach Slot für übersichtliche Anzeige
    sections = [
        ("💊 Verbrauchsgegenstände", [i for i in SHOP_ITEMS if i["type"] == "consumable"]),
        ("🗡️  Waffen",               [i for i in SHOP_ITEMS if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "weapon"]),
        ("🛡️  Rüstungen",             [i for i in SHOP_ITEMS if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "chest"]),
        ("🪖 Helme",                  [i for i in SHOP_ITEMS if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "head"]),
        ("👟 Schuhe",                 [i for i in SHOP_ITEMS if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "feet"]),
    ]
    # Globaler Index-Map
    indexed = [(item, i) for i, item in enumerate(SHOP_ITEMS)]

    while True:
        clear_screen()
        print_header("Händler")
        used_slots = player.inventory_count()
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots")
        print(f"Ausrüstet: {player.equipment['weapon']['name']} / {player.equipment['chest']['name']} / {player.equipment['head']['name']}")
        print("-" * 56)

        global_idx = 0
        for section_name, items in sections:
            if not items:
                continue
            print(f"\n{section_name}")
            for item in items:
                affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"

                if item["type"] == "consumable":
                    cur        = player.inventory.get("Consumables", {}).get(item["key"], 0)
                    max_stack  = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                    has_space  = player.can_add_consumable(item["key"])
                    warn       = "" if has_space else " 🎒VOLL"
                    stack_info = f"({cur}/{max_stack})"
                    line = f"  [{global_idx:>2}] {item['name']:<22} {stack_info:<8} {item['desc']:<18} {item['price']:>4} Gold  {affordable}{warn}"
                else:
                    edef    = EQUIPMENT_DEFS.get(item["key"], {})
                    emoji   = edef.get("emoji", "⚔️")
                    rarity  = edef.get("rarity", "common")
                    _, rbadge = RARITY_LABEL.get(rarity, ("?", "⬜"))
                    has_space = player.has_inventory_space()
                    warn    = "" if has_space else " 🎒VOLL"
                    if edef.get("slot") == "weapon":
                        stat = f"ATK +{edef['attack']}"
                    else:
                        stat = f"DEF +{edef['armor']}"
                    line = f"  [{global_idx:>2}] {rbadge}{emoji} {item['name']:<22} {stat:<10} {edef.get('desc',''):<22} {item['price']:>4} Gold  {affordable}{warn}"
                print(line)
                global_idx += 1

        print(f"\n[0] Verlassen")
        choice = input("\nWas möchtest du kaufen? ")

        if choice == "0":
            break
        if not choice.isdigit():
            continue

        idx = int(choice)
        if not (1 <= idx <= len(SHOP_ITEMS)):
            # idx is 0-based in SHOP_ITEMS, but display starts at 0 which is Verlassen
            # Rebuild: display indices start at 0 for first item
            print("Ungültige Auswahl.")
            input("ENTER...")
            continue

        # Map display index (0-based for items) to SHOP_ITEMS
        item = SHOP_ITEMS[idx - 1] if idx >= 1 else None
        # Actually display indices are 0-based for items (global_idx starts at 0)
        # Let's just use the input directly as 0-based index into SHOP_ITEMS
        item = None
        display_idx = int(choice)
        flat = []
        for _, items in sections:
            flat.extend(items)
        if 0 <= display_idx < len(flat):
            item = flat[display_idx]
        else:
            print("Ungültige Auswahl.")
            input("ENTER...")
            continue

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

        elif item["type"] == "equipment":
            if not player.has_inventory_space():
                print(f"🎒 Inventar voll! ({player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots)")
                input("ENTER...")
                continue
            edef = EQUIPMENT_DEFS.get(item["key"], {})
            slot = edef.get("slot", "weapon")
            equip = {"name": item["name"], "type": slot}
            if slot == "weapon":
                equip["attack"] = edef["attack"]
            else:
                equip["armor"] = edef["armor"]
            player.inventory["Gold"] -= item["price"]
            player.inventory["Equipment"].append(equip)
            print(f"✅ {item['name']} wurde deinem Inventar hinzugefügt!")

        input("ENTER...")
