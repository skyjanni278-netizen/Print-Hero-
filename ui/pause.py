from ui.utils import clear_screen, print_header
from core.save import save_game
from content.shop import shop_menu
from core.player import MAX_INVENTORY_SLOTS


def camp_menu(player):
    while True:
        clear_screen()
        print_header("Lagerfeuer - Pause")
        used_slots = player.inventory_count()
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(consumables.values())
        w = player.equipment['weapon']
        c = player.equipment['chest']
        h = player.equipment['head']
        f = player.equipment['feet']
        from config import DIFFICULTY_SETTINGS
        from content.classes import CLASS_DEFS
        diff_label  = DIFFICULTY_SETTINGS.get(getattr(player, "difficulty", "normal"), {}).get("label", "Normal")
        ng          = getattr(player, "ng_plus", 0)
        ng_tag      = f" | ⭐ NG+{ng}" if ng > 0 else ""
        pclass      = getattr(player, "player_class", "warrior")
        class_emoji = CLASS_DEFS.get(pclass, {}).get("emoji", "")
        class_name  = CLASS_DEFS.get(pclass, {}).get("name", "")
        print(f"Spieler: {player.name} {class_emoji} {class_name} | HP: {player.hp}/{player.max_hp} | Gold: {player.inventory['Gold']} 🪙 | {diff_label}{ng_tag}")
        print(f"ATK: {player.get_total_attack():<4} | DEF: {player.get_total_armor()}")
        print(f"Waffe:   {w['name']} (+{w['attack']} ATK)")
        print(f"Rüstung: {c['name']} (+{c['armor']} DEF)")
        print(f"Helm:    {h['name']} (+{h['armor']} DEF)")
        print(f"Schuhe:  {f['name']} (+{f['armor']} DEF)")
        from content.loot_tables import get_active_sets
        active_sets = get_active_sets(player)
        if active_sets:
            parts = []
            for sname, sdef, count, bonus in active_sets:
                star = "✅" if count == 4 else f"{count}/4"
                parts.append(f"{sdef['emoji']} {sname} {star}: {bonus['desc']}")
            print("Set:     " + "  |  ".join(parts))
        from systems.zones import ZONE_DEFS
        zone_id    = getattr(player, "current_zone", "wald")
        zdef       = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
        zone_line  = f"{zdef['emoji']} {zdef['name']}"
        print(f"🎒 Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots  |  💊 Gegenstände: {total_consumables}  |  🗺️ Zone: {zone_line}")
        print("-" * 50)
        print("  ⚔️  Ausrüstung              🧙 Charakter")
        print("  ─────────────────────      ─────────────────────")
        print(f"  [I] Inventar & Ausrüsten   [F] Fertigkeiten ({player.skill_points} Pkt)")
        print(f"  [U] Equipment aufwerten    [E] Errungenschaften ({len(player.achievements)}/10)")
        print(f"  [V] Inventar verkaufen     [T] Statistiken")
        print(f"  [K] Händler besuchen       [Z] Zone wählen  ({zone_line})")
        print("-" * 50)
        print("  [S] Speichern   [W] Weiter zum Kampf   [Q] Beenden")

        choice = input("\nDeine Wahl: ").lower()
        if choice == 'i':
            inventory_menu(player)
        elif choice == 'u':
            upgrade_menu(player)
        elif choice == 'v':
            sell_menu(player)
        elif choice == 'k':
            shop_menu(player)
        elif choice == 'z':
            zone_menu(player)
        elif choice == 'f':
            from systems.skilltree import skill_menu
            skill_menu(player)
        elif choice == 'e':
            from systems.achievements import achievements_menu
            achievements_menu(player)
        elif choice == 't':
            stats_menu(player)
        elif choice == 's':
            save_game(player)
            input("(ENTER)")
        elif choice == 'q':
            clear_screen()
            print("Du verlässt das Spiel. Auf Wiedersehen!")
            exit()
        elif choice == 'w':
            break


