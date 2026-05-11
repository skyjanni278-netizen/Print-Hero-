import random
from ui.utils import clear_screen, print_header

ROOM_ICONS = {
    "combat":   ("⚔️ ", "Kampf",     "Gegner lauern im nächsten Raum."),
    "event":    ("🎲 ", "Ereignis",  "Ein unbekanntes Ereignis erwartet dich."),
    "miniboss": ("💀 ", "Mini-Boss", "Ein mächtiger Einzelgegner blockiert den Weg."),
    "boss":     ("🔥 ", "Boss",      "Der Anführer dieses Dungeons wartet auf dich!"),
}


def _generate_rooms(player_level: int) -> list:
    n = random.randint(3, 5)
    middle = []
    for _ in range(n - 1):
        rtype = random.choices(
            ["combat", "event", "miniboss"],
            weights=[65, 20, 15],
            k=1
        )[0]
        middle.append(rtype)
    middle.append("boss")
    return middle


def _create_scaled_enemy(player, forced_rank: int):
    from core.combat import create_enemy
    base = create_enemy(player)
    cls  = base.__class__
    enemy = cls(rank=forced_rank)
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
    return enemy


def _room_loot(player, enemy_group) -> tuple:
    from core.combat import collect_loot
    player.stats["fights"] += 1
    player.stats["kills"]  += len(enemy_group)
    gold_before = player.inventory["Gold"]
    loot_lines  = collect_loot(player, enemy_group)
    player.stats["gold_earned"] += player.inventory["Gold"] - gold_before
    total_xp = int(sum(e.xp_value for e in enemy_group) * player.next_fight_xp_mult)
    player.next_fight_xp_mult = 1.0
    player.xp += total_xp
    player.check_level_up()
    return loot_lines, total_xp


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
    Rückgabe: 'completed' | 'fled' | 'defeated'
    """
    from core.combat import generate_enemy_group, combat
    from systems.events import trigger_event
    from systems.achievements import check_all
    from content.loot_tables import roll_loot, apply_loot

    rooms = _generate_rooms(player.level)
    total = len(rooms)

    # Dungeon-Einstieg
    clear_screen()
    print_header("Dungeon betreten")
    preview = "  →  ".join(f"{ROOM_ICONS[r][0]}{ROOM_ICONS[r][1]}" for r in rooms)
    print(f"Räume ({total}):  {preview}")
    print(f"\nHP: {player.hp}/{player.max_hp}  |  Energie: {player.energy}/{player.max_energy}")
    input("\n🗡️  Betreten (ENTER)")

    for i, room_type in enumerate(rooms):
        room_num = i + 1

        # Zwischen-Raum-Menü (nicht vor Raum 1)
        if i > 0:
            if _between_room_menu(player, room_type) == "flee":
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
                return "defeated"
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

        # ── Ereignis-Raum ─────────────────────────────────────
        elif room_type == "event":
            trigger_event(player)
            if not player.is_alive():
                return "defeated"

        # ── Mini-Boss-Raum ────────────────────────────────────
        elif room_type == "miniboss":
            miniboss = _create_scaled_enemy(player, forced_rank=3)
            print(f"--- 💀 {miniboss.name} versperrt den Weg! ---")
            input("Bereit machen... (ENTER)")
            result = combat(player, [miniboss])
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeated"
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
            boss_rank = random.choices([4, 5], weights=[55, 45])[0]
            boss      = _create_scaled_enemy(player, forced_rank=boss_rank)
            clear_screen()
            print_header(f"🔥 BOSS  —  {boss.name}")
            print("Der Anführer dieses Dungeons stellt sich dir entgegen!")
            input("\nIn den Kampf! (ENTER)")
            result = combat(player, [boss])
            player.reset_combat_modifiers()
            if result == "defeat":
                return "defeated"
            if result == "fled":
                return "fled"

            # Boss-Sieg: Bonus-Loot
            clear_screen()
            print_header("🏆 Boss besiegt!")
            player.stats["fights"] += 1
            player.stats["kills"]  += 1
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
    clear_screen()
    print_header("✅ Dungeon abgeschlossen!")
    print("Du kämpfst dich siegreich aus dem Dungeon heraus.\n")
    player.hp     = player.max_hp
    player.energy = player.max_energy
    print(f"💚 HP vollständig wiederhergestellt!      ({player.hp}/{player.max_hp})")
    print(f"⚡ Energie vollständig wiederhergestellt! ({player.energy}/{player.max_energy})")
    input("\n(ENTER)")
    return "completed"
