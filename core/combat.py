import random
from ui.utils import clear_screen, print_header
from content.loot_tables import roll_loot, apply_loot, CONSUMABLE_DEFS

_W = 58  # Anzeigebreite


def generate_enemy_group(player):
    from systems.zones import ZONE_DEFS, create_zone_enemy
    zone_id    = getattr(player, "current_zone", "wald")
    zdef       = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
    mn, mx     = zdef["group_size"]
    count      = random.randint(mn, mx)
    return [create_zone_enemy(player, zone_id) for _ in range(count)]


# ── Hilfs-Renderer ────────────────────────────────────────────────────────────

def _bar(current, maximum, width=16) -> str:
    ratio  = current / maximum if maximum > 0 else 0
    filled = int(ratio * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def _print_combat_screen(player, enemy_list, round_num: int):
    from systems.zones import ZONE_DEFS
    from content.classes import CLASS_DEFS

    clear_screen()
    zone_id = getattr(player, "current_zone", "wald")
    zdef    = ZONE_DEFS.get(zone_id, {})
    cdef    = CLASS_DEFS.get(player.player_class, {})

    print("=" * _W)
    print(f"  KAMPF  |  {zdef.get('emoji','')} {zdef.get('name','')}  |  Runde {round_num}")
    print("=" * _W)

    # Spieler-Block
    hp_bar = _bar(player.hp, player.max_hp)
    en_bar = _bar(player.energy, player.max_energy)
    print(f"  {cdef.get('emoji','🧙')} {player.name:<12} LVL {player.level}  "
          f"XP {player.xp}/{player.xp_to_level_up}")
    print(f"    HP      {hp_bar} {player.hp}/{player.max_hp}")
    print(f"    Energie {en_bar} {player.energy}/{player.max_energy}")

    # Status-Effekte (kompakt, eine Zeile)
    fx = []
    if player.bleed_stacks > 0:                       fx.append(f"⚠ Blutung×{player.bleed_stacks}")
    if player.poison_stacks > 0:                      fx.append(f"☠ Gift×{player.poison_stacks}")
    if player.armor_debuff > 0:                       fx.append(f"🟢 Säure-{player.armor_debuff}")
    if player.stunned:                                 fx.append("🪨 BETÄUBT")
    if getattr(player, "block_next", False):          fx.append(f"🛡 Block×{player.block_charges}")
    if getattr(player, "shield_active", False):       fx.append("🔵 Magieschild")
    if getattr(player, "mana_shield_active", False):  fx.append("🔮 Mana-Schild")
    if fx:
        print(f"    {' | '.join(fx)}")

    # Kurzinventar
    cons = sum(v for v in player.inventory.get("Consumables", {}).values())
    gold = player.inventory.get("Gold", 0)
    print(f"    💰 {gold} Gold  |  💊 {cons} Items")

    # Gegner-Block
    print(f"\n  {'-' * (_W - 2)}")
    for i, e in enumerate(enemy_list):
        if e.is_alive():
            bar    = _bar(e.hp, e.max_hp)
            rank   = f"R{e.rank}" if hasattr(e, "rank") else ""
            e_fx   = []
            if getattr(e, "bleed_stacks", 0) > 0: e_fx.append(f"Blutung{e.bleed_stacks}")
            if getattr(e, "stunned", False):        e_fx.append("BETAUBT")
            fx_str = "  " + " ".join(e_fx) if e_fx else ""
            print(f"  [{i+1}] {e.name:<18} {rank:<4} {bar}  {e.hp}/{e.max_hp}{fx_str}")
        else:
            print(f"  [{i+1}] {e.name:<18}  {'x besiegt':>32}")
    print(f"  {'-' * (_W - 2)}")


def _print_action_menu(player):
    from content.classes import CLASS_DEFS

    total_red = player._energy_cost_reduction()
    cost_s    = max(5, 20 - total_red)
    cost_r    = max(5, 15 - total_red)
    cost_c    = max(5, 10 - total_red)

    pclass    = player.player_class
    cdef      = CLASS_DEFS.get(pclass, {})
    a_used    = player.class_ability_used
    a2_used   = getattr(player, "class_ability2_used", False)
    a3_used   = getattr(player, "class_ability3_used", False)
    a2_unlock = player.level >= 4
    a3_unlock = player.level >= 7

    _A2 = {"warrior": f"[1] Schildstoß    15E",
           "rogue":   f"[1] Giftklinge    12E",
           "mage":    f"[1] Froststrahl   18E"}
    _A3 = {"warrior": f"[2] Kriegsschrei  20E",
           "rogue":   f"[2] Rauchbombe    10E",
           "mage":    f"[2] Mana-Schild"}

    left, right = [], []

    # Linke Spalte: Basis + Fähigkeit 3
    left.append("[A] Angriff")
    if player.level >= 3: left.append(f"[R] Rundumschlag  {cost_r}E")
    x_cost = " 15E" if pclass == "mage" else ""
    if not a_used:         left.append(f"[X] {cdef.get('ability_name','?')}{x_cost}")
    if a3_unlock and not a3_used: left.append(_A3.get(pclass, "[2] ?"))
    left.append("[U] Items")

    # Rechte Spalte: Spezial + Utility
    if player.level >= 5: right.append(f"[S] Himmelsschlag {cost_s}E")
    if player.level >= 2: right.append(f"[C] Cleave         {cost_c}E")
    if a2_unlock and not a2_used: right.append(_A2.get(pclass, "[1] ?"))
    if player.shield_ready: right.append("[M] Magieschild")
    right.append("[F] Fliehen  |  [Q] Ende")

    # Gesperrte Fähigkeiten (einzeilige Notiz)
    locked = []
    if player.level < 2: locked.append("Cleave ab LVL 2")
    if player.level < 3: locked.append("Rundumschlag ab LVL 3")
    if player.level < 5: locked.append("Himmelsschlag ab LVL 5")
    if not a2_unlock:    locked.append(f"{_A2.get(pclass,'').split(']',1)[-1].strip().split()[0]} ab LVL 4")
    if not a3_unlock:    locked.append(f"{_A3.get(pclass,'').split(']',1)[-1].strip().split()[0]} ab LVL 7")

    rows = max(len(left), len(right))
    for i in range(rows):
        l = left[i]  if i < len(left)  else ""
        r = right[i] if i < len(right) else ""
        print(f"  {l:<27}{r}")

    if locked:
        print(f"  🔒 {' / '.join(locked)}")

    print("-" * _W)


def _pick_target(enemy_list) -> int:
    """Gibt 0-basierten Index zurück. Auto-Target wenn nur 1 Gegner lebt. -1 bei Fehler."""
    alive = [(i, e) for i, e in enumerate(enemy_list) if e.is_alive()]
    if len(alive) == 1:
        return alive[0][0]
    try:
        tidx = int(input("  Welchen Gegner? (Nummer): ")) - 1
        if 0 <= tidx < len(enemy_list) and enemy_list[tidx].is_alive():
            return tidx
        print("  Ungültiges Ziel!")
        input("  ENTER...")
        return -1
    except ValueError:
        print("  Bitte eine gültige Zahl eingeben!")
        input("  ENTER...")
        return -1


def _result_header(player, enemy_list):
    """Kompakter HP-Block am Anfang des Ergebnis-Screens."""
    clear_screen()
    print("-" * _W)
    hp_bar = _bar(player.hp, player.max_hp, width=12)
    en_bar = _bar(player.energy, player.max_energy, width=8)
    print(f"  HP {hp_bar} {player.hp}/{player.max_hp}   "
          f"Energie {en_bar} {player.energy}/{player.max_energy}")
    alive = [e for e in enemy_list if e.is_alive()]
    if alive:
        parts = [f"{e.name}: {_bar(e.hp, e.max_hp, width=8)} {e.hp}/{e.max_hp}"
                 for e in alive]
        print(f"  {' | '.join(parts)}")
    print("-" * _W)


# ── Konsumable-Menü ───────────────────────────────────────────────────────────

def consumable_menu(player) -> str:
    clear_screen()
    print_header("Verbrauchsgegenstände")

    consumables = player.inventory.get("Consumables", {})
    available   = {k: v for k, v in consumables.items() if v > 0}

    if not available:
        return "Keine Verbrauchsgegenstände vorhanden!"

    items_list = list(available.items())
    hp_bar = _bar(player.hp, player.max_hp, width=12)
    print(f"  HP {hp_bar} {player.hp}/{player.max_hp}  "
          f"|  Energie: {player.energy}/{player.max_energy}")
    if player.bleed_stacks > 0:
        print(f"  ⚠️  Blutung: {player.bleed_stacks} Stacks")
    if player.poison_stacks > 0:
        print(f"  ☠️  Gift: {player.poison_stacks} Stacks")
    print("-" * 42)

    for i, (key, count) in enumerate(items_list):
        cdef  = CONSUMABLE_DEFS.get(key, {})
        emoji = cdef.get("emoji", "🧪")
        desc  = cdef.get("desc", "")
        print(f"  [{i+1}] {emoji} {key:<22} ×{count}  — {desc}")

    print(f"\n  [0] Zurück (kein Zug verbraucht)")
    choice = input("\n  Welches Item benutzen? ").strip()

    if choice == "0" or not choice.isdigit():
        return ""

    idx = int(choice) - 1
    if not (0 <= idx < len(items_list)):
        return "  Ungültige Auswahl."

    key = items_list[idx][0]
    return player.use_consumable(key)


# ── Hauptkampf-Schleife ───────────────────────────────────────────────────────

def combat(player, enemy_list):
    specials = player.get_set_specials()
    player.arcane_charges_remaining = 2 if "mage_double_arcane" in specials else 1

    # Einmal-ATK-Buff vom Blutigen Altar o.ä. anwenden
    if getattr(player, "next_fight_atk_mult", 1.0) != 1.0:
        bonus = int(player.get_total_attack() * (player.next_fight_atk_mult - 1.0))
        player.combat_modifiers["attack"] = player.combat_modifiers.get("attack", 0) + bonus
        player.next_fight_atk_mult = 1.0

    round_num = 0

    while player.is_alive() and any(e.is_alive() for e in enemy_list):
        round_num += 1
        _print_combat_screen(player, enemy_list, round_num)
        _print_action_menu(player)

        # Betäubung: Zug überspringen
        if player.stunned:
            player.stunned = False
            print("\n  🪨 Du bist betäubt — überspringst diese Runde!")
            input("  ENTER...")
            choice = "__stunned__"
        else:
            choice = input("\n  Deine Wahl: ").strip().lower()

        if choice == "__stunned__":
            pass

        elif choice not in ['a', 's', 'r', 'c', 'm', 'x', '1', '2', 'u', 'f', 'q']:
            print("\n  Ungültige Taste! Bitte eine der angezeigten Optionen wählen.")
            input("  ENTER...")
            continue

        # ── [X] Klassenfähigkeit 1 ────────────────────────────
        elif choice == 'x':
            if player.class_ability_used:
                print("  Klassenfähigkeit bereits benutzt!")
                input("  ENTER...")
                continue
            from content.classes import CLASS_DEFS
            pclass = player.player_class
            _result_header(player, enemy_list)
            print("  🌟 Klassenfähigkeit")
            print()
            if pclass == "warrior":
                has_2block = "warrior_2block" in player.get_set_specials()
                player.block_charges  = 2 if has_2block else 1
                player.block_next     = True
                player.class_ability_used = True
                extra = " (Eisenfestung: 2 Angriffe!)" if has_2block else ""
                print(f"  🛡️  Schildwall aktiviert!{extra}")
            elif pclass == "mage":
                energy_cost = 15
                if player.energy < energy_cost:
                    print(f"  Nicht genug Energie! ({player.energy}/{energy_cost})")
                    input("  ENTER...")
                    continue
                player.energy -= energy_cost
                player.arcane_charges_remaining -= 1
                if player.arcane_charges_remaining <= 0:
                    player.class_ability_used = True
                living = [e for e in enemy_list if e.is_alive()]
                dmg    = random.randint(6 + player.level * 2, 12 + player.level * 3)
                for e in living:
                    e.hp = max(0, e.hp - dmg)
                names = ", ".join(e.name for e in living)
                print(f"  ✨ Arkane Entladung! {dmg} Schaden (ignoriert DEF) an: {names}")
                player.stats["damage_dealt"] += dmg * len(living)
                if player.arcane_charges_remaining > 0:
                    print(f"     (Arkane Roben: {player.arcane_charges_remaining} Ladung verbleibend)")
            elif pclass == "rogue":
                player.shadow_strike_ready = True
                player.class_ability_used  = True
                has_regen = "rogue_shadow_regen" in player.get_set_specials()
                if has_regen:
                    player.shadow_recharge_countdown = 3
                    print("  🗡️  Aus dem Schatten! Nächster Angriff: Krit + ignoriert DEF. (Lädt in 3 Runden neu)")
                else:
                    print("  🗡️  Aus dem Schatten! Nächster Angriff: Krit + ignoriert DEF.")

        # ── [1] Klassenfähigkeit 2 (LVL 4) ───────────────────
        elif choice == '1':
            if player.level < 4:
                print("  🔒 Fähigkeit wird bei Level 4 freigeschaltet!")
                input("  ENTER...")
                continue
            if getattr(player, "class_ability2_used", False):
                print("  Fähigkeit bereits benutzt!")
                input("  ENTER...")
                continue
            tidx = _pick_target(enemy_list)
            if tidx < 0:
                continue
            target = enemy_list[tidx]
            player.class_ability2_used = True
            _result_header(player, enemy_list)
            print("  🌟 Klassen-Fähigkeit 2")
            print()
            pclass = player.player_class
            if pclass == "warrior":
                msg, dmg = player.shield_bash(target)
            elif pclass == "rogue":
                msg, dmg = player.poison_blade(target)
            else:
                msg, dmg = player.frost_ray(target)
            print(f"  {msg}")
            player.stats["damage_dealt"] += dmg

        # ── [2] Klassenfähigkeit 3 (LVL 7) ───────────────────
        elif choice == '2':
            if player.level < 7:
                print("  🔒 Fähigkeit wird bei Level 7 freigeschaltet!")
                input("  ENTER...")
                continue
            if getattr(player, "class_ability3_used", False):
                print("  Fähigkeit bereits benutzt!")
                input("  ENTER...")
                continue
            player.class_ability3_used = True
            _result_header(player, enemy_list)
            print("  🌟 Klassen-Fähigkeit 3")
            print()
            pclass = player.player_class
            if pclass == "warrior":
                print(f"  {player.warcry()}")
            elif pclass == "rogue":
                if player.energy >= 10:
                    player.energy -= 10
                    print("  💨 Rauchbombe! Du verschwindest im Rauch...")
                    input("  ENTER...")
                    return "fled"
                else:
                    player.class_ability3_used = False
                    print(f"  Nicht genug Energie! ({player.energy}/10)")
                    input("  ENTER...")
                    continue
            else:
                print(f"  {player.activate_mana_shield()}")

        # ── [M] Magieschild ───────────────────────────────────
        elif choice == 'm':
            if not player.shield_ready:
                print("  Magieschild nicht verfügbar!")
                input("  ENTER...")
                continue
            player.shield_ready  = False
            player.shield_active = True
            _result_header(player, enemy_list)
            print("  🔵 Magieschild aktiviert! Der nächste Angriff wird geblockt.")

        # ── [A/S/C] Einzelziel-Angriffe ───────────────────────
        elif choice in ['a', 's', 'c']:
            if choice == 's' and player.level < 5:
                print("  🔒 Himmelsschlag wird bei Level 5 freigeschaltet!")
                input("  ENTER...")
                continue
            if choice == 'c' and player.level < 2:
                print("  🔒 Cleave wird bei Level 2 freigeschaltet!")
                input("  ENTER...")
                continue
            tidx = _pick_target(enemy_list)
            if tidx < 0:
                continue
            target = enemy_list[tidx]
            _result_header(player, enemy_list)
            if choice == 'a':
                print("  ⚔  Angriff")
            elif choice == 's':
                print("  ✨ Himmelsschlag")
            else:
                print("  🌀 Cleave")
            print()
            if choice == 'a':
                msg, dmg = player.attack_target(target)
                player.stats["damage_dealt"] += dmg
                print(f"  {msg}")
            elif choice == 's':
                print(f"  {player.heavenstrike(target)}")
            else:
                print(f"  {player.cleave(target)}")

        # ── [R] Rundumschlag ──────────────────────────────────
        elif choice == 'r':
            if player.level < 3:
                print("  🔒 Rundumschlag wird bei Level 3 freigeschaltet!")
                input("  ENTER...")
                continue
            living = [e for e in enemy_list if e.is_alive()]
            _result_header(player, enemy_list)
            print("  🌪  Rundumschlag")
            print()
            print(f"  {player.whirlwind(living)}")

        # ── [U] Verbrauchsgegenstände ─────────────────────────
        elif choice == 'u':
            result = consumable_menu(player)
            if result == "":
                continue  # Kein Zug verbraucht
            _result_header(player, enemy_list)
            print("  🧪 Verbrauchsgegenstand")
            print()
            print(f"  {result}")

        # ── [F] Fliehen ───────────────────────────────────────
        elif choice == 'f':
            clear_screen()
            print("  Du fliehst aus dem Kampf!")
            return "fled"

        # ── [Q] Beenden ───────────────────────────────────────
        elif choice == 'q':
            clear_screen()
            print("  Du verlässt das Spiel. Auf Wiedersehen!")
            exit()

        # ── Blutungs-Tick (Gegner) ────────────────────────────
        for e in enemy_list:
            if e.is_alive():
                bleed_msg = e.check_bleed()
                if bleed_msg:
                    print(f"  {bleed_msg}")

        # ── Blutungs- & Gift-Tick (Spieler) ──────────────────
        player_bleed = player.check_bleed()
        if player_bleed:
            print(f"  {player_bleed}")
        player_poison = player.check_poison()
        if player_poison:
            print(f"  {player_poison}")

        # ── Gegner-Angriffe ───────────────────────────────────
        print()
        for e in enemy_list:
            if not player.is_alive():
                break
            if not e.is_alive():
                continue
            if getattr(e, "stunned", False):
                e.stunned = False
                print(f"  🪨 {e.name} ist betäubt und überspringt diese Runde!")
                continue
            if getattr(player, "block_next", False):
                player.block_charges -= 1
                if player.block_charges <= 0:
                    player.block_next = False
                rem = f" ({player.block_charges} verbleibend)" if player.block_charges > 0 else ""
                print(f"  🛡️  Schildwall blockt {e.name}s Angriff!{rem}")
            elif player.shield_active:
                player.shield_active = False
                print(f"  🔵 Magieschild blockt den Angriff von {e.name}!")
            elif getattr(player, "mana_shield_active", False):
                player.mana_shield_active = False
                raw      = random.randint(max(1, getattr(e, "min_attack", 1)), e.attack)
                dmg      = player.apply_armor_reduction(raw, player.get_total_armor())
                absorbed = min(dmg, player.energy)
                player.energy = max(0, player.energy - absorbed)
                leftover = max(0, dmg - absorbed)
                if leftover:
                    player.hp = max(0, player.hp - leftover)
                    player.stats["damage_taken"] += leftover
                    print(f"  🔮 Mana-Schild absorbiert {absorbed} Energie — "
                          f"{leftover} Restschaden! (HP: {player.hp}/{player.max_hp})")
                else:
                    print(f"  🔮 Mana-Schild absorbiert {dmg} Schaden vollständig! "
                          f"(Energie: {player.energy}/{player.max_energy})")
            else:
                msg, dmg = e.attack_target(player)
                player.stats["damage_taken"] += dmg
                print(f"  {msg}")
            ability_chance = getattr(e, "boss_ability_chance", 0.30)
            if getattr(e, "rank", 1) == 5 and hasattr(e, "boss_ability") and random.random() < ability_chance:
                print(f"  {e.boss_ability(player)}")

        player.regenerate()

        # Aus-dem-Schatten Auflade-Countdown (Schurke)
        if player.player_class == "rogue" and getattr(player, "shadow_recharge_countdown", 0) > 0:
            player.shadow_recharge_countdown -= 1
            if player.shadow_recharge_countdown == 0:
                player.class_ability_used = False
                print("\n  🌙 Schattenhülle: Aus dem Schatten ist wieder aufgeladen! [X]")

        # Finaler HP-Stand am Ende jeder Runde
        print()
        hp_bar = _bar(player.hp, player.max_hp, width=12)
        print(f"  HP {hp_bar} {player.hp}/{player.max_hp}")

        input("\n  Nächste Runde (ENTER)...")

    if not any(e.is_alive() for e in enemy_list):
        return "victory"
    return "defeat"


# ── Beute-Sammlung ────────────────────────────────────────────────────────────

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