def stats_menu(player):
    clear_screen()
    print_header("Statistiken")
    s = player.stats
    kd = f"{s['kills']}/{s['deaths']}" if s['deaths'] > 0 else str(s['kills'])
    print(f"  ⚔️  Kämpfe gewonnen    : {s['fights']}")
    print(f"  💀  Kills / Tode       : {kd}")
    print(f"  🗡️  Schaden ausgeteilt : {s['damage_dealt']}")
    print(f"  🛡️  Schaden erhalten   : {s['damage_taken']}")
    print(f"  💰  Gold verdient      : {s['gold_earned']}")
    print(f"  🧪  Tränke benutzt     : {s['potions_used']}")
    input("\n(ENTER)")


_UPGRADE_COSTS   = [50, 120, 250]   # Kosten für Stufe 1, 2, 3
_STARTER_ITEMS   = {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}
_SLOT_LABELS     = {"weapon": "Waffe", "chest": "Rüstung", "head": "Helm", "feet": "Schuhe"}
_MAX_UPGRADE_LVL = 3


def upgrade_menu(player):
    while True:
        clear_screen()
        print_header("Equipment aufwerten")
        print(f"Gold: {player.inventory['Gold']} 🪙\n")
        print(f"{'Slot':<10} {'Item':<24} {'Stufe':<8} {'Bonus':<12} {'Kosten'}")
        print("-" * 62)

        upgradeable = []
        for slot, label in _SLOT_LABELS.items():
            item     = player.equipment[slot]
            lvl      = player.equipment_upgrades.get(slot, 0)
            is_start = item["name"] in _STARTER_ITEMS

            if is_start:
                print(f"  {label:<10} {item['name']:<24} —        (Starter-Item, nicht aufwertbar)")
                continue

            if slot == "weapon":
                bonus_str = f"+{lvl * 2} ATK"
                next_bonus = f"+{(lvl + 1) * 2} ATK"
            else:
                bonus_str = f"+{lvl} DEF"
                next_bonus = f"+{lvl + 1} DEF"

            if lvl >= _MAX_UPGRADE_LVL:
                print(f"  [{len(upgradeable)}] {label:<10} {item['name']:<24} MAX      {bonus_str:<12} —")
            else:
                cost = _UPGRADE_COSTS[lvl]
                affordable = "✅" if player.inventory["Gold"] >= cost else "❌"
                print(f"  [{len(upgradeable)}] {label:<10} {item['name']:<24} Stufe {lvl}  {bonus_str:<12} {cost} Gold {affordable}")
                upgradeable.append((slot, lvl, cost))

        if not upgradeable:
            print("\nKein Item mehr aufwertbar.")
            input("\n(ENTER)")
            break

        print("\n[Z] Zurück")
        choice = input("\nWelches Item aufwerten? ").strip().lower()

        if choice == "z":
            break
        if choice.isdigit() and 0 <= int(choice) < len(upgradeable):
            slot, lvl, cost = upgradeable[int(choice)]
            if player.inventory["Gold"] < cost:
                print("Zu wenig Gold!")
                input("(ENTER)")
                continue
            player.inventory["Gold"]        -= cost
            player.equipment_upgrades[slot] += 1
            new_lvl = player.equipment_upgrades[slot]
            item    = player.equipment[slot]
            if slot == "weapon":
                bonus_desc = f"+{new_lvl * 2} ATK gesamt"
            else:
                bonus_desc = f"+{new_lvl} DEF gesamt"
            print(f"\n⬆️  {item['name']} auf Stufe {new_lvl} aufgewertet! ({bonus_desc})")
            print(f"   Gold verbleibend: {player.inventory['Gold']} 🪙")
            input("(ENTER)")


