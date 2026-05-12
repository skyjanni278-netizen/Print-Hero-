import random
from ui.utils import clear_screen, print_header


_SCHWARZMARKT_CATALOGUE = [
    {"name": "Drachenzahn",        "key": "Drachenzahn",        "type": "equipment", "price": 280},
    {"name": "Knochensense",       "key": "Knochensense",       "type": "equipment", "price": 240},
    {"name": "Drachenschuppen",    "key": "Drachenschuppen",    "type": "equipment", "price": 260},
    {"name": "Drachenkrone",       "key": "Drachenkrone",       "type": "equipment", "price": 220},
    {"name": "Drachenklauen",      "key": "Drachenklauen",      "type": "equipment", "price": 200},
    {"name": "Elixier",            "key": "Elixier",            "type": "consumable","price":  55},
    {"name": "Phönixfeder",        "key": "Phönixfeder",        "type": "consumable","price":  70},
    {"name": "Stärketrank",        "key": "Stärketrank",        "type": "consumable","price":  35},
]


def _schwarzmarkt(player):
    from content.loot_tables import EQUIPMENT_DEFS, CONSUMABLE_DEFS, RARITY_LABEL
    from core.player import MAX_INVENTORY_SLOTS
    clear_screen()
    print_header("🏴 Schwarzmarkt")
    print("Der Haendler schaut sich um und zieht eine schwarze Plane beiseite.")
    print("\"Nur fuer dich, und nur dieses Mal. Sag niemandem, was du hier gesehen hast.\"\n")
    picks = random.sample(_SCHWARZMARKT_CATALOGUE, min(4, len(_SCHWARZMARKT_CATALOGUE)))
    print(f"Gold: {player.inventory['Gold']} Muenzen\n")
    for i, item in enumerate(picks):
        affordable = "✅" if player.inventory["Gold"] >= item["price"] else "❌"
        if item["type"] == "equipment":
            edef   = EQUIPMENT_DEFS.get(item["key"], {})
            emoji  = edef.get("emoji", "⚔️")
            _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
            stat   = f"ATK +{edef['attack']}" if edef.get("slot") == "weapon" else f"DEF +{edef.get('armor',0)}"
            print(f"  [{i+1}] {rbadge}{emoji} {item['name']:<24} {stat:<10} {item['price']} Gold  {affordable}")
        else:
            cdef  = CONSUMABLE_DEFS.get(item["key"], {})
            emoji = cdef.get("emoji", "🧪")
            desc  = cdef.get("desc", "")
            print(f"  [{i+1}] {emoji} {item['name']:<24} {desc:<20} {item['price']} Gold  {affordable}")
    print("\n  [0] Weggehen")
    choice = input("\nWas kaufen? ").strip()
    if not choice.isdigit() or choice == "0":
        print("\"Komm wieder, wenn du Geld hast.\"")
        input("(ENTER)")
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(picks)):
        print("Ungueltige Auswahl.")
        input("(ENTER)")
        return
    item = picks[idx]
    if player.inventory["Gold"] < item["price"]:
        print("Zu wenig Gold!")
        input("(ENTER)")
        return
    if item["type"] == "consumable":
        added = player.add_consumable(item["key"], 1)
        if not added:
            print("Inventar voll oder Stapel bereits voll!")
            input("(ENTER)")
            return
    else:
        if not player.has_inventory_space():
            print("Inventar voll!")
            input("(ENTER)")
            return
        edef  = EQUIPMENT_DEFS.get(item["key"], {})
        slot  = edef.get("slot", "weapon")
        equip = {"name": item["key"], "type": slot}
        if slot == "weapon":
            equip["attack"] = edef["attack"]
        else:
            equip["armor"] = edef["armor"]
        player.inventory["Equipment"].append(equip)
    player.inventory["Gold"] -= item["price"]
    print(f"\n✅ {item['name']} erworben! Gold: {player.inventory['Gold']}")
    input("(ENTER)")


