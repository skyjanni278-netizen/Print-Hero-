from ui.utils import clear_screen, print_header, console, hp_bar as _hp_bar
from rich.markup import escape as _esc
from core.save import save_run
from content.shop import shop_menu
from config import MAX_INVENTORY_SLOTS


def camp_menu(player, meta=None) -> str:
    """
    Lagerfeuer-Menü.
    Rückgabe: 'dungeon' | 'boss' | 'quit'
    """
    while True:
        from systems.world_map import get_zone_status, ZONE_BOSS_DEFS
        clear_screen()
        print_header("Lagerfeuer - Pause")
        used_slots = player.inventory_count()
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(consumables.values())
        from config import DIFFICULTY_SETTINGS
        from content.classes import CLASS_DEFS
        diff_label  = DIFFICULTY_SETTINGS.get(getattr(player, "difficulty", "normal"), {}).get("label", "Normal")
        pclass      = getattr(player, "player_class", "warrior")
        class_emoji = CLASS_DEFS.get(pclass, {}).get("emoji", "")
        class_name  = CLASS_DEFS.get(pclass, {}).get("name", "")
        hp_b = _hp_bar(player.hp, player.max_hp, width=14)
        console.print(f"  {_esc(class_emoji)} [bold]{_esc(player.name)}[/bold]  {_esc(class_name)}  |  LVL {player.level}  |  {_esc(diff_label)}")
        essenz_tag = f"   💠 {meta.get('runenessenz', 0)} Essenz" if meta is not None else ""
        console.print(f"  HP  {hp_b} {player.hp}/{player.max_hp}   💰 {player.inventory['Gold']} Gold{essenz_tag}")
        console.print(f"  [cyan]ATK {player.get_total_attack():<5}[/cyan]  [yellow]DEF {player.get_total_armor()}[/yellow]   XP {player.xp}/{player.xp_to_level_up}  (LVL {player.level})")
        for _slot_key, _slot_label in (("weapon","Waffe  "),("chest","Rüstung"),("head","Helm   "),("feet","Schuhe ")):
            _up = player.equipment_upgrades.get(_slot_key, 0)
            _up_tag = f" [cyan](↑{_up})[/cyan]" if _up > 0 else ""
            console.print(f"  [dim]{_slot_label}[/dim]  {_equip_line(player.equipment[_slot_key])}{_up_tag}")
        from content.loot_tables import get_active_sets
        active_sets = get_active_sets(player)
        if active_sets:
            parts = []
            for sname, sdef, count, bonus in active_sets:
                star = "[green]✅ VOLL[/green]" if count == 4 else f"{count}/4"
                parts.append(f"{_esc(sdef['emoji'])} {_esc(sname)} {star}: [dim]{_esc(bonus['desc'])}[/dim]")
            console.print("  Set:  " + "  |  ".join(parts))
        active_segs = getattr(player, "active_segnungen", [])
        if active_segs:
            from systems.segnungen import SEGNUNGEN_POOL, get_active_synergien
            seg_parts = [f"{SEGNUNGEN_POOL[sid]['emoji']} {_esc(SEGNUNGEN_POOL[sid]['name'])}"
                         for sid in active_segs if sid in SEGNUNGEN_POOL]
            syn_count = len(get_active_synergien(player))
            syn_tag   = f"  [cyan]🔗 {syn_count} Synergie(n)[/cyan]" if syn_count else ""
            console.print("  ✨ " + "  ".join(seg_parts) + syn_tag)
        from systems.zones import ZONE_DEFS
        zone_id    = getattr(player, "current_zone", "wald")
        zdef       = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
        zp         = getattr(player, "zone_progress", {}).get(zone_id, {})
        zone_done  = zp.get("dungeons_completed", 0)
        zone_req   = zdef["dungeon_count"]
        zone_status = get_zone_status(player, zone_id)
        boss_ready  = zone_status == "boss_ready"
        if zone_status == "completed":
            prog_tag = "✅ Boss besiegt"
        elif zone_status == "boss_ready":
            prog_tag = f"🔥 Boss bereit! ({zone_done}/{zone_req})"
        else:
            prog_tag = f"{zone_done}/{zone_req} Dungeons"
        zone_line  = f"{zdef['emoji']} {zdef['name']}  [{prog_tag}]"
        console.print(f"  🎒 {used_slots}/{MAX_INVENTORY_SLOTS} Slots  💊 {total_consumables} Items  🗺️ {_esc(zone_line)}")
        console.print("─" * 50)
        console.print(f"  [[I]] Inventar & Ausrüsten   [[F]] Fertigkeiten ({player.skill_points} Pkt)")
        console.print(f"  [[U]] Equipment aufwerten    [[E]] Errungenschaften ({len(player.achievements)}/20)")
        console.print(f"  [[V]] Inventar verkaufen     [[T]] Statistiken")
        console.print(f"  [[K]] Händler besuchen       [[Z]] Weltkarte / Zone wählen")
        console.print(f"  [[C]] Handwerk (Crafting)    [[G]] Segnungen ({len(getattr(player, 'active_segnungen', []))})")
        console.print("─" * 50)
        if boss_ready:
            bname = ZONE_BOSS_DEFS[zone_id]["name"]
            console.print(f"  [[B]] [bold red]🔥 Zone-Boss: {_esc(bname)}[/bold red]")
        console.print(f"  [[W]] [bold green]Dungeon betreten[/bold green]  |  [[S]] Speichern  |  [[Q]] Zur Zuflucht")

        choice = input("\nDeine Wahl: ").lower()
        if choice == 'i':
            inventory_menu(player)
        elif choice == 'u':
            upgrade_menu(player)
        elif choice == 'v':
            sell_menu(player)
        elif choice == 'k':
            shop_menu(player)
        elif choice == 'c':
            craft_menu(player)
        elif choice == 'z':
            from systems.world_map import show_world_map
            show_world_map(player)
        elif choice == 'f':
            from systems.skilltree import skill_menu
            skill_menu(player)
        elif choice == 'g':
            from ui.segnungen_ui import show_segnungen_overview
            show_segnungen_overview(player)
        elif choice == 'e':
            from systems.achievements import achievements_menu
            achievements_menu(player.achievements)
        elif choice == 't':
            stats_menu(player)
        elif choice == 's':
            save_run(player)
            input("(ENTER)")
        elif choice == 'q':
            return "quit"
        elif choice == 'b' and boss_ready:
            return "boss"
        elif choice == 'w':
            return "dungeon"


