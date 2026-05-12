import random
from ui.utils import clear_screen, print_header

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


def _create_scaled_enemy(player, forced_rank: int):
    from systems.zones import ZONE_DEFS
    zone_id = getattr(player, "current_zone", "wald")
    zdef = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
    classes, weights = zip(*zdef["monsters"])
    mob_class = random.choices(list(classes), weights=list(weights), k=1)[0]
    enemy = mob_class(rank=forced_rank)
    diff = getattr(player, "difficulty", "normal")
    if diff != "normal":
        from config import DIFFICULTY_SETTINGS
        cfg = DIFFICULTY_SETTINGS[diff]
        enemy.max_hp = max(1, int(enemy.max_hp * cfg["hp_mult"]))
        enemy.hp     = enemy.max_hp
        enemy.attack = max(1, int(enemy.attack * cfg["atk_mult"]))
    ng = getattr(player, "ng_plus", 0)
    if ng > 0:
        mult         = 1.3 ** ng
        enemy.max_hp = max(1, int(enemy.max_hp * mult))
        enemy.hp     = enemy.max_hp
        enemy.attack = max(1, int(enemy.attack * mult))

    # Basis-Buff normale Gegner (+10%)
    enemy.max_hp = max(1, int(enemy.max_hp * 1.1))
    enemy.hp     = enemy.max_hp
    enemy.attack = max(1, int(enemy.attack * 1.1))

    return enemy


def _add_zone_kills(player, count: int):
    zone_id = getattr(player, "current_zone", "wald")
    zk = player.stats.setdefault("zone_kills", {})
    zk[zone_id] = zk.get(zone_id, 0) + count


def _room_loot(player, enemy_group) -> tuple:
    from core.combat import collect_loot
    player.stats["fights"] += 1
    player.stats["kills"]  += len(enemy_group)
    _add_zone_kills(player, len(enemy_group))
    gold_before = player.inventory["Gold"]
    loot_lines  = collect_loot(player, enemy_group)
    player.stats["gold_earned"] += player.inventory["Gold"] - gold_before
    total_xp = int(sum(e.xp_value for e in enemy_group) * player.next_fight_xp_mult)
    player.next_fight_xp_mult = 1.0
    player.xp += total_xp
    player.check_level_up()
    return loot_lines, total_xp


