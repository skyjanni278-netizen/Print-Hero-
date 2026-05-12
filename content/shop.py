import random
from ui.utils import clear_screen, print_header
from core.player import MAX_INVENTORY_SLOTS


SHOP_CATALOGUE = [
    # ── Consumables ───────────────────────────────────────────
    {"name": "Healing Potion",   "type": "consumable", "key": "Healing Potion",   "amount": 1, "price":  12, "desc": "Heilt 10 HP",         "min_level": 1},
    {"name": "Antidot",          "type": "consumable", "key": "Antidot",          "amount": 1, "price":  10, "desc": "Entfernt Blutung & Gift", "min_level": 1},
    {"name": "Energie-Kristall", "type": "consumable", "key": "Energie-Kristall", "amount": 1, "price":  20, "desc": "+15 Energie",          "min_level": 1},
    {"name": "Großes Heiltrank", "type": "consumable", "key": "Großes Heiltrank", "amount": 1, "price":  32, "desc": "Heilt 25 HP",          "min_level": 3},
    {"name": "Stärketrank",      "type": "consumable", "key": "Stärketrank",      "amount": 1, "price":  38, "desc": "+3 ATK (Kampf)",       "min_level": 3},
    {"name": "Elixier",          "type": "consumable", "key": "Elixier",          "amount": 1, "price":  70, "desc": "Heilt 40 HP",          "min_level": 5},
    {"name": "Phönixfeder",      "type": "consumable", "key": "Phönixfeder",      "amount": 1, "price":  85, "desc": "15 HP + Blutung weg",  "min_level": 5},
    # ── Waffen ────────────────────────────────────────────────
    {"name": "Kurzschwert",      "type": "equipment", "key": "Kurzschwert",      "price":  35, "min_level": 1, "max_level": 4},
    {"name": "Schattendolch",    "type": "equipment", "key": "Schattendolch",    "price":  90, "min_level": 3, "max_level": 7},
    {"name": "Langschwert",      "type": "equipment", "key": "Langschwert",      "price":  75, "min_level": 3, "max_level": 6},
    {"name": "Kriegshammer",     "type": "equipment", "key": "Kriegshammer",     "price": 115, "min_level": 3, "max_level": 8},
    {"name": "Sturmklinge",      "type": "equipment", "key": "Sturmklinge",      "price": 160, "min_level": 5, "max_level": 8},
    {"name": "Runenschwert",     "type": "equipment", "key": "Runenschwert",     "price": 190, "min_level": 5},
    # ── Rüstungen ─────────────────────────────────────────────
    {"name": "Lederrüstung",     "type": "equipment", "key": "Lederrüstung",     "price":  30, "min_level": 1, "max_level": 4},
    {"name": "Kettenhemd",       "type": "equipment", "key": "Kettenhemd",       "price":  65, "min_level": 3, "max_level": 6},
    {"name": "Schattenrüstung",  "type": "equipment", "key": "Schattenrüstung",  "price": 145, "min_level": 4, "max_level": 8},
    {"name": "Plattenpanzer",    "type": "equipment", "key": "Plattenpanzer",    "price": 115, "min_level": 3, "max_level": 8},
    {"name": "Runenrüstung",     "type": "equipment", "key": "Runenrüstung",     "price": 190, "min_level": 5},
    # ── Helme ─────────────────────────────────────────────────
    {"name": "Lederkappe",       "type": "equipment", "key": "Lederkappe",       "price":  22, "min_level": 1, "max_level": 4},
    {"name": "Eisenhelm",        "type": "equipment", "key": "Eisenhelm",        "price":  42, "min_level": 1, "max_level": 5},
    {"name": "Stahlhelm",        "type": "equipment", "key": "Stahlhelm",        "price":  85, "min_level": 3, "max_level": 8},
    {"name": "Schattenhelm",     "type": "equipment", "key": "Schattenhelm",     "price": 120, "min_level": 4, "max_level": 8},
    {"name": "Runenhelm",        "type": "equipment", "key": "Runenhelm",        "price": 170, "min_level": 5},
    # ── Schuhe ────────────────────────────────────────────────
    {"name": "Lederstiefel",           "type": "equipment", "key": "Lederstiefel",           "price":  18, "min_level": 1, "max_level": 4},
    {"name": "Eisenstiefel",           "type": "equipment", "key": "Eisenstiefel",           "price":  35, "min_level": 1, "max_level": 5},
    {"name": "Kriegsstiefel",          "type": "equipment", "key": "Kriegsstiefel",          "price":  60, "min_level": 3, "max_level": 7},
    {"name": "Schattenstiefel",        "type": "equipment", "key": "Schattenstiefel",        "price":  55, "min_level": 3, "max_level": 7},
    {"name": "Schnellläuferstiefel",   "type": "equipment", "key": "Schnellläuferstiefel",   "price":  80, "min_level": 3, "max_level": 8},
    {"name": "Runenstiefel",           "type": "equipment", "key": "Runenstiefel",           "price": 160, "min_level": 5},
]