def stats_menu(player):
    from systems.zones import ZONE_DEFS
    clear_screen()
    print_header("Statistiken")
    s  = player.stats
    kd = f"{s['kills']}/{s['deaths']}" if s['deaths'] > 0 else str(s['kills'])
    dc = s.get("dungeons_completed", 0)
    df = s.get("dungeons_fled", 0)
    console.print(f"  ⚔️  Kämpfe gewonnen      : [cyan]{s['fights']}[/cyan]")
    console.print(f"  💀  Kills / Tode         : [cyan]{kd}[/cyan]")
    console.print(f"  🗡️  Schaden ausgeteilt   : [cyan]{s['damage_dealt']}[/cyan]")
    console.print(f"  🛡️  Schaden erhalten     : [cyan]{s['damage_taken']}[/cyan]")
    console.print(f"  💰  Gold verdient        : [yellow]{s['gold_earned']}[/yellow]")
    console.print(f"  🧪  Tränke benutzt       : [cyan]{s['potions_used']}[/cyan]")
    console.print(f"  🏰  Dungeons abgeschl.   : [cyan]{dc}[/cyan]  [dim](geflohen: {df})[/dim]")
    zone_kills = s.get("zone_kills", {})
    if zone_kills:
        console.print(f"\n  [bold]Zone-Kills:[/bold]")
        for zid, count in zone_kills.items():
            zdef  = ZONE_DEFS.get(zid, {})
            emoji = zdef.get("emoji", "🗺️")
            name  = zdef.get("name", zid)
            console.print(f"    {_esc(emoji)} {_esc(name):<16} : [cyan]{count}[/cyan]")
    input("\n(ENTER)")