def _shrine_room(player):
    clear_screen()
    print_header("🕯️  Heiliger Schrein")
    print("Eine göttliche Energie umgibt diesen uralten Schrein.")
    print("Wähle eine Segnung:\n")
    heal_amt   = max(5, player.max_hp // 4)
    energy_gap = player.max_energy - player.energy
    print(f"  [H] Heilsegen     — +{heal_amt} HP")
    print(f"  [E] Energiesegen  — +{energy_gap} Energie (vollständig auffüllen)")
    print(f"  [K] Kampfsegen    — +50% XP im nächsten Kampf")
    print(f"  [F] Fluch wagen   — unbekannter Effekt (gut oder schlecht)")
    choice = input("\nDeine Wahl: ").lower()
    if choice == "e":
        player.energy = player.max_energy
        print(f"\nKraft strömt durch dich. +{energy_gap} Energie  (Energie: {player.energy}/{player.max_energy})")
    elif choice == "k":
        player.next_fight_xp_mult = max(player.next_fight_xp_mult, 1.5)
        print("\nEin Kampfgeist erfasst dich. +50% XP im nächsten Kampf!")
    elif choice == "f":
        roll = random.random()
        if roll < 0.35:
            hp_gain = max(5, player.max_hp // 3)
            player.hp = min(player.max_hp, player.hp + hp_gain)
            player.energy = player.max_energy
            print(f"\nDunkle Energie wandelt sich ins Licht! +{hp_gain} HP, volle Energie!")
        elif roll < 0.65:
            from content.loot_tables import roll_loot, apply_loot
            items = roll_loot(rank=3, rolls=2)
            msgs  = apply_loot(player, items)
            print("\nDer Schrein öffnet eine verborgene Kammer!")
            for m in msgs:
                print(m)
        else:
            dmg = random.randint(8, 15)
            player.hp = max(1, player.hp - dmg)
            print(f"\nDer Schrein reagiert feindselig! -{dmg} HP  (HP: {player.hp}/{player.max_hp})")
    else:
        healed = min(heal_amt, player.max_hp - player.hp)
        player.hp = min(player.max_hp, player.hp + heal_amt)
        print(f"\nDer Schrein strahlt warm. +{healed} HP  (HP: {player.hp}/{player.max_hp})")
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
    print_header(f"⚠️  Falle: {trap_name}")
    print(f"Du betrittst den Raum und erkennst zu spät: {trap_name}!\n")
    print(f"  [A] Ausweichen  — kostet {energy_cost} Energie  {'[✓]' if can_dodge else '[✗ zu wenig Energie]'}")
    print(f"  [T] Durchlaufen — nimmst 8–18 Schaden")
    choice = input("\nDeine Wahl: ").lower()

    if choice == "a" and can_dodge:
        player.energy -= energy_cost
        print(f"\nDu rollst geschickt durch die Falle! -{energy_cost} Energie  (Energie: {player.energy}/{player.max_energy})")
    elif choice == "a":
        dmg = random.randint(4, 9)
        player.hp = max(1, player.hp - dmg)
        print(f"\nDu willst ausweichen, aber deine Energie reicht nicht! -{dmg} HP  (HP: {player.hp}/{player.max_hp})")
    else:
        dmg = random.randint(8, 18)
        player.hp = max(1, player.hp - dmg)
        print(f"\nDu läufst mitten in die Falle! -{dmg} HP  (HP: {player.hp}/{player.max_hp})")
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
    print(random.choice(flavors))
    print()
    roll = random.random()
    if roll < 0.25:
        from content.loot_tables import roll_loot, apply_loot
        items = roll_loot(rank=1, rolls=2)
        msgs  = apply_loot(player, items)
        print("Du durchsuchst den Raum sorgfältig — und wirst belohnt!")
        for m in msgs:
            print(m)
    elif roll < 0.45:
        gold = random.randint(3, 15)
        player.inventory["Gold"] += gold
        player.stats["gold_earned"] += gold
        print(f"Zwischen den Trümmern glitzert etwas. +{gold} Gold!")
    else:
        print("Du findest nichts Nützliches.")
    input("\n(ENTER)")


def _between_room_menu(player, next_room_type: str) -> str:
    from content.loot_tables import CONSUMABLE_DEFS
    from core.player import MAX_INVENTORY_SLOTS
    from ui.pause import inventory_menu

    icon, label, flavor = ROOM_ICONS[next_room_type]

    while True:
        clear_screen()
        print_header("Rast zwischen den Räumen")
        print(f"HP: {player.hp}/{player.max_hp}  |  Energie: {player.energy}/{player.max_energy}")
        print(f"Gold: {player.inventory['Gold']} 🪙  |  🎒 {player.inventory_count()}/{MAX_INVENTORY_SLOTS} Slots")
        print()
        print(f"  Nächster Raum:  {icon} {label}")
        print(f"  {flavor}")
        print()

        consumables = {k: v for k, v in player.inventory.get("Consumables", {}).items() if v > 0}
        if consumables:
            print("[ Tränke ]")
            items = list(consumables.items())
            for i, (key, count) in enumerate(items):
                cdef  = CONSUMABLE_DEFS.get(key, {})
                emoji = cdef.get("emoji", "🧪")
                desc  = cdef.get("desc", "")
                print(f"  [{i}] {emoji} {key:<22} x{count}  — {desc}")
            print()

        equip_count = len(player.inventory.get("Equipment", []))
        print(f"  [A] Ausrüstung verwalten  ({equip_count} Items im Inventar)")
        print("  [W] Weiter in nächsten Raum")
        print("  [F] Dungeon verlassen  (kein Abschluss, kein Loot)")

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
                print(f"\n{player.use_consumable(key)}")
                input("(ENTER)")


def run_dungeon(player) -> str:
    """
    Vollständiger Dungeon-Durchlauf.
    Rückgabe: 'completed' | 'fled' | 'defeat'
    """
    from core.combat import generate_enemy_group, combat
    from systems.events import trigger_event
    from systems.achievements import check_all
    from content.loot_tables import roll_loot, apply_loot

    rooms = _generate_rooms(player.level)
    total = len(rooms)
    zone_id = getattr(player, "current_zone", "wald")
    dungeon_name = random.choice(DUNGEON_NAMES.get(zone_id, DUNGEON_NAMES["wald"]))

    # Dungeon-Einstieg
    clear_screen()
    print_header(f"🗡️  {dungeon_name}")
    preview = "  →  ".join(f"{ROOM_ICONS[r][0]}{ROOM_ICONS[r][1]}" for r in rooms)
    print(f"Räume ({total}):  {preview}")
    print(f"\nHP: {player.hp}/{player.max_hp}  |  Energie: {player.energy}/{player.max_energy}")
    input("\n🗡️  Betreten (ENTER)")

    for i, room_type in enumerate(rooms):
        room_num = i + 1

        # Zwischen-Raum-Menü (nicht vor Raum 1)
        if i > 0:
            if _between_room_menu(player, room_type) == "flee":
                player.stats["dungeons_fled"] = player.stats.get("dungeons_fled", 0) + 1
                clear_screen()
                print("Du verlässt den Dungeon. Kein Abschluss, kein Loot, keine HP-Heilung.")
                input("(ENTER)")
                return "fled"

        clear_screen()
        icon, label, _ = ROOM_ICONS[room_type]
        print_header(f"Raum {room_num}/{total}  —  {icon} {label}")

        # ── Kampf-Raum ────────────────────────────────────────
        if room_type == "combat":
            enemies = generate_enemy_group(player)
            print(f"--- {', '.join(e.name for e in enemies)} erscheinen! ---")
            input("Bereit machen... (ENTER)")
            result = combat(player, enemies)
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeat"
            if result == "fled":
                return "fled"
            clear_screen()
            print_header(f"Raum {room_num} geleert!")
            loot_lines, xp = _room_loot(player, enemies)
            if loot_lines:
                print("Beute:")
                for line in loot_lines:
                    print(line)
            print(f"\n+{xp} XP")
            input("\n(ENTER)")

        # ── Elite-Raum ────────────────────────────────────────
        elif room_type == "elite":
            elite = _create_scaled_enemy(player, forced_rank=2)
            print(f"--- 💪 {elite.name} stellt sich dir entgegen! ---")
            input("Bereit machen... (ENTER)")
            result = combat(player, [elite])
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeat"
            if result == "fled":
                return "fled"
            clear_screen()
            print_header(f"Raum {room_num} geleert!")
            loot_lines, xp = _room_loot(player, [elite])
            if loot_lines:
                print("Beute:")
                for line in loot_lines:
                    print(line)
            print(f"\n+{xp} XP")
            input("\n(ENTER)")

        # ── Ereignis-Raum ─────────────────────────────────────
        elif room_type == "event":
            trigger_event(player)
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
            miniboss = _create_scaled_enemy(player, forced_rank=3)
            print(f"--- 💀 {miniboss.name} versperrt den Weg! ---")
            input("Bereit machen... (ENTER)")
            result = combat(player, [miniboss])
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeat"
            if result == "fled":
                return "fled"
            clear_screen()
            print_header(f"Raum {room_num} geleert!")
            loot_lines, xp = _room_loot(player, [miniboss])
            if loot_lines:
                print("Beute:")
                for line in loot_lines:
                    print(line)
            print(f"\n+{xp} XP")
            input("\n(ENTER)")

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
            boss      = _create_scaled_enemy(player, forced_rank=boss_rank)
            clear_screen()
            print_header(f"🔥 BOSS  —  {boss.name}")
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
            print(intro)
            input("\nIn den Kampf! (ENTER)")
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
            loot_items   = roll_loot(rank=boss_rank, rolls=boss.loot_rolls)
            msgs         = apply_loot(player, loot_items)
            player.stats["gold_earned"] += player.inventory["Gold"] - gold_before
            total_xp     = int(boss.xp_value * player.next_fight_xp_mult)
            player.next_fight_xp_mult = 1.0
            player.xp   += total_xp
            player.check_level_up()
            if msgs:
                print("\n💰 Boss-Beute:")
                for m in msgs:
                    print(m)
            print(f"\n+{total_xp} XP")
            for m in check_all(player, {"event": "victory", "enemies": [boss]}):
                print(m)
            for m in check_all(player, {"event": "level_up", "level": player.level}):
                print(m)
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
    print("Du kämpfst dich siegreich aus dem Dungeon heraus.\n")
    player.hp     = player.max_hp
    player.energy = player.max_energy
    print(f"💚 HP vollständig wiederhergestellt!      ({player.hp}/{player.max_hp})")
    print(f"⚡ Energie vollständig wiederhergestellt! ({player.energy}/{player.max_energy})")

    # Boss-Benachrichtigung wenn Ziel erreicht
    req  = ZONE_DEFS[zone_id]["dungeon_count"]
    done = zp[zone_id]["dungeons_completed"]
    if done >= req and not zp[zone_id].get("boss_defeated", False):
        bdef = ZONE_BOSS_DEFS[zone_id]
        print(f"\n🔥 Zonen-Ziel erreicht! ({done}/{req} Dungeons)")
        print(f"   {bdef['name']} kann nun herausgefordert werden!")

    for m in check_all(player, {"event": "dungeon_complete", "zone_id": zone_id}):
        print(m)
    input("\n(ENTER)")
    return "completed"