def refresh_shop_stock(player):
    """Pick 2 consumables + 1 item per equipment slot from level-appropriate catalogue."""
    from content.loot_tables import EQUIPMENT_DEFS
    lvl = player.level
    available = [i for i in SHOP_CATALOGUE if i.get("min_level", 1) <= lvl <= i.get("max_level", 99)]

    consumables = [i for i in available if i["type"] == "consumable"]
    weapons     = [i for i in available if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "weapon"]
    chests      = [i for i in available if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "chest"]
    heads       = [i for i in available if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "head"]
    feet_items  = [i for i in available if i["type"] == "equipment" and EQUIPMENT_DEFS.get(i["key"], {}).get("slot") == "feet"]

    stock = []
    stock += random.sample(consumables, min(2, len(consumables)))
    stock += random.sample(weapons,     min(1, len(weapons)))
    stock += random.sample(chests,      min(1, len(chests)))
    stock += random.sample(heads,       min(1, len(heads)))
    stock += random.sample(feet_items,  min(1, len(feet_items)))

    player.shop_stock = [i["name"] for i in stock]


def get_shop_items(player_level: int) -> list:
    result = []
    for item in SHOP_CATALOGUE:
        min_lvl = item.get("min_level", 1)
        max_lvl = item.get("max_level", 99)
        if min_lvl <= player_level <= max_lvl:
            result.append(item)
    return result


def get_next_unlock(player_level: int) -> dict:
    from content.loot_tables import EQUIPMENT_DEFS
    unlocks = {}
    for item in SHOP_CATALOGUE:
        min_lvl = item.get("min_level", 1)
        if min_lvl <= player_level:
            continue  # bereits freigeschaltet
        # Bestimme Slot-Gruppe
        if item["type"] == "consumable":
            group = "consumable"
        else:
            edef  = EQUIPMENT_DEFS.get(item["key"], {})
            group = edef.get("slot", "unknown")
        # Nur das nächste (kleinste min_level) pro Gruppe merken
        if group not in unlocks or min_lvl < unlocks[group][1]:
            unlocks[group] = (item["name"], min_lvl)
    return unlocks