def _wandering_merchant(player):
    clear_screen()
    print_header("Wandernder Haendler")
    print("Ein Haendler tritt aus dem Gebusch — sein Sortiment wirkt verlockend.")
    print("Er bietet dir 3 zuefaellige Items zu einem Sonderpreis an!\n")

    # 3 zufaellige Consumables aus dem Shop-Sortiment mit 20% Rabatt
    from content.shop import SHOP_CATALOGUE
    available = [item for item in SHOP_CATALOGUE if item.get("type") == "consumable"
                 and item.get("min_level", 1) <= player.level]
    if not available:
        print("Er hat leider nichts fuer dich.")
        input("(ENTER)")
        return

    from content.loot_tables import CONSUMABLE_DEFS
    picks = random.sample(available, min(3, len(available)))
    print(f"Gold: {player.inventory['Gold']} Muenzen\n")
    for i, item in enumerate(picks):
        discounted = max(1, int(item["price"] * 0.8))
        emoji = CONSUMABLE_DEFS.get(item["key"], {}).get("emoji", "🧪")
        print(f"  [{i+1}] {emoji} {item['name']:<22} {discounted} Gold  (statt {item['price']})")
    print("\n  [0] Weiterziehen")

    while True:
        choice = input("\nWas kaufen? ").strip()
        if choice == "0" or not choice.isdigit():
            break
        idx = int(choice) - 1
        if not (0 <= idx < len(picks)):
            print("Ungueltige Auswahl.")
            continue
        item = picks[idx]
        discounted = max(1, int(item["price"] * 0.8))
        if player.inventory["Gold"] < discounted:
            print("Zu wenig Gold!")
            input("(ENTER)")
            break
        added = player.add_consumable(item["key"], 1)
        if added:
            player.inventory["Gold"] -= discounted
            print(f"Gekauft! Gold verbleibend: {player.inventory['Gold']}")
        else:
            print("Inventar voll oder Stapel bereits voll!")
        input("(ENTER)")
        break

    if getattr(player, "schwarzmarkt_available", True):
        print("\nDer Haendler schaut sich verschwoeererisch um...")
        print("\"Psst — ich haette da noch... ein Sonderangebot. Nichts fuer schwache Nerven.\"")
        c2 = input("[J] Schwarzmarkt besuchen  [N] Ablehnen: ").strip().lower()
        if c2 == "j":
            player.schwarzmarkt_available = False
            _schwarzmarkt(player)


