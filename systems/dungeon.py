import random
from ui.utils import clear_screen, print_header, console, hp_bar, energy_bar
from rich.markup import escape as _esc
from rich.panel import Panel

DUNGEON_NAMES = {
    "wald": [
        "Die Finstere Waldschlucht",
        "Höhle des Schattenwolfes",
        "Das Versunkene Dickicht",
        "Hain der alten Bestien",
        "Der Knochenpfad",
    ],
    "ruinen": [
        "Die Blutigen Ruinen",
        "Gewölbe des Vergessens",
        "Katakomben des ewigen Fluches",
        "Das Grabmal der Verdammten",
        "Untote Festung Arkenmoor",
    ],
    "wueste": [
        "Das Sandgrab des Sultans",
        "Ruinen von Dhar'Khan",
        "Die Räuberhöhle von Al-Marak",
        "Tempel des Sonnengottes",
        "Schlucht der Meuchler",
    ],
    "vulkan": [
        "Schmiede der Verdammnis",
        "Höhle des Ewigen Frostes",
        "Lavafestung Ignaris",
        "Der Brennende Abgrund",
        "Tempel des Feuerdämons",
    ],
    "dunkelreich": [
        "Zitadelle der Finsternis",
        "Das Ewige Labyrinth",
        "Thron des Dunkelritters",
        "Gewölbe des Vergänglichen",
        "Herz der Dunkelheit",
    ],
}

BOSS_INTROS = {
    "Zombie":        "Ein gewaltiger Untoter erhebt sich aus dem Boden. Sein Blick ist leer — sein Hunger grenzenlos.",
    "Skelett":       "Das Skelett rasselt mit seinen Knochen. Einst ein mächtiger Krieger, jetzt ein nie endender Albtraum.",
    "Schleim":       "Eine riesige Schleimmasse pulsiert bedrohlich. Alles, was sie berührt, löst sich in nichts auf.",
    "Goblin":        "Der Anführer der Goblin-Horde grinst bösartig. Sein Gold-durchtränkter Blick verrät grenzenlose Gier.",
    "Drache":        "Der Drache entfaltet seine mächtigen Schwingen. Ein jahrtausendealter Schatz liegt hinter ihm.",
    "Bandit":        "Der Banditenkönig tritt vor. Narben zieren sein Gesicht — jede davon eine Geschichte überlebter Kämpfe.",
    "Waldtroll":     "Der Waldtroll schlägt sich mit seinen Fäusten auf die Brust. Der Boden bebt unter jedem Schritt.",
    "Schattenwolf":  "Der Alphawolf jault. Aus dem Dunkel treten seine Augen hervor — brennend wie Glutkohlen.",
    "Giftige Spinne": "Die Riesenspinne lauert in ihrem Netz. Ihr Gift ist stark genug, einen Ochsen in Minuten zu töten.",
    "Meuchler":      "Der Meistermeuchler verschmilzt mit den Schatten. Du weißt, dass er da ist — aber wo genau, bleibt verborgen.",
    "Eismagierin":   "Die Eismagierin hebt ihre Hände. Die Temperatur fällt sofort — dein Atem bildet Dampfwolken.",
    "Steingolem":    "Der Steingolem erwacht. Felsbrocken fallen von seinem Körper, als er sich langsam aufrichtet.",
    "Dunkelritter":  "Der Dunkelritter zieht seine pechschwarze Klinge. Sein Blick ist eiskalt — keine Gnade, kein Erbarmen.",
    "Flammendämon":  "Der Flammendämon tritt aus der Lava. Sein Körper brennt wie ein lebendiger Scheiterhaufen.",
}

ROOM_ICONS = {
    "combat":   ("⚔️ ", "Kampf",        "Gegner lauern im nächsten Raum."),
    "event":    ("🎲 ", "Ereignis",     "Ein unbekanntes Ereignis erwartet dich."),
    "elite":    ("💪 ", "Elite-Gegner", "Ein starker Krieger versperrt den Weg."),
    "shrine":   ("🕯️ ", "Schrein",      "Ein uralter Schrein verbreitet mystische Energie."),
    "trap":     ("⚠️ ", "Falle",        "Dieser Raum sieht gefährlich aus..."),
    "empty":    ("🌫️ ", "Leerer Raum",  "Stille. Was auch immer hier war, ist verschwunden."),
    "miniboss": ("💀 ", "Mini-Boss",    "Ein mächtiger Einzelgegner blockiert den Weg."),
    "boss":     ("🔥 ", "Boss",         "Der Anführer dieses Dungeons wartet auf dich!"),
}

