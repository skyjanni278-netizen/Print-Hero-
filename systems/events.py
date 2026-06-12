import random
from ui.utils import clear_screen, print_header, console, hp_bar, energy_bar
from rich.markup import escape as _esc
from systems.spiegel import spiegel_price as _spiegel_price


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
    from config import MAX_INVENTORY_SLOTS
    clear_screen()
    print_header("🏴 Schwarzmarkt")
    console.print("  Der Händler schaut sich um und zieht eine schwarze Plane beiseite.")
    console.print("  [dim]\"Nur für dich, und nur dieses Mal. Sag niemandem, was du hier gesehen hast.\"[/dim]\n")
    picks = [dict(it, price=_spiegel_price(player, it["price"]))
             for it in random.sample(_SCHWARZMARKT_CATALOGUE, min(4, len(_SCHWARZMARKT_CATALOGUE)))]
    console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]\n")
    for i, item in enumerate(picks):
        can_afford = player.inventory["Gold"] >= item["price"]
        afford_tag = "[green]✅[/green]" if can_afford else "[red]❌[/red]"
        price_col  = "yellow" if can_afford else "red"
        if item["type"] == "equipment":
            from content.loot_tables import CLASS_WEAPON_MAP
            edef   = EQUIPMENT_DEFS.get(item["key"], {})
            if edef.get("slot") == "weapon":
                variant = CLASS_WEAPON_MAP.get(item["key"], {}).get(player.player_class)
                if variant and variant in EQUIPMENT_DEFS:
                    display_key, edef = variant, EQUIPMENT_DEFS[variant]
                else:
                    display_key = item["key"]
            else:
                display_key = item["key"]
            emoji  = edef.get("emoji", "⚔️")
            _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
            stat   = f"ATK +{edef['attack']}" if edef.get("slot") == "weapon" else f"DEF +{edef.get('armor',0)}"
            console.print(f"  [[{i+1}]] {rbadge}{_esc(emoji)} {_esc(display_key):<24} {stat:<10} [{price_col}]{item['price']} Gold[/{price_col}]  {afford_tag}")
        else:
            cdef  = CONSUMABLE_DEFS.get(item["key"], {})
            emoji = cdef.get("emoji", "🧪")
            desc  = cdef.get("desc", "")
            console.print(f"  [[{i+1}]] {_esc(emoji)} {_esc(item['name']):<24} [dim]{_esc(desc):<20}[/dim] [{price_col}]{item['price']} Gold[/{price_col}]  {afford_tag}")
    console.print("\n  [[0]] Weggehen")
    choice = input("\nWas kaufen? ").strip()
    if not choice.isdigit() or choice == "0":
        console.print("  [dim]\"Komm wieder, wenn du Geld hast.\"[/dim]")
        input("(ENTER)")
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(picks)):
        console.print("  [red]Ungültige Auswahl.[/red]")
        input("(ENTER)")
        return
    item = picks[idx]
    if player.inventory["Gold"] < item["price"]:
        console.print("  [red]Zu wenig Gold![/red]")
        input("(ENTER)")
        return
    if item["type"] == "consumable":
        added = player.add_consumable(item["key"], 1)
        if not added:
            console.print("  [red]Inventar voll oder Stapel bereits voll![/red]")
            input("(ENTER)")
            return
        player.inventory["Gold"] -= item["price"]
        console.print(f"\n  [green]✅ {_esc(item['name'])} erworben![/green]  Gold: [yellow]{player.inventory['Gold']}[/yellow]")
    else:
        if not player.has_inventory_space():
            console.print("  [red]Inventar voll![/red]")
            input("(ENTER)")
            return
        from content.loot_tables import CLASS_WEAPON_MAP
        edef = EQUIPMENT_DEFS.get(item["key"], {})
        slot = edef.get("slot", "weapon")
        if slot == "weapon":
            variant = CLASS_WEAPON_MAP.get(item["key"], {}).get(player.player_class)
            if variant and variant in EQUIPMENT_DEFS:
                resolved_key, edef = variant, EQUIPMENT_DEFS[variant]
            else:
                resolved_key = item["key"]
        else:
            resolved_key = item["key"]
        equip = {"name": resolved_key, "type": slot}
        equip["attack" if slot == "weapon" else "armor"] = edef.get("attack" if slot == "weapon" else "armor", 0)
        player.inventory["Equipment"].append(equip)
        player.inventory["Gold"] -= item["price"]
        console.print(f"\n  [green]✅ {_esc(resolved_key)} erworben![/green]  Gold: [yellow]{player.inventory['Gold']}[/yellow]")
    input("(ENTER)")