def _equip_line(item):
    from content.loot_tables import EQUIPMENT_DEFS, RARITY_LABEL, SET_DEFS
    edef    = EQUIPMENT_DEFS.get(item["name"], {})
    emoji   = edef.get("emoji", "⚔️")
    rarity  = edef.get("rarity", "common")
    rlabel, rbadge = RARITY_LABEL.get(rarity, ("?", "⬜"))
    slot    = item.get("type") or edef.get("slot", "weapon")
    slot_labels = {"weapon": "Waffe", "chest": "Rüstung", "head": "Helm", "feet": "Schuhe"}
    slot_label  = slot_labels.get(slot, slot)
    if slot == "weapon":
        stat = f"ATK +{item.get('attack', 0)}"
    else:
        stat = f"DEF +{item.get('armor', 0)}"
    set_tag = ""
    for sname, sdef in SET_DEFS.items():
        if item["name"] in sdef["pieces"]:
            set_tag = f" {sdef['emoji']}{sname}"
            break
    return f"{rbadge}{emoji} {item['name']:<24} {stat:<10} [{rlabel}] ({slot_label}){set_tag}"


def inventory_menu(player):
    from content.loot_tables import CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_DEFS, RARITY_LABEL, get_active_sets
    while True:
        clear_screen()
        print_header("Dein Inventar")
        used_slots = player.inventory_count()
        print(f"🎒 Slots: {used_slots}/{MAX_INVENTORY_SLOTS}")
        w = player.equipment['weapon']
        c = player.equipment['chest']
        h = player.equipment['head']
        f = player.equipment['feet']
        print(f"Angelegt: {player.equipment['weapon']['name']} | {c['name']} | {h['name']} | {f['name']}")
        active_sets = get_active_sets(player)
        if active_sets:
            for sname, sdef, count, bonus in active_sets:
                star = "✅ VOLL" if count == 4 else f"{count}/4"
                print(f"  {sdef['emoji']} {sname} {star} → {bonus['desc']}")
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
        print("[ Schrott ]")
        if junk:
            for key, count in junk.items():
                jdef  = JUNK_DEFS.get(key, {})
                emoji = jdef.get("emoji", "🗑️")
                sell  = jdef.get("sell", 1)
                print(f"  {emoji} {key:<22} x{count}  — {sell} Gold/Stk")
        else:
            print("  (keine)")
        print()

        # --- Equipment nach Slot gruppiert ---
        equip_items = player.inventory["Equipment"]
        SLOT_ORDER = [
            ("weapon", "🗡️  Waffe"),
            ("chest",  "🛡️  Rüstung"),
            ("head",   "🪖 Helm"),
            ("feet",   "👟 Schuhe"),
        ]
        _STARTER = {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}

        # Block 1: Alle angelegten Items auf einen Blick
        print("[ Angelegt ]")
        for slot_key, slot_label in SLOT_ORDER:
            equipped = player.equipment[slot_key]
            print(f"  ★ {slot_label:<12} {_equip_line(equipped)}")

        # Block 2: Inventar-Alternativen zum Anlegen
        print("\n[ Inventar — Nummer zum Anlegen ]")
        indexed_items = []

        for slot_key, slot_label in SLOT_ORDER:
            inv_for_slot = [it for it in equip_items if it["type"] == slot_key]
            if not inv_for_slot:
                continue
            print(f"\n  {slot_label}")
            for item in inv_for_slot:
                n = len(indexed_items)
                indexed_items.append(item)
                print(f"  [{n:>2}] {_equip_line(item)}")

        if not indexed_items:
            print("  (keine Ausrüstung im Inventar)")

        print(f"\n[Nummer] Anlegen  |  [Z] Zurück")
        choice = input("\nDeine Wahl: ").lower()

        if choice == 'z':
            break

        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(indexed_items):
                new_item = indexed_items[idx]
                equip_items.remove(new_item)
                slot     = new_item["type"]
                old_item = player.equipment[slot]
                if old_item["name"] not in _STARTER:
                    equip_items.append(old_item)
                player.equipment[slot] = new_item
                player.equipment_upgrades[slot] = 0
                print(f"\n✅ Du trägst nun {new_item['name']}!")
                input("(ENTER)")