_ROOM_COLORS = {
    "combat":   "red",
    "event":    "cyan",
    "elite":    "red",
    "shrine":   "magenta",
    "trap":     "yellow",
    "empty":    "white",
    "miniboss": "red",
    "boss":     "bright_red",
}


def _generate_rooms(player_level: int) -> list:
    n = random.randint(3, 5)
    middle = []
    for _ in range(n - 1):
        rtype = random.choices(
            ["combat", "event", "elite", "shrine", "trap", "empty", "miniboss"],
            weights=[55, 10, 15,  6,  6,  4,  8],
            k=1
        )[0]
        middle.append(rtype)
    middle.append("boss")
    return middle


def _add_zone_kills(player, count: int):
    zone_id = getattr(player, "current_zone", "wald")
    zk = player.stats.setdefault("zone_kills", {})
    zk[zone_id] = zk.get(zone_id, 0) + count


def _room_loot(player, enemy_group) -> tuple:
    from core.combat import collect_loot
    from systems.achievements import check_all
    player.stats["fights"] += 1
    player.stats["kills"]  += len(enemy_group)
    _add_zone_kills(player, len(enemy_group))
    gold_before = player.inventory["Gold"]
    loot_lines  = collect_loot(player, enemy_group)
    player.stats["gold_earned"] += player.inventory["Gold"] - gold_before
    total_xp = int(sum(e.xp_value for e in enemy_group) * player.next_fight_xp_mult * player.get_xp_bonus_mult())
    player.next_fight_xp_mult = 1.0
    player.xp += total_xp
    lvl_msgs = player.check_level_up()
    loot_lines.extend(lvl_msgs)
    for m in check_all(player, {"event": "victory", "enemies": enemy_group, "potions_used": -1}):
        loot_lines.append(m)
    for m in check_all(player, {"event": "level_up", "level": player.level}):
        loot_lines.append(m)
    return loot_lines, total_xp