_UPGRADE_COSTS   = [50, 120, 250]   # Kosten für Stufe 1, 2, 3
_STARTER_ITEMS   = {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}
_SLOT_LABELS     = {"weapon": "Waffe", "chest": "Rüstung", "head": "Helm", "feet": "Schuhe"}
_MAX_UPGRADE_LVL = 3


def upgrade_menu(player):
    while True:
        clear_screen()
        print_header("Equipment aufwerten")
        gratis = getattr(player, "schmied_gratis_upgrade", False)
        console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]\n")
        if gratis:
            console.print("  [bold cyan]🔨 Schmiedegeheimnis: Dein nächstes Upgrade ist GRATIS![/bold cyan]\n")
        console.print(f"  {'Slot':<10} {'Item':<24} {'Stufe':<8} {'Bonus':<12} {'Kosten'}")
        console.print("  " + "─" * 60)

        upgradeable = []
        for slot, label in _SLOT_LABELS.items():
            item     = player.equipment[slot]
            lvl      = player.equipment_upgrades.get(slot, 0)
            is_start = item["name"] in _STARTER_ITEMS

            if is_start:
                console.print(f"  [dim]{label:<10} {_esc(item['name']):<24} —        (Starter-Item, nicht aufwertbar)[/dim]")
                continue

            if slot == "weapon":
                bonus_str = f"+{lvl * 2} ATK"
            else:
                bonus_str = f"+{lvl} DEF"

            if lvl >= _MAX_UPGRADE_LVL:
                console.print(f"  [green]✅  {label:<10} {_esc(item['name']):<24} MAX      {bonus_str:<12} —[/green]")
            else:
                cost = 0 if gratis else _UPGRADE_COSTS[lvl]
                can_afford = player.inventory["Gold"] >= cost
                afford_tag = "[green]✅[/green]" if can_afford else "[red]❌[/red]"
                price_col  = "yellow" if can_afford else "red"
                cost_str   = "GRATIS 🔨" if gratis else f"{cost} Gold"
                console.print(f"  [[{len(upgradeable)}]] {label:<10} {_esc(item['name']):<24} Stufe {lvl}  {bonus_str:<12} [{price_col}]{cost_str}[/{price_col}] {afford_tag}")
                upgradeable.append((slot, lvl, cost))

        if not upgradeable:
            console.print("\n  [dim]Kein Item mehr aufwertbar.[/dim]")
            input("\n(ENTER)")
            break

        console.print("\n  [[Z]] Zurück")
        choice = input("\nWelches Item aufwerten? ").strip().lower()

        if choice == "z":
            break
        if choice.isdigit() and 0 <= int(choice) < len(upgradeable):
            slot, lvl, cost = upgradeable[int(choice)]
            if player.inventory["Gold"] < cost:
                console.print("  [red]Zu wenig Gold![/red]")
                input("(ENTER)")
                continue
            if gratis:
                player.schmied_gratis_upgrade = False
                console.print("  [cyan]🔨 Der Schmied übernimmt die Kosten.[/cyan]")
            player.inventory["Gold"]        -= cost
            player.equipment_upgrades[slot] += 1
            new_lvl = player.equipment_upgrades[slot]
            item    = player.equipment[slot]
            item["upgrade"] = new_lvl
            if slot == "weapon":
                bonus_desc = f"+{new_lvl * 2} ATK gesamt"
            else:
                bonus_desc = f"+{new_lvl} DEF gesamt"
            console.print(f"\n  [bold green]⬆️  {_esc(item['name'])} auf Stufe {new_lvl} aufgewertet![/bold green] ({bonus_desc})")
            console.print(f"  Gold verbleibend: [yellow]{player.inventory['Gold']} 🪙[/yellow]")
            input("(ENTER)")