def _abandoned_shrine(player):
    clear_screen()
    print_header("Verlassener Schrein")
    print("Du entdeckst einen alten Schrein am Wegesrand.")
    print("Eine schwache Energie liegt in der Luft...\n")
    print("  [B] Blutopfer — zahle 10 HP fuer +25% XP im naechsten Kampf")
    print("  [G] Gratis beten — ungewisser Ausgang")
    print("  [W] Weitergehen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "b":
        if player.hp <= 10:
            print("Du hast zu wenig HP fuer ein Opfer!")
        else:
            player.hp -= 10
            player.next_fight_xp_mult = 1.25
            print(f"Du opferst 10 HP. Der Schrein leuchtet auf! (HP: {player.hp}/{player.max_hp})")
            print("Naechster Kampf: +25% XP")
    elif choice == "g":
        roll = random.random()
        if roll < 0.5:
            from content.loot_tables import CONSUMABLE_DEFS
            key = random.choice(["Healing Potion", "Energie-Kristall"])
            added = player.add_consumable(key, 1)
            if added:
                print(f"Der Schrein beschenkt dich mit: {key}!")
            else:
                print("Der Schrein reagiert... aber dein Inventar ist voll.")
        else:
            print("Stille. Der Schrein gibt dir nichts.")
    input("\n(ENTER)")


def _poison_trap(player):
    clear_screen()
    print_header("Giftige Falle")
    avoid_roll = random.random()
    if avoid_roll < 0.40:
        print("Du bemerkst eine Falle im Boden und weichst geschickt aus!")
    else:
        dmg = random.randint(5, 12)
        player.hp = max(1, player.hp - dmg)
        print(f"Du trittst in eine vergiftete Falle! -{dmg} HP (HP: {player.hp}/{player.max_hp})")
    input("\n(ENTER)")


def _treasure_chest(player):
    from content.loot_tables import roll_loot, apply_loot
    clear_screen()
    print_header("Schatz-Truhe")
    print("Du entdeckst eine verstaubte Truhe im Dickicht!\n")
    loot_items = roll_loot(rank=2, rolls=2)
    msgs = apply_loot(player, loot_items)
    if msgs:
        for m in msgs:
            print(m)
    else:
        print("Die Truhe ist leider leer.")
    input("\n(ENTER)")


def _mysterious_stranger(player):
    clear_screen()
    print_header("Mysterioeoser Fremder")
    print("Ein vermummter Fremder tritt aus den Schatten.")
    print("Er sieht dich schweigend an und bietet dir etwas an...\n")
    heal_amt = max(1, player.max_hp // 5)
    print(f"  [H] Heilung annehmen   — +{heal_amt} HP")
    print(f"  [G] Gold erhalten      — +20 Gold")
    print(f"  [A] Ablehnen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "h":
        healed = min(heal_amt, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal_amt)
        print(f"Der Fremde legt seine Hand auf deine Schulter. +{healed} HP (HP: {player.hp}/{player.max_hp})")
    elif choice == "g":
        player.inventory["Gold"] += 20
        player.stats["gold_earned"] += 20
        print(f"Der Fremde drueckt dir einen Beutel Gold in die Hand. +20 Gold (Gold: {player.inventory['Gold']})")
    else:
        print("Du lehnst ab. Der Fremde nickt und verschwindet.")
    input("\n(ENTER)")


def _captured_soldier(player):
    clear_screen()
    print_header("Gefangener Soldat")
    print("Hinter einem Gitter liegt ein verwundeter Soldat.")
    print("Er fleht dich an, ihn zu befreien. Es kostet Zeit — und vielleicht Kraft.\n")
    print("  [B] Befreien   — nimmst 5 Schaden, erhältst dafür Gold und Loot")
    print("  [I] Ignorieren — du gehst weiter")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "b":
        cost = 5
        player.hp = max(1, player.hp - cost)
        print(f"\nDu kämpfst das Gitter auf. -{cost} HP  (HP: {player.hp}/{player.max_hp})")
        gold = random.randint(20, 45)
        player.inventory["Gold"] += gold
        player.stats["gold_earned"] += gold
        print(f"Der Soldat drückt dir seinen Reservebeutel in die Hand. +{gold} Gold!")
        if random.random() < 0.60:
            from content.loot_tables import roll_loot, apply_loot
            items = roll_loot(rank=2, rolls=1)
            msgs  = apply_loot(player, items)
            if msgs:
                print("Er zieht noch etwas aus seinem Mantel hervor:")
                for m in msgs:
                    print(m)
    else:
        print("\nDu gehst weiter. Der Soldat verstummt enttäuscht.")
    input("\n(ENTER)")


def _old_blacksmith(player):
    clear_screen()
    print_header("Alter Schmied")
    print("Ein alter Schmied hockt über seinem tragbaren Amboss.")
    print("Er schaut kurz auf dein Equipment und nickt bedächtig.\n")
    print("\"Ich kann das verbessern. Einmal, für umsonst. Such dir was aus.\"\n")

    from content.loot_tables import EQUIPMENT_DEFS
    _STARTER = {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}
    _MAX_UPGRADE_LVL = 3
    _SLOT_LABELS = {"weapon": "Waffe", "chest": "Rüstung", "head": "Helm", "feet": "Schuhe"}

    upgradeable = []
    for slot, label in _SLOT_LABELS.items():
        item = player.equipment[slot]
        if item["name"] in _STARTER:
            continue
        lvl = player.equipment_upgrades.get(slot, 0)
        if lvl >= _MAX_UPGRADE_LVL:
            continue
        upgradeable.append((slot, label, item, lvl))

    if not upgradeable:
        print("Er schaut sich dein Equipment an und schüttelt den Kopf.")
        print("\"Alles schon auf dem Höchstlevel. Gut gemacht.\"")
        input("\n(ENTER)")
        return

    for i, (slot, label, item, lvl) in enumerate(upgradeable):
        if slot == "weapon":
            next_bonus = f"+{(lvl + 1) * 2} ATK"
        else:
            next_bonus = f"+{lvl + 1} DEF"
        print(f"  [{i+1}] {label:<10} {item['name']:<24} Stufe {lvl} → {lvl+1}  ({next_bonus})")

    print("\n  [0] Ablehnen")
    choice = input("\nWas aufwerten? ").strip()

    if choice == "0" or not choice.isdigit():
        print("\nDu lehnst das Angebot ab. Der Schmied zuckt die Schultern.")
        input("(ENTER)")
        return

    idx = int(choice) - 1
    if not (0 <= idx < len(upgradeable)):
        print("\nUngültige Auswahl.")
        input("(ENTER)")
        return

    slot, label, item, lvl = upgradeable[idx]
    player.equipment_upgrades[slot] = lvl + 1
    new_lvl = player.equipment_upgrades[slot]
    if slot == "weapon":
        bonus_desc = f"+{new_lvl * 2} ATK gesamt"
    else:
        bonus_desc = f"+{new_lvl} DEF gesamt"
    print(f"\nDer Schmied arbeitet geschickt. Ein kurzes Hämmern — fertig.")
    print(f"⬆️  {item['name']} auf Stufe {new_lvl} aufgewertet! ({bonus_desc})")
    input("\n(ENTER)")


# Gewichtete Event-Tabelle: (Funktion, Gewicht)
_EVENTS = [
    (_wandering_merchant,  20),
    (_abandoned_shrine,    15),
    (_poison_trap,         10),
    (_treasure_chest,      20),
    (_mysterious_stranger, 15),
    (_captured_soldier,    12),
    (_old_blacksmith,       8),
]


def trigger_event(player):
    funcs, weights = zip(*_EVENTS)
    chosen = random.choices(funcs, weights=weights, k=1)[0]
    chosen(player)