def zone_menu(player):
    from systems.zones import ZONE_DEFS, ZONE_ORDER, get_unlocked_zones
    while True:
        clear_screen()
        print_header("Zone wählen")
        print(f"Dein Level: {player.level}  |  Aktuelle Zone: ", end="")
        zdef_cur = ZONE_DEFS.get(getattr(player, "current_zone", "wald"), ZONE_DEFS["wald"])
        print(f"{zdef_cur['emoji']} {zdef_cur['name']}")
        print()
        unlocked = get_unlocked_zones(player.level)
        for i, zid in enumerate(ZONE_ORDER):
            zdef = ZONE_DEFS[zid]
            active = "★ " if zid == getattr(player, "current_zone", "wald") else "  "
            if zid in unlocked:
                print(f"  [{i+1}] {active}{zdef['emoji']}  {zdef['name']:<16} — {zdef['desc']}")
            else:
                print(f"  [{i+1}]   {zdef['emoji']}  {zdef['name']:<16} 🔒 Ab Level {zdef['unlock_level']}")
        print("\n  [Z] Zurück")
        choice = input("\nDeine Wahl: ").strip()
        if choice.lower() == "z":
            break
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ZONE_ORDER):
                zid = ZONE_ORDER[idx]
                if zid in unlocked:
                    player.current_zone = zid
                    zdef = ZONE_DEFS[zid]
                    clear_screen()
                    print_header(f"{zdef['emoji']}  {zdef['name']}")
                    from systems.zones import ZONE_FLAVOR
                    for line in ZONE_FLAVOR.get(zid, []):
                        print(line)
                    print(f"\n✅ Zone gewechselt zu: {zdef['emoji']} {zdef['name']}")
                    input("\n(ENTER)")
                    break
                else:
                    print(f"\n🔒 Diese Zone ist ab Level {ZONE_DEFS[zid]['unlock_level']} verfügbar.")
                    input("(ENTER)")


def sell_menu(player):
    from content.loot_tables import CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_DEFS, RARITY_LABEL

    while True:
        clear_screen()
        print_header("Inventar verkaufen")
        print(f"Gold: {player.inventory['Gold']} 🪙  |  Slots: {player.inventory_count()}/{MAX_INVENTORY_SLOTS}")
        print("-" * 56)

        sell_list = []

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
            print(f"  [{idx:>2}] {emoji} {key:<22} x{count}  →  {price} Gold/Stk  ({total} Gold)")
            sell_list.append(("consumable", key, price, count))

        # Junk
        junk = player.inventory.get("Junk", {})
        if junk:
            print("\n[ Schrott ]")
        for key, count in list(junk.items()):
            jdef  = JUNK_DEFS.get(key, {})
            emoji = jdef.get("emoji", "🗑️")
            price = jdef.get("sell", 1)
            total = price * count
            idx   = len(sell_list)
            print(f"  [{idx:>2}] {emoji} {key:<22} x{count}  →  {price} Gold/Stk  ({total} Gold)")
            sell_list.append(("junk", key, price, count))

        # Equipment
        equip_items = player.inventory["Equipment"]
        if equip_items:
            print("\n[ Ausrüstung ]")
        for i, item in enumerate(equip_items):
            if item["name"] in _STARTER_ITEMS:
                continue
            edef  = EQUIPMENT_DEFS.get(item["name"], {})
            price = edef.get("sell", 5)
            idx   = len(sell_list)
            print(f"  [{idx:>2}] {_equip_line(item)}  →  {price} Gold")
            sell_list.append(("equipment", item["name"], price, 1))

        if not sell_list:
            print("  Nichts zu verkaufen.")
            input("\n(ENTER)")
            return

        total_value = sum(p * c for _, _, p, c in sell_list)
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
                earned += EQUIPMENT_DEFS.get(item["name"], {}).get("sell", 5)
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
                real_idx = next((i for i, e in enumerate(equip_items) if e["name"] == key), None)
                if real_idx is None:
                    input("Item nicht mehr vorhanden. ENTER...")
                    continue
                equip_items.pop(real_idx)
                player.inventory["Gold"] += price
                print(f"\n✅ {key} verkauft für {price} Gold.")

            print(f"   Gold jetzt: {player.inventory['Gold']} 🪙")
            input("(ENTER)")