def _equip_line(item):
    from content.loot_tables import EQUIPMENT_DEFS, RARITY_LABEL, SET_DEFS, WEAPON_VARIANT_TO_BASE
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
    # Resolve class variant → base for set lookup
    base_name = WEAPON_VARIANT_TO_BASE.get(item["name"], item["name"])
    set_tag = ""
    for sname, sdef in SET_DEFS.items():
        if base_name in sdef["pieces"]:
            set_tag = f" {sdef['emoji']}{sname}"
            break
    passive = edef.get("passive")
    passive_icons = {
        "poison_on_hit": " ☠️+Gift", "burn_on_hit": " 🔥+Verbr.",
        "freeze_on_hit": " ❄️+Einf.", "def_debuff_on_hit": " 🔨-DEF",
    }
    passive_tag = passive_icons.get(passive, "")
    return f"{rbadge}{emoji} {item['name']:<24} {stat:<10} [{rlabel}] ({slot_label}){set_tag}{passive_tag}"


def inventory_menu(player):
    from content.loot_tables import CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_DEFS, RARITY_LABEL, get_active_sets
    while True:
        clear_screen()
        print_header("Dein Inventar")
        used_slots = player.inventory_count()
        console.print(f"  🎒 Slots: [cyan]{used_slots}/{MAX_INVENTORY_SLOTS}[/cyan]")
        for _slot_key, _slot_label in (("weapon","Waffe  "),("chest","Rüstung"),("head","Helm   "),("feet","Schuhe ")):
            _up = player.equipment_upgrades.get(_slot_key, 0)
            _up_tag = f" [cyan](↑{_up})[/cyan]" if _up > 0 else ""
            console.print(f"  [dim]{_slot_label}[/dim]  {_equip_line(player.equipment[_slot_key])}{_up_tag}")
        active_sets = get_active_sets(player)
        if active_sets:
            for sname, sdef, count, bonus in active_sets:
                star = "[green]✅ VOLL[/green]" if count == 4 else f"{count}/4"
                console.print(f"  {_esc(sdef['emoji'])} {_esc(sname)} {star} → [dim]{_esc(bonus['desc'])}[/dim]")
        console.print()

        # --- Consumables ---
        consumables = player.inventory.get("Consumables", {})
        console.print("  [bold][ Verbrauchsgegenstände ][/bold]")
        if consumables:
            for key, count in consumables.items():
                cdef      = CONSUMABLE_DEFS.get(key, {})
                emoji     = cdef.get("emoji", "🧪")
                desc      = cdef.get("desc", "")
                max_stack = cdef.get("max_stack", 99)
                console.print(f"  {_esc(emoji)} {_esc(key):<22} {count}/{max_stack:<3}  — [dim]{_esc(desc)}[/dim]")
        else:
            console.print("  [dim](keine)[/dim]")
        console.print()

        # --- Junk ---
        junk = player.inventory.get("Junk", {})
        console.print("  [bold][ Schrott ][/bold]")
        if junk:
            for key, count in junk.items():
                jdef  = JUNK_DEFS.get(key, {})
                emoji = jdef.get("emoji", "🗑️")
                sell  = jdef.get("sell", 1)
                console.print(f"  {_esc(emoji)} {_esc(key):<22} x{count}  — [dim]{sell} Gold/Stk[/dim]")
        else:
            console.print("  [dim](keine)[/dim]")
        console.print()

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
        console.print("  [bold][ Angelegt ][/bold]")
        for slot_key, slot_label in SLOT_ORDER:
            equipped = player.equipment[slot_key]
            console.print(f"  ★ {_esc(slot_label):<12} {_equip_line(equipped)}")

        # Block 2: Inventar-Alternativen zum Anlegen
        console.print("\n  [bold][ Inventar — Nummer zum Anlegen ][/bold]")
        indexed_items = []

        for slot_key, slot_label in SLOT_ORDER:
            inv_for_slot = [it for it in equip_items if it["type"] == slot_key]
            if not inv_for_slot:
                continue
            console.print(f"\n  {_esc(slot_label)}")
            for item in inv_for_slot:
                n = len(indexed_items)
                indexed_items.append(item)
                up     = item.get("upgrade", 0)
                up_tag = f" [cyan](↑{up})[/cyan]" if up > 0 else ""
                console.print(f"  [[{n:>2}]] {_equip_line(item)}{up_tag}")

        if not indexed_items:
            console.print("  [dim](keine Ausrüstung im Inventar)[/dim]")

        console.print("\n  [Nummer] Anlegen  |  [[Z]] Zurück")
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
                    old_item["upgrade"] = player.equipment_upgrades.get(slot, 0)
                    equip_items.append(old_item)
                player.equipment[slot] = new_item
                new_lvl = new_item.get("upgrade", 0)
                player.equipment_upgrades[slot] = new_lvl
                suffix = f" [cyan](↑{new_lvl})[/cyan]" if new_lvl > 0 else ""
                console.print(f"\n  [green]✅ Du trägst nun {_esc(new_item['name'])}!{suffix}[/green]")
                input("(ENTER)")