def _wandering_merchant(player):
    clear_screen()
    print_header("Wandernder Händler")
    console.print("  Ein Händler tritt aus dem Gebüsch — sein Sortiment wirkt verlockend.")
    console.print("  Er bietet dir 3 zufällige Items zu einem Sonderpreis an!\n")

    from content.shop import SHOP_CATALOGUE
    available = [item for item in SHOP_CATALOGUE if item.get("type") == "consumable"
                 and item.get("min_level", 1) <= player.level]
    if not available:
        console.print("  [dim]Er hat leider nichts für dich.[/dim]")
        input("(ENTER)")
        return

    from content.loot_tables import CONSUMABLE_DEFS
    picks = random.sample(available, min(3, len(available)))

    while True:
        clear_screen()
        print_header("Wandernder Händler")
        console.print("  Ein Händler tritt aus dem Gebüsch — sein Sortiment wirkt verlockend.")
        console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]\n")
        for i, item in enumerate(picks):
            discounted = _spiegel_price(player, max(1, int(item["price"] * 0.8)))
            emoji      = CONSUMABLE_DEFS.get(item["key"], {}).get("emoji", "🧪")
            cur        = player.inventory.get("Consumables", {}).get(item["key"], 0)
            max_stack  = CONSUMABLE_DEFS.get(item["key"], {}).get("max_stack", 99)
            can_afford = player.inventory["Gold"] >= discounted
            price_col  = "yellow" if can_afford else "red"
            afford_tag = "[green]✅[/green]" if can_afford else "[red]❌[/red]"
            stack_info = f"({cur}/{max_stack})"
            console.print(f"  [[{i+1}]] {_esc(emoji)} {_esc(item['name']):<22} {stack_info:<8} [{price_col}]{discounted} Gold[/{price_col}]  [dim](statt {item['price']})[/dim]  {afford_tag}")
        console.print("\n  [[0]] Weiterziehen")

        choice = input("\nWas kaufen? ").strip()
        if choice == "0" or not choice.isdigit():
            break
        idx = int(choice) - 1
        if not (0 <= idx < len(picks)):
            console.print("  [red]Ungültige Auswahl.[/red]")
            input("(ENTER)")
            continue
        item = picks[idx]
        discounted = _spiegel_price(player, max(1, int(item["price"] * 0.8)))
        if player.inventory["Gold"] < discounted:
            console.print("  [red]Zu wenig Gold![/red]")
            input("(ENTER)")
            continue
        added = player.add_consumable(item["key"], 1)
        if added:
            player.inventory["Gold"] -= discounted
            console.print(f"  [green]✅ Gekauft![/green] Gold verbleibend: [yellow]{player.inventory['Gold']}[/yellow]")
        else:
            console.print("  [red]Inventar voll oder Stapel bereits voll![/red]")
        input("(ENTER)")

    if getattr(player, "schwarzmarkt_available", True):
        console.print("\n  [dim]Der Händler schaut sich verschwörerisch um...[/dim]")
        console.print("  [dim]\"Psst — ich hätte da noch... ein Sonderangebot. Nichts für schwache Nerven.\"[/dim]")
        c2 = input("  [J] Schwarzmarkt besuchen  [N] Ablehnen: ").strip().lower()
        if c2 == "j":
            player.schwarzmarkt_available = False
            _schwarzmarkt(player)


def _abandoned_shrine(player):
    clear_screen()
    print_header("Verlassener Schrein")
    console.print("  Du entdeckst einen alten Schrein am Wegesrand.")
    console.print("  [dim]Eine schwache Energie liegt in der Luft...[/dim]\n")
    console.print("  [[B]] [red]Blutopfer[/red]   — zahle 10 HP für +25% XP im nächsten Kampf")
    console.print("  [[G]] Gratis beten — ungewisser Ausgang")
    console.print("  [[W]] Weitergehen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "b":
        if player.hp <= 10:
            console.print("  [red]Du hast zu wenig HP für ein Opfer![/red]")
        else:
            player.hp -= 10
            hp_b = hp_bar(player.hp, player.max_hp)
            player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.25)
            console.print(f"  [red]Du opferst 10 HP. Der Schrein leuchtet auf![/red]")
            console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
            console.print("  [yellow]Nächster Kampf: +25% XP[/yellow]")
    elif choice == "g":
        roll = random.random()
        if roll < 0.5:
            key = random.choice(["Healing Potion", "Energie-Kristall"])
            added = player.add_consumable(key, 1)
            if added:
                console.print(f"  [green]Der Schrein beschenkt dich mit: {_esc(key)}![/green]")
            else:
                console.print("  [dim]Der Schrein reagiert... aber dein Inventar ist voll.[/dim]")
        else:
            console.print("  [dim]Stille. Der Schrein gibt dir nichts.[/dim]")
    input("\n(ENTER)")