def _shrine_room(player):
    clear_screen()
    print_header("🕯️  Heiliger Schrein")
    console.print("  Eine göttliche Energie umgibt diesen uralten Schrein.")
    console.print("  Wähle eine Segnung:\n")
    heal_amt   = max(5, player.max_hp // 4)
    eff_max    = player.get_effective_max_energy()
    energy_gap = max(0, eff_max - player.energy)
    console.print(f"  [[H]] [green]Heilsegen[/green]     — +{heal_amt} HP")
    console.print(f"  [[E]] [blue]Energiesegen[/blue]  — +{energy_gap} Energie (vollständig auffüllen)")
    console.print(f"  [[K]] [yellow]Kampfsegen[/yellow]    — +50% XP im nächsten Kampf")
    console.print(f"  [[F]] [red]Fluch wagen[/red]   — unbekannter Effekt (gut oder schlecht)")
    choice = input("\nDeine Wahl: ").lower()
    hp_b = hp_bar(player.hp, player.max_hp)
    en_b = energy_bar(player.energy, player.max_energy)
    if choice == "e":
        player.energy = eff_max
        en_b2 = energy_bar(player.energy, eff_max)
        console.print(f"\n  [blue]Kraft strömt durch dich. +{energy_gap} Energie[/blue]")
        console.print(f"  ⚡ {en_b2} {player.energy}/{eff_max}")
    elif choice == "k":
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.5)
        console.print("\n  [yellow]Ein Kampfgeist erfasst dich. +50% XP im nächsten Kampf![/yellow]")
    elif choice == "f":
        roll = random.random()
        if roll < 0.35:
            hp_gain = max(5, player.max_hp // 3)
            player.hp = min(player.max_hp, player.hp + hp_gain)
            player.energy = eff_max
            hp_b2 = hp_bar(player.hp, player.max_hp)
            en_b2 = energy_bar(player.energy, eff_max)
            console.print(f"\n  [green]Dunkle Energie wandelt sich ins Licht! +{hp_gain} HP, volle Energie![/green]")
            console.print(f"  HP {hp_b2} {player.hp}/{player.max_hp}   ⚡ {en_b2} {player.energy}/{eff_max}")
        elif roll < 0.65:
            from content.loot_tables import roll_loot, apply_loot
            items = roll_loot(rank=3, rolls=2)
            msgs  = apply_loot(player, items)
            console.print("\n  [cyan]Der Schrein öffnet eine verborgene Kammer![/cyan]")
            for m in msgs:
                console.print(f"  {m}")
        else:
            dmg = random.randint(8, 15)
            player.hp = max(1, player.hp - dmg)
            hp_b2 = hp_bar(player.hp, player.max_hp)
            console.print(f"\n  [red]Der Schrein reagiert feindselig! -{dmg} HP[/red]")
            console.print(f"  HP {hp_b2} {player.hp}/{player.max_hp}")
    else:
        healed = min(heal_amt, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal_amt)
        hp_b2 = hp_bar(player.hp, player.max_hp)
        console.print(f"\n  [green]Der Schrein strahlt warm. +{healed} HP[/green]")
        console.print(f"  HP {hp_b2} {player.hp}/{player.max_hp}")
    input("\n(ENTER)")


def _trap_room(player):
    trap_names = [
        "Pfeilschießstand",
        "Druckplatten mit Klingen",
        "Klingenpendel",
        "Giftnebel-Falle",
    ]
    trap_name   = random.choice(trap_names)
    energy_cost = 8
    can_dodge   = player.energy >= energy_cost

    clear_screen()
    print_header(f"⚠️  Falle: {_esc(trap_name)}")
    console.print(f"  Du betrittst den Raum und erkennst zu spät: [yellow]{_esc(trap_name)}[/yellow]!\n")
    dodge_suffix = "" if can_dodge else "  [red][✗ zu wenig Energie][/red]"
    console.print(f"  [[A]] [green]Ausweichen[/green]  — kostet {energy_cost} Energie{dodge_suffix}")
    console.print(f"  [[T]] [red]Durchlaufen[/red] — nimmst 8–18 Schaden")
    choice = input("\nDeine Wahl: ").lower()

    if choice == "a" and can_dodge:
        player.energy -= energy_cost
        en_b = energy_bar(player.energy, player.max_energy)
        console.print(f"\n  [green]Du rollst geschickt durch die Falle! -{energy_cost} Energie[/green]")
        console.print(f"  ⚡ {en_b} {player.energy}/{player.max_energy}")
    elif choice == "a":
        dmg = random.randint(4, 9)
        player.hp = max(1, player.hp - dmg)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print(f"\n  [red]Du willst ausweichen, aber deine Energie reicht nicht! -{dmg} HP[/red]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    else:
        dmg = random.randint(8, 18)
        player.hp = max(1, player.hp - dmg)
        hp_b = hp_bar(player.hp, player.max_hp)
        console.print(f"\n  [red]Du läufst mitten in die Falle! -{dmg} HP[/red]")
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}")
    input("\n(ENTER)")


def _empty_room(player):
    flavors = [
        "Staubige Stille. Hier war einmal etwas — jetzt nur noch Asche.",
        "Die Wände tragen alte Kratzer. Jemand war hier, lange vor dir.",
        "Leere Kisten, zerbrochene Fackeln. Andere waren schneller.",
        "Ein verlassenes Lager. Die Glut ist noch warm.",
        "Ein langer Seufzer hallt durch den leeren Raum.",
    ]
    clear_screen()
    print_header("🌫️  Leerer Raum")
    console.print(f"  [dim]{_esc(random.choice(flavors))}[/dim]")
    console.print()
    roll = random.random()
    if roll < 0.25:
        from content.loot_tables import roll_loot, apply_loot
        items = roll_loot(rank=1, rolls=2)
        msgs  = apply_loot(player, items)
        console.print("  [cyan]Du durchsuchst den Raum sorgfältig — und wirst belohnt![/cyan]")
        for m in msgs:
            console.print(f"  {m}")
    elif roll < 0.45:
        gold = random.randint(3, 15)
        player.inventory["Gold"] += gold
        player.stats["gold_earned"] += gold
        console.print(f"  [yellow]Zwischen den Trümmern glitzert etwas. +{gold} Gold![/yellow]")
    else:
        console.print("  [dim]Du findest nichts Nützliches.[/dim]")
    input("\n(ENTER)")


def _between_room_menu(player, next_room_type: str) -> str:
    from content.loot_tables import CONSUMABLE_DEFS
    from config import MAX_INVENTORY_SLOTS
    from ui.pause import inventory_menu

    icon, label, flavor = ROOM_ICONS[next_room_type]
    c = _ROOM_COLORS.get(next_room_type, "white")

    while True:
        clear_screen()
        print_header("Rast zwischen den Räumen")
        hp_b = hp_bar(player.hp, player.max_hp)
        en_b = energy_bar(player.energy, player.max_energy)
        console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}   ⚡ {en_b} {player.energy}/{player.max_energy}")
        console.print(f"  Gold: {player.inventory['Gold']} 🪙  |  🎒 {player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots")
        console.print()
        console.print(f"  Nächster Raum:  [{c}]{icon}{_esc(label)}[/{c}]")
        console.print(f"  [dim]{_esc(flavor)}[/dim]")
        console.print()

        consumables = {k: v for k, v in player.inventory.get("Consumables", {}).items() if v > 0}
        if consumables:
            console.print("[bold][ Tränke ][/bold]")
            items = list(consumables.items())
            for i, (key, count) in enumerate(items):
                cdef  = CONSUMABLE_DEFS.get(key, {})
                emoji = cdef.get("emoji", "🧪")
                desc  = cdef.get("desc", "")
                console.print(f"  [[{i}]] {emoji} {_esc(key):<22} x{count}  — [dim]{_esc(desc)}[/dim]")
            console.print()

        equip_count = len(player.inventory.get("Equipment", []))
        console.print(f"  [[A]] Ausrüstung verwalten  ({equip_count} Items im Inventar)")
        console.print("  [[W]] [bold green]Weiter in nächsten Raum[/bold green]")
        console.print("  [[F]] [dim]Dungeon verlassen  (kein Abschluss, kein Loot)[/dim]")

        choice = input("\nDeine Wahl: ").lower()

        if choice == 'w':
            return "continue"
        elif choice == 'f':
            return "flee"
        elif choice == 'a':
            inventory_menu(player)
        elif choice.isdigit():
            idx   = int(choice)
            items = list(consumables.items())
            if 0 <= idx < len(items):
                key = items[idx][0]
                console.print(f"\n{player.use_consumable(key)}")
                input("(ENTER)")