def craft_menu(player):
    from content.loot_tables import CRAFT_RECIPES, CONSUMABLE_DEFS, JUNK_DEFS
    while True:
        clear_screen()
        print_header("🔨 Handwerk")
        junk = player.inventory.get("Junk", {})
        if junk:
            mat_parts = "  ".join(
                f"{_esc(JUNK_DEFS.get(k,{}).get('emoji','?'))} {_esc(k)} x{v}"
                for k, v in junk.items() if v > 0
            )
            console.print(f"  Materialien:  {mat_parts}")
        else:
            console.print("  Materialien:  [dim](keine Schrott-Items)[/dim]")
        console.print()

        craftable = []
        for key, recipe in CRAFT_RECIPES.items():
            can_craft = all(junk.get(mat, 0) >= qty for mat, qty in recipe["inputs"].items())
            cdef  = CONSUMABLE_DEFS.get(recipe["output"], {})
            emoji = cdef.get("emoji", "🧪")
            mark  = "[green]✅[/green]" if can_craft else "[red]❌[/red]"
            # Show missing materials in red
            mat_parts = []
            for mat, qty in recipe["inputs"].items():
                have = junk.get(mat, 0)
                if have >= qty:
                    mat_parts.append(f"[green]{_esc(mat)} x{qty}[/green]")
                else:
                    mat_parts.append(f"[red]{_esc(mat)} x{qty} (fehlt {qty-have})[/red]")
            mat_str = ", ".join(mat_parts)
            console.print(f"  [[{len(craftable)+1}]] {mark} {_esc(emoji)} {_esc(recipe['desc'])}")
            console.print(f"       Materialien: {mat_str}")
            craftable.append((key, recipe, can_craft))

        console.print("\n  [[Z]] Zurück")
        choice = input("\nWas herstellen? ").strip().lower()
        if choice == "z":
            break
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if not (0 <= idx < len(craftable)):
            continue
        rkey, recipe, can_craft = craftable[idx]
        if not can_craft:
            console.print("\n  [red]Nicht genug Materialien![/red]")
            input("(ENTER)")
            continue
        # Materialien verbrauchen
        for mat, qty in recipe["inputs"].items():
            player.inventory["Junk"][mat] -= qty
            if player.inventory["Junk"][mat] <= 0:
                del player.inventory["Junk"][mat]
        # Output hinzufügen
        added = player.add_consumable(recipe["output"], recipe["output_count"])
        cdef  = CONSUMABLE_DEFS.get(recipe["output"], {})
        emoji = cdef.get("emoji", "🧪")
        if added:
            console.print(f"\n  [green]{_esc(emoji)} {recipe['output_count']}× {_esc(recipe['output'])} hergestellt![/green]")
        else:
            # Rückgabe der Materialien bei vollem Inventar
            for mat, qty in recipe["inputs"].items():
                player.inventory["Junk"][mat] = player.inventory["Junk"].get(mat, 0) + qty
            console.print("\n  [red]Inventar voll! Crafting abgebrochen.[/red]")
        input("(ENTER)")




