import random
from monsters import Zombie, Slime, Goblin, Skeleton, Dragon, Bandit, WoodTroll, ShadowWolf, roll_rank
from utils import clear_screen, print_header
from loot_tables import roll_loot, apply_loot, CONSUMABLE_DEFS


def generate_enemy_group(player):
    lvl = player.level
    # Frühe Level: nur 1–2 Gegner; ab LVL 5: bis 3; ab LVL 8: bis 4
    if lvl <= 4:
        count = random.randint(1, 2)
    elif lvl <= 7:
        count = random.randint(1, 3)
    else:
        count = random.randint(2, 4)
    return [create_enemy(player) for _ in range(count)]


def create_enemy(player):
    lvl = player.level

    if lvl <= 2:
        # Nur die einfachsten Gegner
        classes = [Slime,  ShadowWolf, Goblin]
        weights = [45,     35,         20]

    elif lvl <= 4:
        # Schleime werden seltener, Banditen & Zombies kommen dazu
        classes = [Slime,  ShadowWolf, Goblin, Bandit, Zombie]
        weights = [20,     30,         20,     15,     15]

    elif lvl <= 6:
        # Schleime verschwinden, Waldtroll und Skelett tauchen auf
        classes = [ShadowWolf, Goblin, Bandit, Zombie, WoodTroll, Skeleton]
        weights = [20,         15,     20,     20,     15,        10]

    elif lvl <= 8:
        # Schattenwölfe verschwinden, Drachen tauchen auf
        classes = [Goblin, Bandit, Zombie, WoodTroll, Skeleton, Dragon]
        weights = [10,     20,     15,     20,        25,       10]

    else:
        # LVL 9–10: Nur starke Gegner, keine schwachen mehr
        classes = [Bandit, WoodTroll, Skeleton, Dragon]
        weights = [10,     25,        35,       30]

    mob_class = random.choices(classes, weights=weights, k=1)[0]
    rank      = roll_rank(player.level)
    mob       = mob_class(rank=rank)

    diff = getattr(player, "difficulty", "normal")
    if diff != "normal":
        from config import DIFFICULTY_SETTINGS
        cfg = DIFFICULTY_SETTINGS[diff]
        mob.max_hp = max(1, int(mob.max_hp * cfg["hp_mult"]))
        mob.hp     = mob.max_hp
        mob.attack = max(1, int(mob.attack * cfg["atk_mult"]))

    ng = getattr(player, "ng_plus", 0)
    if ng > 0:
        ng_mult    = 1.3 ** ng
        mob.max_hp = max(1, int(mob.max_hp * ng_mult))
        mob.hp     = mob.max_hp
        mob.attack = max(1, int(mob.attack * ng_mult))

    return mob


def consumable_menu(player) -> str:
    clear_screen()
    print_header("Verbrauchsgegenstände")

    consumables = player.inventory.get("Consumables", {})
    available = {k: v for k, v in consumables.items() if v > 0}

    if not available:
        return "Keine Verbrauchsgegenstände vorhanden!"

    items_list = list(available.items())
    print(f"HP: {player.hp}/{player.max_hp}  |  Energie: {player.energy}/{player.max_energy}")
    if player.bleed_stacks > 0:
        print(f"⚠️  Blutung: {player.bleed_stacks} Stacks")
    print("-" * 40)

    for i, (key, count) in enumerate(items_list):
        cdef = CONSUMABLE_DEFS.get(key, {})
        emoji = cdef.get("emoji", "🧪")
        desc  = cdef.get("desc", "")
        print(f"[{i+1}] {emoji} {key:<22} x{count}  — {desc}")

    print(f"\n[0] Zurück (kein Zug verbraucht)")

    choice = input("\nWelches Item benutzen? ")
    if choice == "0" or not choice.isdigit():
        return ""

    idx = int(choice) - 1
    if not (0 <= idx < len(items_list)):
        return "Ungültige Auswahl."

    key = items_list[idx][0]
    return player.use_consumable(key)