def _run_combat_room(player, enemies, room_num) -> str:
    """Führt einen Kampf-Raum durch (combat + reset + loot-Anzeige).
    Gibt 'defeat', 'fled' oder 'ok' zurück."""
    from core.combat import combat
    from systems.achievements import check_all
    result = combat(player, enemies)
    player.reset_combat_modifiers()
    if result in ("defeat", "fled"):
        return result
    clear_screen()
    print_header(f"Raum {room_num} geleert!")
    loot_lines, xp = _room_loot(player, enemies)
    if loot_lines:
        console.print("  [bold]Beute:[/bold]")
        for line in loot_lines:
            console.print(f"  {line}")
    console.print(f"\n  [bold green]+{xp} XP[/bold green]")
    input("\n(ENTER)")
    return "ok"


def run_dungeon(player, meta) -> str:
    """
    Vollständiger Dungeon-Durchlauf.
    Rückgabe: 'completed' | 'fled' | 'defeat'
    """
    from core.combat import generate_enemy_group, combat
    from systems.zones import create_zone_enemy
    from systems.events import trigger_event
    from systems.achievements import check_all
    from content.loot_tables import roll_loot, roll_zone_loot, roll_boss_loot, apply_loot

    rooms = _generate_rooms(player.level)
    total = len(rooms)
    zone_id = getattr(player, "current_zone", "wald")
    dungeon_name = random.choice(DUNGEON_NAMES.get(zone_id, DUNGEON_NAMES["wald"]))

    if getattr(player, "spiegel", {}).get("kriegserfahrung") == "B":
        player.spiegel_first_fight = True

    # Dungeon-Einstieg
    clear_screen()
    print_header(f"🗡️  {_esc(dungeon_name)}")
    preview_parts = []
    for r in rooms:
        icon, lbl, _ = ROOM_ICONS[r]
        c = _ROOM_COLORS.get(r, "white")
        preview_parts.append(f"[{c}]{icon}{_esc(lbl)}[/{c}]")
    console.print("  Räume (" + str(total) + "):  " + "  →  ".join(preview_parts))
    console.print()
    hp_b = hp_bar(player.hp, player.max_hp)
    en_b = energy_bar(player.energy, player.max_energy)
    console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}   ⚡ {en_b} {player.energy}/{player.max_energy}")
    input("\n🗡️  Betreten (ENTER)")

    for i, room_type in enumerate(rooms):
        room_num = i + 1

        # Zwischen-Raum-Menü (nicht vor Raum 1)
        if i > 0:
            if _between_room_menu(player, room_type) == "flee":
                player.stats["dungeons_fled"] = player.stats.get("dungeons_fled", 0) + 1
                clear_screen()
                console.print("  [dim]Du verlässt den Dungeon. Kein Abschluss, kein Loot, keine HP-Heilung.[/dim]")
                input("(ENTER)")
                return "fled"

        clear_screen()
        icon, label, _ = ROOM_ICONS[room_type]
        c = _ROOM_COLORS.get(room_type, "white")
        console.print()
        console.rule(f"[bold]Raum {room_num}/{total}  —  {icon}{_esc(label)}[/bold]", style=c)
        console.print()

        # ── Kampf-Raum ────────────────────────────────────────
        if room_type == "combat":
            enemies = generate_enemy_group(player)
            console.print(f"  [red]{', '.join(_esc(e.name) for e in enemies)} erscheinen![/red]")
            input("  Bereit machen... (ENTER)")
            outcome = _run_combat_room(player, enemies, room_num)
            if outcome in ("defeat", "fled"):
                return outcome

        # ── Elite-Raum ────────────────────────────────────────
        elif room_type == "elite":
            elite = create_zone_enemy(player, forced_rank=2)
            console.print(f"  [bold red]💪 {_esc(elite.name)} stellt sich dir entgegen![/bold red]")
            input("  Bereit machen... (ENTER)")
            outcome = _run_combat_room(player, [elite], room_num)
            if outcome in ("defeat", "fled"):
                return outcome
            from systems.runen import check_rune_drop, rune_found_msgs
            rid = check_rune_drop(meta, "elite")
            if rid:
                for m in rune_found_msgs(rid):
                    console.print(f"  {m}")
                input("  (ENTER)")

        # ── Ereignis-Raum ─────────────────────────────────────
        elif room_type == "event":
            trigger_event(player, meta)
            if not player.is_alive():
                return "defeat"

        # ── Schrein-Raum ──────────────────────────────────────
        elif room_type == "shrine":
            _shrine_room(player)
            if not player.is_alive():
                return "defeat"

        # ── Fallen-Raum ───────────────────────────────────────
        elif room_type == "trap":
            _trap_room(player)
            if not player.is_alive():
                return "defeat"

        # ── Leerer Raum ───────────────────────────────────────
        elif room_type == "empty":
            _empty_room(player)

        # ── Mini-Boss-Raum ────────────────────────────────────
        elif room_type == "miniboss":
            miniboss = create_zone_enemy(player, forced_rank=3)
            console.print(f"  [bold red]💀 {_esc(miniboss.name)} versperrt den Weg![/bold red]")
            input("  Bereit machen... (ENTER)")
            outcome = _run_combat_room(player, [miniboss], room_num)
            if outcome in ("defeat", "fled"):
                return outcome

        # ── Boss-Raum ─────────────────────────────────────────
        elif room_type == "boss":
            lvl = player.level
            if lvl <= 3:
                boss_rank = random.choices([2, 3], weights=[55, 45])[0]
            elif lvl <= 5:
                boss_rank = random.choices([3, 4], weights=[60, 40])[0]
            elif lvl <= 7:
                boss_rank = random.choices([3, 4, 5], weights=[20, 50, 30])[0]
            else:
                boss_rank = random.choices([4, 5], weights=[55, 45])[0]
            boss      = create_zone_enemy(player, forced_rank=boss_rank)
            clear_screen()
            print_header(f"🔥 BOSS  —  {_esc(boss.name)}")
            base_name = type(boss).__name__
            name_map = {
                "Zombie": "Zombie", "Skeleton": "Skelett", "Slime": "Schleim",
                "Goblin": "Goblin", "Dragon": "Drache", "Bandit": "Bandit",
                "WoodTroll": "Waldtroll", "ShadowWolf": "Schattenwolf",
                "VenomSpider": "Giftige Spinne", "Assassin": "Meuchler",
                "IceWitch": "Eismagierin", "StoneGolem": "Steingolem",
                "DarkKnight": "Dunkelritter", "FireDemon": "Flammendämon",
            }
            intro_key = name_map.get(base_name, "")
            intro = BOSS_INTROS.get(intro_key, "Der Anführer dieses Dungeons stellt sich dir entgegen!")
            console.print(Panel(
                f"[bold]{_esc(intro)}[/bold]",
                border_style="bright_red",
                expand=False,
                padding=(0, 2),
            ))
            console.print()
            console.print("  [bold bright_red]⚔️  In den Kampf![/bold bright_red]")
            input("  (ENTER) ")
            pots_before = player.stats.get("potions_used", 0)
            result = combat(player, [boss])
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeat"
            if result == "fled":
                return "fled"

            # Boss-Sieg: Bonus-Loot
            clear_screen()
            print_header("🏆 Boss besiegt!")
            player.stats["fights"] += 1
            player.stats["kills"]  += 1
            _add_zone_kills(player, 1)
            gold_before  = player.inventory["Gold"]
            extra_rolls  = 2 if getattr(player, "spiegel", {}).get("glueck") == "B" else 1
            loot_items   = roll_zone_loot(zone_id, rolls=boss.loot_rolls + extra_rolls)
            msgs         = apply_loot(player, loot_items)
            player.stats["gold_earned"] += player.inventory["Gold"] - gold_before
            total_xp     = int(boss.xp_value * player.next_fight_xp_mult * player.get_xp_bonus_mult())
            player.next_fight_xp_mult = 1.0
            player.xp   += total_xp
            lvl_msgs = player.check_level_up()
            if msgs:
                console.print("\n  [bold yellow]💰 Boss-Beute:[/bold yellow]")
                for m in msgs:
                    console.print(f"  {m}")
            for m in lvl_msgs:
                console.print(f"  {m}")
            console.print(f"\n  [bold green]+{total_xp} XP[/bold green]")
            if boss_rank == 5:
                from systems.runen import check_rune_drop, rune_found_msgs
                rid = check_rune_drop(meta, "dungeon_boss")
                if rid:
                    console.print()
                    for m in rune_found_msgs(rid):
                        console.print(f"  {m}")
            pots_used = player.stats.get("potions_used", 0) - pots_before
            for m in check_all(player, {"event": "victory", "enemies": [boss], "potions_used": pots_used}):
                console.print(f"  {m}")
            for m in check_all(player, {"event": "level_up", "level": player.level}):
                console.print(f"  {m}")
            input("\n(ENTER)")

    # ── Dungeon abgeschlossen ─────────────────────────────────
    from systems.zones import ZONE_DEFS
    from systems.world_map import ZONE_BOSS_DEFS

    player.stats["dungeons_completed"] = player.stats.get("dungeons_completed", 0) + 1
    zones_cleared = player.stats.setdefault("zones_cleared", [])
    if zone_id not in zones_cleared:
        zones_cleared.append(zone_id)

    # zone_progress aktualisieren
    zp = getattr(player, "zone_progress", {})
    if zone_id not in zp:
        zp[zone_id] = {"dungeons_completed": 0, "boss_defeated": False}
    zp[zone_id]["dungeons_completed"] = zp[zone_id].get("dungeons_completed", 0) + 1
    player.zone_progress = zp

    clear_screen()
    print_header("✅ Dungeon abgeschlossen!")
    console.print("  Du kämpfst dich siegreich aus dem Dungeon heraus.\n")
    player.hp     = player.max_hp
    player.energy = player.get_effective_max_energy()
    hp_b = hp_bar(player.hp, player.max_hp)
    en_b = energy_bar(player.energy, player.get_effective_max_energy())
    console.print(f"  [green]💚 HP vollständig wiederhergestellt![/green]      {hp_b} {player.hp}/{player.max_hp}")
    console.print(f"  [blue]⚡ Energie vollständig wiederhergestellt![/blue] {en_b} {player.energy}/{player.get_effective_max_energy()}")

    # Boss-Benachrichtigung wenn Ziel erreicht
    req  = ZONE_DEFS[zone_id]["dungeon_count"]
    done = zp[zone_id]["dungeons_completed"]
    if done >= req and not zp[zone_id].get("boss_defeated", False):
        bdef = ZONE_BOSS_DEFS[zone_id]
        console.print(f"\n  [bold red]🔥 Zonen-Ziel erreicht! ({done}/{req} Dungeons)[/bold red]")
        console.print(f"  [red]{_esc(bdef['name'])} kann nun herausgefordert werden![/red]")

    from config import RUNENESSENZ_DUNGEON
    from core.save import save_run, add_runenessenz
    essenz = random.randint(*RUNENESSENZ_DUNGEON)
    add_runenessenz(meta, essenz)
    console.print(f"\n  [bold cyan]💠 +{essenz} Runenessenz[/bold cyan]  [dim](Gesamt: {meta['runenessenz']})[/dim]")

    for m in check_all(player, {"event": "dungeon_complete", "zone_id": zone_id}):
        console.print(f"  {m}")

    input("\n(ENTER)")

    from ui.segnungen_ui import choose_segnung_menu
    choose_segnung_menu(player)

    save_run(player, quiet=True)
    return "completed"
