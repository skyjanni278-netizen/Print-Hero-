import random
from ui.utils import clear_screen, print_header, console
from rich.markup import escape as _esc
from config import MAX_INVENTORY_SLOTS

_RARITY_COLORS = {
    "common":    "white",
    "uncommon":  "green",
    "rare":      "blue",
    "epic":      "magenta",
    "legendary": "yellow",
}


def _resolve_weapon(item_key: str, player_class: str):
    """Return (resolved_key, edef) using class-specific variant if one exists."""
    from content.loot_tables import CLASS_WEAPON_MAP, EQUIPMENT_DEFS
    variant_key = CLASS_WEAPON_MAP.get(item_key, {}).get(player_class)
    if variant_key and variant_key in EQUIPMENT_DEFS:
        return variant_key, EQUIPMENT_DEFS[variant_key]
    return item_key, EQUIPMENT_DEFS.get(item_key, {})


def _build_item_to_set() -> dict:
    """Return {item_key: (set_name, set_emoji)} for every piece in every set."""
    from content.loot_tables import SET_DEFS
    result = {}
    for sname, sdef in SET_DEFS.items():
        for piece in sdef["pieces"]:
            result[piece] = (sname, sdef["emoji"])
    return result


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
    item_to_set = _build_item_to_set()

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
        ch = player.equipment['chest']
        h = player.equipment['head']
        f = player.equipment['feet']

        console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]  |  Inventar: {used_slots}/{MAX_INVENTORY_SLOTS} Slots  |  LVL {lvl}")
        console.print(f"  Ausgerüstet: [dim]{_esc(w['name'])} / {_esc(ch['name'])} / {_esc(h['name'])} / {_esc(f['name'])}[/dim]")
        console.print("─" * 62)

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

            console.print(f"\n  [bold]{_esc(sec_name)}[/bold]")

            for item in section_items:
                idx        = flat.index(item) + 1
                can_afford = player.inventory["Gold"] >= item["price"]
                afford_tag = "[green]✅[/green]" if can_afford else "[red]❌[/red]"

                if item["type"] == "consumable":
                    cur        = player.inventory.get("Consumables", {}).get(item["key"], 0)
                    max_stack  = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                    has_space  = player.can_add_consumable(item["key"])
                    warn       = "" if has_space else " [red]🎒VOLL[/red]"
                    stack_info = f"({cur}/{max_stack})"
                    price_col  = "yellow" if can_afford else "red"
                    console.print(f"  [[{idx:>2}]] {_esc(item['name']):<24} {stack_info:<8} [dim]{_esc(item['desc']):<20}[/dim] [{price_col}]{item['price']:>4} Gold[/{price_col}]  {afford_tag}{warn}")
                else:
                    if EQUIPMENT_DEFS.get(item["key"], {}).get("slot") == "weapon":
                        display_key, edef = _resolve_weapon(item["key"], player.player_class)
                    else:
                        display_key = item["key"]
                        edef = EQUIPMENT_DEFS.get(item["key"], {})
                    emoji     = edef.get("emoji", "⚔️")
                    rarity    = edef.get("rarity", "common")
                    _, rbadge = RARITY_LABEL.get(rarity, ("?", "⬜"))
                    rc        = _RARITY_COLORS.get(rarity, "white")
                    has_space = player.has_inventory_space()
                    warn      = "" if has_space else " [red]🎒VOLL[/red]"
                    stat      = f"ATK +{edef['attack']}" if edef.get("slot") == "weapon" else f"DEF +{edef['armor']}"
                    price_col = "yellow" if can_afford else "red"
                    set_info  = item_to_set.get(item["key"])
                    set_tag   = f"  [dim]{set_info[1]} {_esc(set_info[0])}[/dim]" if set_info else ""
                    console.print(f"  [[{idx:>2}]] {rbadge}[{rc}]{emoji} {_esc(display_key):<24}[/{rc}] {stat:<10} [dim]{_esc(edef.get('desc','')):<22}[/dim] [{price_col}]{item['price']:>4} Gold[/{price_col}]  {afford_tag}{warn}{set_tag}")

            # 🔒 Vorschau nächster Unlock
            if upcoming:
                unlock_name, unlock_lvl = upcoming
                if slot_filter == "weapon":
                    unlock_name, _ = _resolve_weapon(unlock_name, player.player_class)
                console.print(f"  [dim]🔒 {_esc(unlock_name):<24} (freigeschaltet ab LVL {unlock_lvl})[/dim]")

        if not flat:
            console.print("\n  [dim](Keine Items verfügbar)[/dim]")

        console.print(f"\n  [dim]🔄 Sortiment wechselt nach jedem Dungeon[/dim]")
        console.print("  [[0]] Verlassen")
        choice = input("\nWas möchtest du kaufen? ")

        if choice == "0":
            break
        if not choice.isdigit():
            continue

        display_idx = int(choice)
        if not (1 <= display_idx <= len(flat)):
            console.print("  [red]Ungültige Auswahl.[/red]")
            input("ENTER...")
            continue

        item = flat[display_idx - 1]

        if player.inventory["Gold"] < item["price"]:
            console.print("  [red]❌ Nicht genug Gold![/red]")
            input("ENTER...")
            continue

        if item["type"] == "consumable":
            added = player.add_consumable(item["key"], item["amount"])
            if added == 0:
                max_stack = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
                cur = player.inventory.get("Consumables", {}).get(item["key"], 0)
                if cur >= max_stack:
                    console.print(f"  [red]❌ Stapel voll! ({cur}/{max_stack})[/red]")
                else:
                    console.print(f"  [red]🎒 Inventar voll! ({player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots)[/red]")
                input("ENTER...")
                continue
            player.inventory["Gold"] -= item["price"]
            console.print(f"  [green]✅ Du kaufst {added}x {_esc(item['name'])}![/green]")

        elif item["type"] == "equipment":
            if not player.has_inventory_space():
                console.print(f"  [red]🎒 Inventar voll! ({player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots)[/red]")
                input("ENTER...")
                continue
            base_edef = EQUIPMENT_DEFS.get(item["key"], {})
            slot = base_edef.get("slot", "weapon")
            if slot == "weapon":
                resolved_key, edef = _resolve_weapon(item["key"], player.player_class)
            else:
                resolved_key, edef = item["key"], base_edef
            equip = {"name": resolved_key, "type": slot}
            if slot == "weapon":
                equip["attack"] = edef["attack"]
            else:
                equip["armor"] = edef["armor"]
            player.inventory["Gold"] -= item["price"]
            player.inventory["Equipment"].append(equip)
            console.print(f"  [green]✅ {_esc(resolved_key)} wurde deinem Inventar hinzugefügt![/green]")

        input("ENTER...")