def sell_menu(player):
    from content.loot_tables import CONSUMABLE_DEFS, JUNK_DEFS, EQUIPMENT_DEFS, RARITY_LABEL

    while True:
        clear_screen()
        print_header("Inventar verkaufen")
        console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]  |  Slots: {player.inventory_count()}/{MAX_INVENTORY_SLOTS}")
        console.print("─" * 56)

        sell_list = []

        # Consumables
        consumables = player.inventory.get("Consumables", {})
        if consumables:
            console.print("  [bold][ Verbrauchsgegenstände ][/bold]")
        for key, count in list(consumables.items()):
            cdef  = CONSUMABLE_DEFS.get(key, {})
            emoji = cdef.get("emoji", "🧪")
            price = cdef.get("sell", 1)
            total = price * count
            idx   = len(sell_list)
            console.print(f"  [[{idx:>2}]] {_esc(emoji)} {_esc(key):<22} x{count}  →  [yellow]{price} Gold/Stk  ({total} Gold)[/yellow]")
            sell_list.append(("consumable", key, price, count))

        # Junk
        junk = player.inventory.get("Junk", {})
        if junk:
            console.print("\n  [bold][ Schrott ][/bold]")
        for key, count in list(junk.items()):
            jdef  = JUNK_DEFS.get(key, {})
            emoji = jdef.get("emoji", "🗑️")
            price = jdef.get("sell", 1)
            total = price * count
            idx   = len(sell_list)
            console.print(f"  [[{idx:>2}]] {_esc(emoji)} {_esc(key):<22} x{count}  →  [yellow]{price} Gold/Stk  ({total} Gold)[/yellow]")
            sell_list.append(("junk", key, price, count))

        # Equipment
        equip_items = player.inventory["Equipment"]
        if equip_items:
            console.print("\n  [bold][ Ausrüstung ][/bold]")
        for i, item in enumerate(equip_items):
            if item["name"] in _STARTER_ITEMS:
                continue
            edef  = EQUIPMENT_DEFS.get(item["name"], {})
            price = edef.get("sell", 5)
            idx   = len(sell_list)
            console.print(f"  [[{idx:>2}]] {_equip_line(item)}  →  [yellow]{price} Gold[/yellow]")
            sell_list.append(("equipment", item["name"], price, 1))

        if not sell_list:
            console.print("  [dim]Nichts zu verkaufen.[/dim]")
            input("\n(ENTER)")
            return

        total_value = sum(p * c for _, _, p, c in sell_list)
        console.print(f"\n  [[A]] [bold]Alles verkaufen ({total_value} Gold)[/bold]  |  [[Z]] Zurück")
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
            console.print(f"\n  [green]✅ Alles verkauft! +{earned} Gold.[/green]")
            console.print(f"  Gold jetzt: [yellow]{player.inventory['Gold']} 🪙[/yellow]")
            input("(ENTER)")
            break

        elif choice.isdigit():
            idx = int(choice)
            if not (0 <= idx < len(sell_list)):
                console.print("  [red]Ungültige Auswahl.[/red]")
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
                    console.print(f"\n  Wie viele {_esc(key)} verkaufen? (1–{cur}, ENTER = alle)")
                    amt_in = input("> ").strip()
                    if amt_in == "":
                        amount = cur
                    elif amt_in.isdigit() and 1 <= int(amt_in) <= cur:
                        amount = int(amt_in)
                    else:
                        console.print("  [red]Ungültige Menge.[/red]")
                        input("ENTER...")
                        continue
                else:
                    amount = 1
                earned = price * amount
                store[key] -= amount
                if store[key] <= 0:
                    del store[key]
                player.inventory["Gold"] += earned
                console.print(f"\n  [green]✅ {amount}x {_esc(key)} verkauft für {earned} Gold.[/green]")

            elif cat == "equipment":
                real_idx = next((i for i, e in enumerate(equip_items) if e["name"] == key), None)
                if real_idx is None:
                    input("Item nicht mehr vorhanden. ENTER...")
                    continue
                equip_items.pop(real_idx)
                player.inventory["Gold"] += price
                console.print(f"\n  [green]✅ {_esc(key)} verkauft für {price} Gold.[/green]")

            console.print(f"  Gold jetzt: [yellow]{player.inventory['Gold']} 🪙[/yellow]")
            input("(ENTER)")