def shop_menu(player):
    from content.loot_tables import CONSUMABLE_DEFS, EQUIPMENT_DEFS, RARITY_LABEL

    SECTION_ORDER = [
        ("💊 Verbrauchsgegenstände", "consumable", None),
        ("🗡️  Waffen",               "equipment",  "weapon"),
        ("🛡️  Rüstungen",             "equipment",  "chest"),
        ("🪖 Helme",                  "equipment",  "head"),
        ("👟 Schuhe",                 "equipment",  "feet"),
    ]

    while True:
        clear_screen()
        print_header("Händler")

        lvl        = player.level
        used_slots = player.inventory_count()
        w = player.equipment['weapon']
        c = player.equipment['chest']
        h = player.equipment['head']
        f = player.equipment['feet']

        print(f"Gold: {player.inventory['Gold']} 🪙  |  Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots  |  LVL {lvl}")
        print(f"Ausrüstet: {w['name']} / {c['name']} / {h['name']} / {f['name']}")
        print("-" * 62)

        stock = getattr(player, "shop_stock", [])
        if not stock:
            refresh_shop_stock(player)
            stock = player.shop_stock
        all_lvl_items = get_shop_items(lvl)
        active_items  = [i for i in all_lvl_items if i["name"] in stock]
        next_unlocks  = get_next_unlock(lvl)

        # Baue flache Liste für Indexierung (in Sections-Reihenfolge)
        flat = []
        for _, item_type, slot_filter in SECTION_ORDER:
            for item in active_items:
                if item["type"] != item_type:
                    continue
                if slot_filter is not None:
                    edef = EQUIPMENT_DEFS.get(item["key"], {})
                    if edef.get("slot") != slot_filter:
                        continue
                flat.append(item)

        # Anzeige
        for sec_name, item_type, slot_filter in SECTION_ORDER:
            section_items = []
            for item in flat:
                if item["type"] != item_type:
                    continue
                if slot_filter is not None:
                    edef = EQUIPMENT_DEFS.get(item["key"], {})
                    if edef.get("slot") != slot_filter:
                        continue
                section_items.append(item)

            # Unlock-Vorschau für diese Sektion
            group_key = "consumable" if item_type == "consumable" else slot_filter
            upcoming  = next_unlocks.get(group_key)

            if not section_items and not upcoming:
                continue

            print(f"\n{sec_name}")

            for item in section_items:
                idx        = flat.index(item) + 1  # 1-basiert, damit [0] = Verlassen frei bleibt
                affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"

                if item["type"] == "consumable":
                    cur        = player.inventory.get("Consumables", {}).get(item["key"], 0)
                    max_stack  = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                    has_space  = player.can_add_consumable(item["key"])
                    warn       = "" if has_space else " 🎒VOLL"
                    stack_info = f"({cur}/{max_stack})"
                    line = f"  [{idx:>2}] {item['name']:<24} {stack_info:<8} {item['desc']:<20} {item['price']:>4} Gold  {affordable}{warn}"
                else:
                    edef     = EQUIPMENT_DEFS.get(item["key"], {})
                    emoji    = edef.get("emoji", "⚔️")
                    rarity   = edef.get("rarity", "common")
                    _, rbadge = RARITY_LABEL.get(rarity, ("?", "⬜"))
                    has_space = player.has_inventory_space()
                    warn     = "" if has_space else " 🎒VOLL"
                    stat     = f"ATK +{edef['attack']}" if edef.get("slot") == "weapon" else f"DEF +{edef['armor']}"
                    line = f"  [{idx:>2}] {rbadge}{emoji} {item['name']:<24} {stat:<10} {edef.get('desc',''):<22} {item['price']:>4} Gold  {affordable}{warn}"
                print(line)

            # 🔒 Vorschau nächster Unlock
            if upcoming:
                unlock_name, unlock_lvl = upcoming
                print(f"  🔒 {unlock_name:<24} (freigeschalten ab LVL {unlock_lvl})")

        if not flat:
            print("\n  (Keine Items verfügbar)")

        print(f"\n  🔄 Sortiment wechselt nach jedem Dungeon")
        print(f"[0] Verlassen")
        choice = input("\nWas möchtest du kaufen? ")

        if choice == "0":
            break
        if not choice.isdigit():
            continue

        display_idx = int(choice)
        if not (1 <= display_idx <= len(flat)):
            print("Ungültige Auswahl.")
            input("ENTER...")
            continue

        item = flat[display_idx - 1]  # zurück auf 0-basiert

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