def combat(player, enemy_list):
    while player.is_alive() and any(e.is_alive() for e in enemy_list):
        clear_screen()
        print_header("Kampf-Modus")

        # Player stats
        print(f"{player.name:<4} HP: {player.hp}/{player.max_hp} | Energie: {player.energy}/{player.max_energy}")
        print(f"     LVL: {player.level}    | XP: {player.xp}/{player.xp_to_level_up}")
        if player.bleed_stacks > 0:
            print(f"     ⚠️  Blutung: {player.bleed_stacks} Stacks")
        if player.poison_stacks > 0:
            print(f"     ☠️  Gift: {player.poison_stacks} Stacks")
        if player.armor_debuff > 0:
            print(f"     🟢 Säure-Debuff: -{player.armor_debuff} DEF")
        if player.stunned:
            print(f"     🪨 BETÄUBT — überspringt diese Runde!")
        print("-" * 30)

        # Consumables Kurzübersicht
        consumables = player.inventory.get("Consumables", {})
        total_consumables = sum(v for v in consumables.values())
        print(f"Inventar:  💊 Gegenstände: {total_consumables} | 💰 Gold: {player.inventory.get('Gold', 0)}")
        print("-" * 30)

        # Show all enemies
        print("GEGNER:")
        for i, e in enumerate(enemy_list):
            rank_label = f"[Rang {e.rank}]" if hasattr(e, "rank") else ""
            status = f"HP: {e.hp}/{e.max_hp}" if e.is_alive() else "BESIEGT"
            print(f"[{i+1}] {e.name:<22} {rank_label:<10} {status}")

        print("=" * 30)
        # Verfügbare Fähigkeiten abhängig vom Level
        has_cleave       = player.level >= 2
        has_whirlwind    = player.level >= 3
        has_heavenstrike = player.level >= 5
        has_shield       = player.shield_ready

        # Fokus-Skill + Magier-Klasse: Spezialfähigkeiten kosten weniger Energie
        total_red = player._energy_cost_reduction()
        cost_s = max(5, 20 - total_red)
        cost_r = max(5, 15 - total_red)
        cost_c = max(5, 10 - total_red)

        # Klassen-Fähigkeit
        from classes import CLASS_DEFS
        pclass       = player.player_class
        cdef         = CLASS_DEFS.get(pclass, {})
        ability_used = player.class_ability_used
        ability_label = f"[X] {cdef.get('ability_name','?')} (einmal/Kampf)"

        # Aktionsmenü dynamisch aufbauen
        action_lines = ["[A] Angreifen"]
        if has_heavenstrike:
            action_lines.append(f"[S] Himmelsschlag {cost_s} E")
        else:
            action_lines.append(f"[S] Himmelsschlag — 🔒 ab LVL 5")
        if has_whirlwind:
            action_lines.append(f"[R] Rundumschlag {cost_r} E")
        else:
            action_lines.append(f"[R] Rundumschlag  — 🔒 ab LVL 3")
        if has_cleave:
            action_lines.append(f"[C] Cleave {cost_c} E")
        else:
            action_lines.append(f"[C] Cleave        — 🔒 ab LVL 2")
        if has_shield:
            action_lines.append("[M] Magieschild (Block)")
        if not ability_used:
            action_lines.append(ability_label)
        action_lines += ["[U] Verbrauchsgegenstände", "[F] Fliehen", "[Q] Beenden"]

        # Betäubung: Spielerzug überspringen
        if player.stunned:
            player.stunned = False
            print("\n🪨 Du bist betäubt und kannst nicht handeln!")
            input("ENTER...")
            choice = "__stunned__"
        else:
            choice = input("\n" + " | ".join(action_lines[:4]) + "\n" + " | ".join(action_lines[4:]) + "\nDeine Wahl: ").lower()

        if choice == "__stunned__":
            pass  # Direkt zu Gegner-Angriffen
        elif choice not in ['a', 's', 'r', 'c', 'm', 'x', 'u', 'f', 'q']:
            print("\nUngültige Taste! Bitte wähle eine der angezeigten Optionen.")
            input("ENTER...")
            continue

        # Klassen-Fähigkeit
        if choice == 'x':
            if ability_used:
                print("Klassenfähigkeit bereits benutzt!")
                input("ENTER...")
                continue
            player.class_ability_used = True
            clear_screen()
            print_header("Klassenfähigkeit")
            if pclass == "warrior":
                player.block_next = True
                print(f"🛡️  Schildwall! Nächster Angriff wird vollständig geblockt.")
            elif pclass == "mage":
                living = [e for e in enemy_list if e.is_alive()]
                dmg    = random.randint(25, 40)
                for e in living:
                    e.hp = max(0, e.hp - dmg)
                names = ", ".join(e.name for e in living)
                print(f"✨ Arkane Entladung! {dmg} Schaden (ignoriert DEF) an: {names}")
                player.stats["damage_dealt"] += dmg * len(living)
            elif pclass == "rogue":
                player.shadow_strike_ready = True
                print(f"🗡️  Aus dem Schatten! Nächster Angriff: Krit + ignoriert DEF.")

        # Magieschild aktivieren
        elif choice == 'm':
            if not has_shield:
                print("Magieschild nicht verfuegbar!")
                input("ENTER...")
                continue
            player.shield_ready  = False
            player.shield_active = True
            clear_screen()
            print_header("Kampf-Ergebnis")
            print("🔵 Magieschild aktiviert! Der naechste Angriff wird geblockt.")

        # Target selection for single-target attacks
        elif choice in ['a', 's', 'c']:
            # Gesperrte Fähigkeiten prüfen
            if choice == 's' and not has_heavenstrike:
                print("🔒 Himmelsschlag wird bei Level 5 freigeschaltet!")
                input("ENTER...")
                continue
            if choice == 'c' and not has_cleave:
                print("🔒 Cleave wird bei Level 2 freigeschaltet!")
                input("ENTER...")
                continue
            try:
                target_index = int(input("Welchen Gegner angreifen? (Nummer): ")) - 1
                clear_screen()
                print_header("Kampf-Ergebnis")
                if 0 <= target_index < len(enemy_list) and enemy_list[target_index].is_alive():
                    target = enemy_list[target_index]
                    if choice == 'a':
                        msg, dmg = player.attack_target(target)
                        player.stats["damage_dealt"] += dmg
                        print(msg)
                    elif choice == 's':
                        print(player.heavenstrike(target))
                    elif choice == 'c':
                        print(player.cleave(target))
                else:
                    print("Ungültiges Ziel oder Gegner bereits besiegt!")
                    input("ENTER...")
                    continue
            except ValueError:
                print("Bitte gib eine gültige Zahl ein!")
                input("ENTER...")
                continue

        elif choice == 'r':
            if not has_whirlwind:
                print("🔒 Rundumschlag wird bei Level 3 freigeschaltet!")
                input("ENTER...")
                continue
            clear_screen()
            print_header("Kampf-Ergebnis")
            living_enemies = [e for e in enemy_list if e.is_alive()]
            print(player.whirlwind(living_enemies))

        elif choice == 'u':
            result = consumable_menu(player)
            if result == "":
                # Kein Zug verbraucht — zurück ohne Gegnerangriff
                continue
            clear_screen()
            print_header("Kampf-Ergebnis")
            print(result)

        elif choice == 'f':
            clear_screen()
            print("Du fliehst aus dem Kampf!")
            return "fled"

        elif choice == 'q':
            clear_screen()
            print("Du verlässt das Spiel. Auf Wiedersehen!")
            exit()

        # Bleed tick (Gegner)
        for e in enemy_list:
            if e.is_alive():
                bleed_msg = e.check_bleed()
                if bleed_msg:
                    print(bleed_msg)

        # Bleed + Gift tick (Spieler)
        player_bleed_msg = player.check_bleed()
        if player_bleed_msg:
            print(player_bleed_msg)
        player_poison_msg = player.check_poison()
        if player_poison_msg:
            print(player_poison_msg)

        # Enemy attacks + Boss-Abilities
        for e in enemy_list:
            if not player.is_alive():
                break
            if e.is_alive():
                if player.block_next:
                    player.block_next = False
                    print(f"🛡️  Schildwall blockt den Angriff von {e.name}!")
                elif player.shield_active:
                    player.shield_active = False
                    print(f"🔵 Magieschild blockt den Angriff von {e.name}!")
                else:
                    msg, dmg = e.attack_target(player)
                    player.stats["damage_taken"] += dmg
                    print(msg)
                # Boss-Fähigkeit: Rang 5, 30% Chance
                if getattr(e, "rank", 1) == 5 and hasattr(e, "boss_ability") and random.random() < 0.30:
                    print(e.boss_ability(player))

        player.regenerate()
        input("\nNächste Runde (ENTER)...")

    if not any(e.is_alive() for e in enemy_list):
        return "victory"
    return "defeat"


def collect_loot(player, enemy_group) -> list:
    all_messages = []
    for enemy in enemy_group:
        rank       = getattr(enemy, "rank", 1)
        rolls      = getattr(enemy, "loot_rolls", 1)
        loot_items = roll_loot(rank=rank, rolls=rolls)
        msgs       = apply_loot(player, loot_items)
        if msgs:
            all_messages.append(f"\n  [{enemy.name}]")
            all_messages.extend(msgs)
    return all_messages