def _poison_trap(player):
    clear_screen()
    print_header("Giftige Falle")
    avoid_roll = random.random()
    if avoid_roll < 0.40:
        console.print("  [green]Du bemerkst eine Falle im Boden und weichst geschickt aus![/green]")
    else:
        dmg = random.randint(5, 12)
        player.hp = max(1, player.hp - dmg)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print(f"  [red]Du trittst in eine vergiftete Falle! -{dmg} HP[/red]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    input("\n(ENTER)")


def _treasure_chest(player, meta=None):
    from content.loot_tables import roll_loot, apply_loot
    clear_screen()
    print_header("Schatz-Truhe")
    console.print("  Du entdeckst eine verstaubte Truhe im Dickicht!\n")
    loot_items = roll_loot(rank=2, rolls=2)
    msgs = apply_loot(player, loot_items)
    if msgs:
        for m in msgs:
            console.print(f"  {m}")
    else:
        console.print("  [dim]Die Truhe ist leider leer.[/dim]")
    if meta is not None:
        from systems.runen import check_rune_drop, rune_found_msgs
        rid = check_rune_drop(meta, "chest")
        if rid:
            console.print()
            for m in rune_found_msgs(rid, meta):
                console.print(f"  {m}")
    input("\n(ENTER)")


def _mysterious_stranger(player):
    clear_screen()
    print_header("Mysteriöser Fremder")
    console.print("  Ein vermummter Fremder tritt aus den Schatten.")
    console.print("  [dim]Er sieht dich schweigend an und bietet dir etwas an...[/dim]\n")
    heal_amt = max(1, player.max_hp // 5)
    console.print(f"  [[H]] [green]Heilung annehmen[/green]   — +{heal_amt} HP")
    console.print(f"  [[G]] [yellow]Gold erhalten[/yellow]      — +20 Gold")
    console.print(f"  [[A]] Ablehnen")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "h":
        healed = min(heal_amt, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal_amt)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print(f"  [green]Der Fremde legt seine Hand auf deine Schulter. +{healed} HP[/green]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    elif choice == "g":
        player.inventory["Gold"] += 20
        player.stats["gold_earned"] += 20
        console.print(f"  [yellow]Der Fremde drückt dir einen Beutel Gold in die Hand. +20 Gold[/yellow]")
        console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]")
    else:
        console.print("  [dim]Du lehnst ab. Der Fremde nickt und verschwindet.[/dim]")
    input("\n(ENTER)")


def _captured_soldier(player):
    clear_screen()
    print_header("Gefangener Soldat")
    console.print("  Hinter einem Gitter liegt ein verwundeter Soldat.")
    console.print("  [dim]Er fleht dich an, ihn zu befreien. Es kostet Zeit — und vielleicht Kraft.[/dim]\n")
    console.print("  [[B]] [green]Befreien[/green]   — nimmst 5 Schaden, erhältst dafür Gold und Loot")
    console.print("  [[I]] Ignorieren — du gehst weiter")

    choice = input("\nDeine Wahl: ").lower()
    if choice == "b":
        cost = 5
        player.hp = max(1, player.hp - cost)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print(f"\n  [red]Du kämpfst das Gitter auf. -{cost} HP[/red]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
        gold = random.randint(20, 45)
        player.inventory["Gold"] += gold
        player.stats["gold_earned"] += gold
        console.print(f"  [yellow]Der Soldat drückt dir seinen Reservebeutel in die Hand. +{gold} Gold![/yellow]")
        if random.random() < 0.60:
            from content.loot_tables import roll_loot, apply_loot
            items = roll_loot(rank=2, rolls=1)
            msgs  = apply_loot(player, items)
            if msgs:
                console.print("  Er zieht noch etwas aus seinem Mantel hervor:")
                for m in msgs:
                    console.print(f"  {m}")
    else:
        console.print("\n  [dim]Du gehst weiter. Der Soldat verstummt enttäuscht.[/dim]")
    input("\n(ENTER)")


def _old_blacksmith(player):
    clear_screen()
    print_header("Alter Schmied")
    console.print("  Ein alter Schmied hockt über seinem tragbaren Amboss.")
    console.print("  Er schaut kurz auf dein Equipment und nickt bedächtig.\n")
    console.print("  [dim]\"Ich kann das verbessern. Einmal, für umsonst. Such dir was aus.\"[/dim]\n")

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
        console.print("  [dim]Er schaut sich dein Equipment an und schüttelt den Kopf.[/dim]")
        console.print("  [dim]\"Alles schon auf dem Höchstlevel. Gut gemacht.\"[/dim]")
        input("\n(ENTER)")
        return

    for i, (slot, label, item, lvl) in enumerate(upgradeable):
        if slot == "weapon":
            next_bonus = f"+{(lvl + 1) * 2} ATK"
        else:
            next_bonus = f"+{lvl + 1} DEF"
        console.print(f"  [[{i+1}]] {_esc(label):<10} {_esc(item['name']):<24} Stufe {lvl} → {lvl+1}  [cyan]({next_bonus})[/cyan]")

    console.print("\n  [[0]] Ablehnen")
    choice = input("\nWas aufwerten? ").strip()

    if choice == "0" or not choice.isdigit():
        console.print("\n  [dim]Du lehnst das Angebot ab. Der Schmied zuckt die Schultern.[/dim]")
        input("(ENTER)")
        return

    idx = int(choice) - 1
    if not (0 <= idx < len(upgradeable)):
        console.print("\n  [red]Ungültige Auswahl.[/red]")
        input("(ENTER)")
        return

    slot, label, item, lvl = upgradeable[idx]
    player.equipment_upgrades[slot] = lvl + 1
    new_lvl = player.equipment_upgrades[slot]
    player.equipment[slot]["upgrade"] = new_lvl
    if slot == "weapon":
        bonus_desc = f"+{new_lvl * 2} ATK gesamt"
    else:
        bonus_desc = f"+{new_lvl} DEF gesamt"
    console.print(f"\n  [dim]Der Schmied arbeitet geschickt. Ein kurzes Hämmern — fertig.[/dim]")
    console.print(f"  [bold green]⬆️  {_esc(item['name'])} auf Stufe {new_lvl} aufgewertet![/bold green] ({bonus_desc})")
    input("\n(ENTER)")


def _bloody_altar(player):
    clear_screen()
    print_header("🩸 Blutiger Altar")
    console.print("  Ein dunkler Altar aus schwarzem Stein ragt aus dem Boden.")
    console.print("  [dim]Frisches Blut rinnt über die Runen — er verlangt ein Opfer.[/dim]\n")
    cost = max(5, int(player.max_hp * 0.15))
    if player.hp <= cost:
        console.print(f"  [red]Du bist zu geschwächt für ein Opfer. (Benötigt >{cost} HP)[/red]")
        input("\n(ENTER)")
        return
    hp_b = hp_bar(player.hp, player.max_hp)
    console.print(f"  Kosten: [red]{cost} HP[/red]   Deine HP: {hp_b} {player.hp}/{player.max_hp}\n")
    console.print("  [[A]] [cyan]+30% ATK im nächsten Kampf[/cyan]")
    console.print("  [[E]] [blue]Energie vollständig auffüllen[/blue]")
    console.print("  [[X]] [yellow]+50% XP im nächsten Kampf[/yellow]")
    console.print("  [[N]] Ablehnen")
    choice = input("\nDeine Wahl: ").lower()
    if choice == "n" or choice not in ("a", "e", "x"):
        console.print("\n  [dim]Du wendest dich vom Altar ab.[/dim]")
        input("(ENTER)")
        return
    player.hp -= cost
    hp_b2 = hp_bar(player.hp, player.max_hp)
    console.print(f"\n  [red]Du hast {cost} HP geopfert. Der Altar leuchtet blutrot auf.[/red]")
    console.print(f"  HP {hp_b2} {player.hp}/{player.max_hp}")
    if choice == "a":
        player.next_fight_atk_mult = getattr(player, "next_fight_atk_mult", 1.0) * 1.30
        console.print("  [cyan]Ein dunkler Schauer stärkt deinen Arm. +30% ATK im nächsten Kampf![/cyan]")
    elif choice == "e":
        eff_max = player.get_effective_max_energy()
        player.energy = eff_max
        en_b = energy_bar(player.energy, eff_max)
        console.print(f"  [blue]Schwarze Energie strömt in dich. Energie vollständig aufgefüllt![/blue]")
        console.print(f"  ⚡ {en_b} {player.energy}/{eff_max}")
    elif choice == "x":
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.5)
        console.print("  [yellow]Der Altar zeigt dir Visionen vergangener Kämpfe. +50% XP im nächsten Kampf![/yellow]")
    input("\n(ENTER)")


def _whispering_ghost(player):
    clear_screen()
    print_header("👻 Flüsternder Geist")
    console.print("  Eine schimmernde Gestalt materialisiert sich vor dir.")
    console.print("  [dim]Der Geist des Dungeons flüstert... er kennt die Tiefen dieser Hallen.[/dim]\n")
    roll = random.random()
    if roll < 0.50:
        bonus = 0.20
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.0 + bonus)
        heal = max(3, int(player.max_hp * 0.10))
        healed = min(heal, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print("  [green]Der Geist legt seine eiskalten Hände auf deine Schultern.[/green]")
        console.print(f"  [green]Eine seltsame Ruhe überkommt dich. +{healed} HP, +{int(bonus*100)}% XP im nächsten Kampf.[/green]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    elif roll < 0.80:
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.30)
        console.print("  [yellow]Der Geist flüstert dir Taktiken und Schwachstellen ins Ohr.")
        console.print("  +30% XP im nächsten Kampf![/yellow]")
    else:
        dmg = random.randint(5, 12)
        player.hp = max(1, player.hp - dmg)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print("  [red]Der Geist ist feindselig! Er reißt Lebensenergie aus dir heraus.[/red]")
        console.print(f"  [red]-{dmg} HP[/red]   HP {hp_b} {player.hp}/{player.max_hp}")
    input("\n(ENTER)")


def _magic_chest(player):
    from content.loot_tables import roll_loot, apply_loot
    clear_screen()
    print_header("🔮 Magische Schatztruhe")
    console.print("  Eine leuchtende Truhe schwebt leicht über dem Boden.")
    console.print("  [dim]Runenschrift zieht sich über das Holz — gut oder böse, schwer zu sagen.[/dim]\n")
    if random.random() < 0.30:
        dmg = random.randint(10, 20)
        player.hp = max(1, player.hp - dmg)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print("  [red]Die Truhe explodiert beim Öffnen! Dunkle Magie schlägt dich zurück.[/red]")
        console.print(f"  [red]-{dmg} HP[/red]   HP {hp_b} {player.hp}/{player.max_hp}\n")
        items = roll_loot(rank=2, rolls=1)
        msgs  = apply_loot(player, items)
        if msgs:
            console.print("  Aus den Trümmern rettest du noch etwas:")
            for m in msgs:
                console.print(f"  {m}")
        else:
            console.print("  [dim]Und die Truhe war obendrein leer. Einfach kein Glück.[/dim]")
    else:
        items = roll_loot(rank=3, rolls=2)
        msgs  = apply_loot(player, items)
        console.print("  [green]Die Truhe öffnet sich mit einem sanften Leuchten. Heute hast du Glück![/green]")
        if msgs:
            for m in msgs:
                console.print(f"  {m}")
        else:
            gold = random.randint(25, 50)
            player.inventory["Gold"] += gold
            player.stats["gold_earned"] += gold
            console.print(f"  [yellow]+{gold} Gold aus dem Inneren der Truhe.[/yellow]")
    input("\n(ENTER)")


def _dungeon_arms_dealer(player):
    from content.loot_tables import EQUIPMENT_DEFS, CONSUMABLE_DEFS, RARITY_LABEL
    from content.shop import _RARITY_COLORS
    from config import MAX_INVENTORY_SLOTS
    clear_screen()
    print_header("🏪 Händler im Dungeon")
    console.print("  Ein schwer bewaffneter Händler nickt dir zu.")
    console.print("  [dim]\"Keine Zeit für Smalltalk. Kaufst du oder nicht?\"[/dim]\n")

    equip_pool = [k for k, v in EQUIPMENT_DEFS.items()
                  if v.get("rarity") in ("common", "uncommon", "rare")
                  and v.get("sell", 0) > 0]
    cons_pool  = list(CONSUMABLE_DEFS.keys())

    picks = []
    for key in random.sample(equip_pool, min(2, len(equip_pool))):
        edef  = EQUIPMENT_DEFS[key]
        price = _spiegel_price(player, max(15, int(edef.get("sell", 10) * 2 * 1.3)))
        picks.append({"key": key, "type": "equipment", "price": price, "edef": edef})
    for key in random.sample(cons_pool, min(2, len(cons_pool))):
        cdef  = CONSUMABLE_DEFS[key]
        price = _spiegel_price(player, max(10, int(cdef.get("sell", 8) * 2 * 1.3)))
        picks.append({"key": key, "type": "consumable", "price": price, "cdef": cdef})

    console.print(f"  Gold: [yellow]{player.inventory['Gold']} 🪙[/yellow]\n")
    for i, item in enumerate(picks):
        can_afford = player.inventory["Gold"] >= item["price"]
        afford_tag = "[green]✅[/green]" if can_afford else "[red]❌[/red]"
        price_col  = "yellow" if can_afford else "red"
        if item["type"] == "equipment":
            from content.loot_tables import CLASS_WEAPON_MAP
            edef  = item["edef"]
            slot  = edef.get("slot", "weapon")
            display_key = item["key"]
            if slot == "weapon":
                variant = CLASS_WEAPON_MAP.get(item["key"], {}).get(player.player_class)
                if variant and variant in EQUIPMENT_DEFS:
                    display_key = variant
                    edef = EQUIPMENT_DEFS[variant]
            emoji = edef.get("emoji", "⚔️")
            _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
            rc    = _RARITY_COLORS.get(edef.get("rarity", "common"), "white")
            stat  = f"ATK +{edef['attack']}" if slot == "weapon" else f"DEF +{edef.get('armor',0)}"
            console.print(f"  [[{i+1}]] {rbadge}[{rc}]{_esc(emoji)} {_esc(display_key):<22}[/{rc}] {stat:<10} [{price_col}]{item['price']} Gold[/{price_col}]  {afford_tag}")
        else:
            cdef  = item["cdef"]
            emoji = cdef.get("emoji", "🧪")
            desc  = cdef.get("desc", "")
            console.print(f"  [[{i+1}]] {_esc(emoji)} {_esc(item['key']):<22} [dim]{_esc(desc):<18}[/dim] [{price_col}]{item['price']} Gold[/{price_col}]  {afford_tag}")
    console.print("\n  [[0]] Weggehen")

    while True:
        choice = input("\nWas kaufen? (0 = weggehen) ").strip()
        if choice == "0" or not choice.isdigit():
            break
        idx = int(choice) - 1
        if not (0 <= idx < len(picks)):
            console.print("  [red]Ungültige Auswahl.[/red]")
            continue
        item = picks[idx]
        if player.inventory["Gold"] < item["price"]:
            console.print("  [red]Zu wenig Gold![/red]")
            continue
        if item["type"] == "consumable":
            if not player.add_consumable(item["key"], 1):
                console.print("  [red]Inventar voll![/red]")
                continue
        else:
            if not player.has_inventory_space():
                console.print("  [red]Inventar voll![/red]")
                continue
            from content.loot_tables import CLASS_WEAPON_MAP
            edef = item["edef"]
            slot = edef.get("slot", "weapon")
            resolved_key = item["key"]
            if slot == "weapon":
                variant = CLASS_WEAPON_MAP.get(item["key"], {}).get(player.player_class)
                if variant and variant in EQUIPMENT_DEFS:
                    resolved_key = variant
                    edef = EQUIPMENT_DEFS[variant]
            entry = {"name": resolved_key, "type": slot}
            if slot == "weapon":
                entry["attack"] = edef["attack"]
            else:
                entry["armor"] = edef["armor"]
            player.inventory["Equipment"].append(entry)
        player.inventory["Gold"] -= item["price"]
        console.print(f"  [green]Gekauft![/green] Gold: [yellow]{player.inventory['Gold']}[/yellow]")
    input("\n(ENTER)")


def _verfallene_bibliothek(player):
    clear_screen()
    print_header("📚 Verfallene Bibliothek")
    console.print("  Halb eingestürzte Regale, vergilbtes Pergament, Staub in der Luft.")
    console.print("  [dim]Ein einziges Buch kannst du in Ruhe studieren — wähle weise.[/dim]\n")
    console.print("  [[W]] [cyan]Waffenkunde[/cyan]     — +2 ATK für diesen Run")
    console.print("  [[R]] [yellow]Runen-Lore[/yellow]      — +15% XP für diesen Run")
    console.print("  [[M]] [magenta]Magiebuch[/magenta]       — sofort eine zufällige Segnung")
    console.print("  [[?]] Unlesbares Buch — unbekannter Effekt (gut oder schlecht)")
    console.print("  [[Z]] Weitergehen")
    choice = input("\nDeine Wahl: ").strip().lower()
    if choice == "w":
        player.attack += 2
        console.print("\n  [cyan]⚔️  Du studierst alte Kampftechniken. +2 ATK für diesen Run![/cyan]")
    elif choice == "r":
        player.run_xp_mult = getattr(player, "run_xp_mult", 1.0) * 1.15
        console.print("\n  [yellow]📜 Uraltes Runenwissen erfüllt dich. +15% XP für diesen Run![/yellow]")
    elif choice == "m":
        from systems.segnungen import roll_segnung_choices, apply_segnung
        choices = roll_segnung_choices(player, 1)
        if choices:
            console.print("\n  [magenta]✨ Das Magiebuch leuchtet auf — eine Segnung strömt in dich![/magenta]")
            for m in apply_segnung(player, choices[0]):
                console.print(f"  {m}")
        else:
            console.print("\n  [dim]Das Buch bleibt dunkel — du trägst bereits alle Segnungen.[/dim]")
    elif choice == "?":
        roll = random.random()
        if roll < 0.35:
            healed = min(player.max_hp - player.hp, max(5, player.max_hp // 4))
            player.hp = min(player.max_hp, player.hp + healed)
            console.print(f"\n  [green]Die Worte ordnen sich zu einem Heilgesang. +{healed} HP![/green]")
        elif roll < 0.60:
            gold = random.randint(20, 45)
            player.inventory["Gold"] += gold
            player.stats["gold_earned"] += gold
            console.print(f"\n  [yellow]Zwischen den Seiten: eine vergessene Börse. +{gold} Gold![/yellow]")
        else:
            dmg = random.randint(5, 12)
            player.hp = max(1, player.hp - dmg)
            hp_b = hp_bar(player.hp, player.max_hp)
            console.print(f"\n  [red]Die Schriftzeichen brennen sich in deinen Geist! -{dmg} HP[/red]")
            console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    else:
        console.print("\n  [dim]Du lässt die alten Bücher ruhen.[/dim]")
    input("\n(ENTER)")


def _gefallener_held(player, meta=None):
    from content.loot_tables import LOOT_POOL, EQUIPMENT_DEFS, apply_loot
    clear_screen()
    print_header("🪦 Gefallener Held")
    console.print("  Am Wegesrand liegt ein toter Abenteurer — die Rüstung noch intakt.")
    console.print("  [dim]Er war kurz vor dem Ziel. Fast wie du.[/dim]\n")
    console.print("  [[N]] [magenta]Ausrüstung nehmen[/magenta] — zufälliges episches Item, aber −10 max HP (dieser Run)")
    console.print("  [[B]] [green]Bestatten[/green]         — +20% XP im nächsten Kampf, Chance auf eine Rune")
    console.print("  [[R]] Ruhe lassen")
    choice = input("\nDeine Wahl: ").strip().lower()
    if choice == "n":
        pool = [e for e in LOOT_POOL["epic"]
                if e["type"] == "equipment"
                and EQUIPMENT_DEFS.get(e["key"], {}).get("class_only") in (None, player.player_class)]
        item = random.choice(pool)
        player.max_hp = max(1, player.max_hp - 10)
        player.hp     = min(player.hp, player.max_hp)
        console.print(f"\n  [red]Ein kalter Schauer — der Fluch des Toten haftet an dir. −10 max HP (HP: {player.hp}/{player.max_hp})[/red]")
        for m in apply_loot(player, [item]):
            console.print(f"  {m}")
    elif choice == "b":
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.20)
        console.print("\n  [green]Du errichtest ein schlichtes Grab. Der Held dankt es dir.[/green]")
        console.print("  [yellow]+20% XP im nächsten Kampf![/yellow]")
        if meta is not None:
            from systems.runen import check_rune_drop, rune_found_msgs
            rid = check_rune_drop(meta, "grave")
            if rid:
                console.print()
                for m in rune_found_msgs(rid, meta):
                    console.print(f"  {m}")
    else:
        console.print("\n  [dim]Du gehst leise weiter. Manche Geschichten enden eben so.[/dim]")
    input("\n(ENTER)")


def _haendler_auktion(player):
    from content.loot_tables import EQUIPMENT_DEFS, CLASS_WEAPON_MAP, RARITY_LABEL
    clear_screen()
    print_header("🔨 Händler-Auktion")
    candidates = [k for k, v in EQUIPMENT_DEFS.items()
                  if v.get("rarity") in ("rare", "epic") and v.get("sell", 0) > 0
                  and v.get("class_only") in (None, player.player_class)
                  and k not in CLASS_WEAPON_MAP]
    item_key = random.choice(candidates)
    edef     = EQUIPMENT_DEFS[item_key]
    if edef.get("slot") == "weapon":
        variant = CLASS_WEAPON_MAP.get(item_key, {}).get(player.player_class)
        if variant and variant in EQUIPMENT_DEFS:
            item_key, edef = variant, EQUIPMENT_DEFS[variant]
    _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
    stat = f"ATK +{edef['attack']}" if edef.get("slot") == "weapon" else f"DEF +{edef.get('armor', 0)}"
    bid          = max(10, int(edef.get("sell", 20) * 0.8))
    rival_budget = int(bid * random.uniform(1.6, 2.6))
    rival_name   = random.choice(["Grimbart", "Lysandra", "Der Vermummte"])

    console.print("  Drei Gestalten feilschen um ein einzelnes Fundstück — du trittst dazu.")
    console.print(f"\n  Zur Auktion: {rbadge}{_esc(edef.get('emoji','⚔️'))} [bold]{_esc(item_key)}[/bold]  ({stat})")
    console.print(f"  Startgebot: [yellow]{bid} Gold[/yellow]   Dein Gold: [yellow]{player.inventory['Gold']}[/yellow]")

    won = False
    while True:
        next_bid = int(bid * 1.25) + 1
        can_pay  = player.inventory["Gold"] >= next_bid
        tag      = "" if can_pay else "  [red](zu teuer)[/red]"
        console.print(f"\n  {_esc(rival_name)} bietet [yellow]{bid} Gold[/yellow].")
        console.print(f"  [[J]] Überbieten ({next_bid} Gold){tag}    [[N]] Aussteigen")
        c = input("  Deine Wahl: ").strip().lower()
        if c != "j" or not can_pay:
            break
        bid = next_bid
        if bid > rival_budget:
            won = True
            break
        bid = int(bid * 1.2) + 1
        if bid > rival_budget:
            bid = rival_budget

    if won:
        if not player.has_inventory_space():
            console.print("\n  [red]🎒 Inventar voll — du musst das Item zurücklassen! Das Gold behältst du.[/red]")
        else:
            player.inventory["Gold"] -= bid
            equip = {"name": item_key, "type": edef.get("slot", "weapon")}
            equip["attack" if edef.get("slot") == "weapon" else "armor"] = edef.get("attack", edef.get("armor", 0))
            player.inventory["Equipment"].append(equip)
            console.print(f"\n  [green]✅ Zuschlag! {_esc(item_key)} für {bid} Gold ersteigert.[/green]")
            console.print(f"  Gold: [yellow]{player.inventory['Gold']}[/yellow]")
    else:
        player.auction_grudge = item_key
        console.print(f"\n  [red]{_esc(rival_name)} erhält den Zuschlag — und fixiert dich mit einem hasserfüllten Blick.[/red]")
        console.print("  [dim]\"Das Stück gehört MIR. Wage es nicht, mir zu folgen...\"[/dim]")
        console.print("  [yellow]⚠️  Der Rivale wird dir im nächsten Kampf auflauern![/yellow]")
    input("\n(ENTER)")


def _zeitkapsel(player):
    from core.save import load_last_run_data
    from content.loot_tables import EQUIPMENT_DEFS, RARITY_LABEL
    clear_screen()
    print_header("⏳ Zeitkapsel")
    console.print("  Eine versiegelte Kapsel, halb im Boden vergraben.")
    console.print("  [dim]Sie wirkt seltsam vertraut — als hättest du sie selbst hinterlassen...[/dim]\n")

    _STARTER = {"Fäuste", "Lumpen", "Kein Helm", "Keine Schuhe"}
    data = load_last_run_data()
    candidates = []
    if data:
        names  = [it.get("name") for it in data.get("inventory", {}).get("Equipment", [])]
        names += [it.get("name") for it in data.get("equipment", {}).values()]
        candidates = [n for n in names
                      if n and n not in _STARTER and n in EQUIPMENT_DEFS
                      and EQUIPMENT_DEFS[n].get("class_only") in (None, player.player_class)]

    if not candidates or not player.has_inventory_space():
        gold = random.randint(20, 40)
        player.inventory["Gold"] += gold
        player.stats["gold_earned"] += gold
        console.print(f"  [yellow]In der Kapsel: ein Beutel Gold. +{gold} Gold![/yellow]")
    else:
        name  = random.choice(candidates)
        edef  = EQUIPMENT_DEFS[name]
        slot  = edef.get("slot", "weapon")
        equip = {"name": name, "type": slot}
        equip["attack" if slot == "weapon" else "armor"] = edef.get("attack", edef.get("armor", 0))
        player.inventory["Equipment"].append(equip)
        _, rbadge = RARITY_LABEL.get(edef.get("rarity", "common"), ("?", "⬜"))
        console.print("  [cyan]Ein Echo deines letzten Lebens — die Kapsel enthält:[/cyan]")
        console.print(f"  {rbadge}{_esc(edef.get('emoji','⚔️'))} [bold]{_esc(name)}[/bold]")
    input("\n(ENTER)")


# Gewichtete Event-Tabelle: (Funktion, Gewicht)
_EVENTS = [
    (_wandering_merchant,  18),
    (_abandoned_shrine,    12),
    (_poison_trap,          8),
    (_treasure_chest,      15),
    (_mysterious_stranger, 12),
    (_captured_soldier,    10),
    (_old_blacksmith,       7),
    # v2.0.2 — neue Events
    (_bloody_altar,        10),
    (_whispering_ghost,    12),
    (_magic_chest,         10),
    (_dungeon_arms_dealer,  6),
    # v3.2 — neue Events
    (_verfallene_bibliothek, 9),
    (_gefallener_held,       8),
    (_haendler_auktion,      7),
    (_zeitkapsel,            6),
]

_META_EVENTS = {_treasure_chest, _gefallener_held}


def trigger_event(player, meta=None):
    events = _EVENTS
    if getattr(player, "spiegel", {}).get("haendlerglueck") == "A":
        events = [(f, w * 2 if f is _wandering_merchant else w) for f, w in _EVENTS]
    funcs, weights = zip(*events)
    chosen = random.choices(funcs, weights=weights, k=1)[0]
    if chosen in _META_EVENTS:
        chosen(player, meta)
    else:
        chosen(player)
