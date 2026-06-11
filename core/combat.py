import random
from ui.utils import clear_screen, print_header, console, hp_bar, energy_bar
from rich.markup import escape as _esc
from rich.table import Table
from content.loot_tables import roll_loot, roll_zone_loot, apply_loot, CONSUMABLE_DEFS, EQUIPMENT_DEFS
from core.abilities import (
    brutaler_hieb, schildwall, schildstoss, kriegsschrei,
    aus_dem_schatten, giftklinge, blendpulver, rauchbombe,
    arkane_entladung, froststrahl, feuerball, mana_schild_aktivieren,
)
from systems.segnungen import (
    on_combat_start, on_kill, on_player_hit, status_snapshot,
    check_vergeltung, check_zweite_chance, check_glut_burst,
)
from systems.spiegel import spiegel_active, check_spiegel_leben, check_dunkelresistenz


# Waffen-Passive leben nur hier — nicht in player.attack_target().
def _apply_weapon_passive(player, target, dmg: int):
    if dmg <= 0:
        return
    passive = EQUIPMENT_DEFS.get(player.equipment["weapon"]["name"], {}).get("passive")
    if not passive:
        return
    immune = getattr(target, "immune_to_bleed_poison", False)
    if passive == "poison_on_hit" and not immune:
        target.poison_stacks = getattr(target, "poison_stacks", 0) + 1
        console.print(f"  [magenta]☠️  Giftklaue: +1 Giftstack auf {_esc(target.name)}![/magenta]")
    elif passive == "burn_on_hit" and not immune and random.random() < 0.25:
        target.burn_stacks = getattr(target, "burn_stacks", 0) + 2
        console.print(f"  [orange1]🔥 Flammenklinge: 2 Verbrennungsstacks auf {_esc(target.name)}![/orange1]")
    elif passive == "freeze_on_hit" and random.random() < 0.20:
        target.stunned = True
        console.print(f"  [cyan]❄️  Eisaxt: {_esc(target.name)} ist eingefroren![/cyan]")
    elif passive == "def_debuff_on_hit" and random.random() < 0.30:
        target.armor_debuff = getattr(target, "armor_debuff", 0) + 3
        console.print(f"  [yellow]🔨 Runen-Kriegshammer: {_esc(target.name)} −3 DEF![/yellow]")


def _check_swallow(target) -> bool:
    sc = getattr(target, "swallow_chance", 0)
    return sc > 0 and random.random() < sc

_W = 58  # Anzeigebreite


def generate_enemy_group(player):
    from systems.zones import ZONE_DEFS, create_zone_enemy
    zone_id    = getattr(player, "current_zone", "wald")
    zdef       = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
    mn, mx     = zdef["group_size"]
    count      = random.randint(mn, mx)
    return [create_zone_enemy(player, zone_id) for _ in range(count)]


def _print_combat_screen(player, enemy_list, round_num: int):
    from systems.zones import ZONE_DEFS
    from content.classes import CLASS_DEFS

    clear_screen()
    zone_id = getattr(player, "current_zone", "wald")
    zdef    = ZONE_DEFS.get(zone_id, {})
    cdef    = CLASS_DEFS.get(player.player_class, {})

    console.print(f"[bold]{'=' * _W}[/bold]")
    console.print(f"  [bold]KAMPF[/bold]  |  {_esc(zdef.get('emoji',''))} {_esc(zdef.get('name',''))}  |  Runde {round_num}")
    console.print(f"[bold]{'=' * _W}[/bold]")

    # Spieler-Block
    hp_b = hp_bar(player.hp, player.max_hp)
    en_b = energy_bar(player.energy, player.max_energy)
    console.print(f"  {_esc(cdef.get('emoji','🧙'))} [bold]{_esc(player.name):<12}[/bold] LVL {player.level}  XP {player.xp}/{player.xp_to_level_up}")
    console.print(f"    HP      {hp_b} {player.hp}/{player.max_hp}")
    console.print(f"    Energie {en_b} {player.energy}/{player.max_energy}")

    # Status-Effekte (kompakt, eine Zeile)
    fx = []
    if player.bleed_stacks > 0:                       fx.append(f"[red]⚠ Blutung×{player.bleed_stacks}[/red]")
    if player.poison_stacks > 0:                      fx.append(f"[purple]☠ Gift×{player.poison_stacks}[/purple]")
    if getattr(player, "burn_stacks", 0) > 0:         fx.append(f"[orange1]🔥 Verbr×{player.burn_stacks}[/orange1]")
    if player.armor_debuff > 0:                       fx.append(f"[orange1]🟠 Säure-DEF−{player.armor_debuff}[/orange1]")
    if player.stunned:                                 fx.append("[bold yellow]🪨 BETÄUBT[/bold yellow]")
    if getattr(player, "block_next", False):          fx.append(f"[cyan]🛡 Block×{player.block_charges}[/cyan]")
    if getattr(player, "shield_active", False):       fx.append("[cyan]🔵 Magieschild[/cyan]")
    if getattr(player, "mana_shield_active", False):  fx.append("[blue]🔮 Mana-Schild[/blue]")
    if getattr(player, "shadow_strike_ready", False): fx.append("[magenta]🗡️ Schatten-Krit[/magenta]")
    if getattr(player, "seg_raserei_ready", False):   fx.append("[bold red]🔥 RASEREI bereit[/bold red]")
    if fx:
        console.print(f"    {' | '.join(fx)}")

    # Kurzinventar
    cons = sum(v for v in player.inventory.get("Consumables", {}).values())
    gold = player.inventory.get("Gold", 0)
    console.print(f"    💰 {gold} Gold  |  💊 {cons} Items")

    # Gegner-Block
    console.print(f"\n  {'-' * (_W - 2)}")
    for i, e in enumerate(enemy_list):
        if e.is_alive():
            e_hp_b = hp_bar(e.hp, e.max_hp)
            rank   = f"R{e.rank}" if hasattr(e, "rank") else ""
            e_fx   = []
            if getattr(e, "bleed_stacks", 0) > 0:  e_fx.append(f"[red]Blutung×{e.bleed_stacks}[/red]")
            if getattr(e, "burn_stacks",  0) > 0:   e_fx.append(f"[orange1]🔥Verbr.×{e.burn_stacks}[/orange1]")
            if getattr(e, "stunned", False):         e_fx.append("[yellow]BETÄUBT[/yellow]")
            if getattr(e, "blind_turns", 0) > 0:    e_fx.append(f"[cyan]💨Blind×{getattr(e,'blind_turns',0)}[/cyan]")
            fx_str = "  " + " ".join(e_fx) if e_fx else ""
            console.print(f"  [[{i+1}]] {_esc(e.name):<18} {rank:<4} {e_hp_b}  {e.hp}/{e.max_hp}{fx_str}")
        else:
            console.print(f"  [[{i+1}]] {_esc(e.name):<18}  [dim]✗ besiegt[/dim]")
    console.print(f"  {'-' * (_W - 2)}")


def _print_action_menu(player):
    from content.classes import CLASS_ABILITY_DEFS

    pclass = player.player_class
    adefs  = CLASS_ABILITY_DEFS.get(pclass, {})
    cds    = getattr(player, "ability_cooldowns", {"S": 0, "R": 0, "C": 0, "X": 0})
    red    = player._energy_cost_reduction()

    def _ab(key) -> str:
        d       = adefs.get(key, {})
        name    = d.get("name", "?")
        e_base  = d.get("energy", 0)
        cd_max  = d.get("cd", 0)
        unlock  = d.get("unlock", 1)
        cur_cd  = cds.get(key, 0)
        if player.level < unlock:
            return f"[dim][[{key}]] {_esc(name)}  🔒LV{unlock}[/dim]"
        cost  = max(0, e_base - red) if e_base > 0 else 0
        e_str = f"{cost}E" if cost > 0 else " —"
        if cd_max == 99 and cur_cd:
            return f"[red][[{key}]] {_esc(name)}  {e_str} ✗1×/K[/red]"
        elif cur_cd > 0:
            return f"[yellow][[{key}]] {_esc(name)}  {e_str} ⏳{cur_cd}Rd[/yellow]"
        return f"[[{key}]] {_esc(name)}  {e_str}"

    a_str = ("[[A]] Angriff  [magenta bold]🗡️ Krit bereit![/magenta bold]"
             if player.shadow_strike_ready else "[[A]] Angriff")

    t = Table(box=None, padding=(0, 2, 0, 0), show_header=False, expand=False)
    t.add_column(min_width=32, no_wrap=True)
    t.add_column()
    t.add_row(a_str, _ab("S"))
    t.add_row(_ab("R"), _ab("C"))
    t.add_row(_ab("X"), "[[U]] Items")
    console.print(t)

    if player.shield_ready:
        console.print("  [[M]] Magieschild")
    console.print("  [[F]] Fliehen    [[Q]] Beenden    [[?]] Hilfe")
    console.print("─" * _W)


def _pick_target(enemy_list) -> int:
    """Gibt 0-basierten Index zurück. Auto-Target wenn nur 1 Gegner lebt. -1 bei Fehler."""
    alive = [(i, e) for i, e in enumerate(enemy_list) if e.is_alive()]
    if len(alive) == 1:
        return alive[0][0]
    try:
        tidx = int(input("  Welchen Gegner? (Nummer): ")) - 1
        if 0 <= tidx < len(enemy_list) and enemy_list[tidx].is_alive():
            return tidx
        console.print("  [red]Ungültiges Ziel![/red]")
        input("  ENTER...")
        return -1
    except ValueError:
        console.print("  [red]Bitte eine gültige Zahl eingeben![/red]")
        input("  ENTER...")
        return -1


def _result_header(player, enemy_list):
    """Kompakter HP-Block am Anfang des Ergebnis-Screens."""
    clear_screen()
    console.print("─" * _W)
    hp_b = hp_bar(player.hp, player.max_hp, width=12)
    en_b = energy_bar(player.energy, player.max_energy, width=8)
    console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}   Energie {en_b} {player.energy}/{player.max_energy}")
    alive = [e for e in enemy_list if e.is_alive()]
    if alive:
        parts = [f"{_esc(e.name)}: {hp_bar(e.hp, e.max_hp, width=8)} {e.hp}/{e.max_hp}"
                 for e in alive]
        console.print(f"  {' | '.join(parts)}")
    console.print("─" * _W)


# ── Konsumable-Menü ───────────────────────────────────────────────────────────

def consumable_menu(player) -> str:
    clear_screen()
    print_header("Verbrauchsgegenstände")

    consumables = player.inventory.get("Consumables", {})
    available   = {k: v for k, v in consumables.items() if v > 0}

    if not available:
        return "Keine Verbrauchsgegenstände vorhanden!"

    items_list = list(available.items())
    hp_b = hp_bar(player.hp, player.max_hp, width=12)
    en_b = energy_bar(player.energy, player.max_energy, width=8)
    console.print(f"  HP {hp_b} {player.hp}/{player.max_hp}   Energie {en_b} {player.energy}/{player.max_energy}")
    if player.bleed_stacks > 0:
        console.print(f"  [red]⚠️  Blutung: {player.bleed_stacks} Stacks[/red]")
    if player.poison_stacks > 0:
        console.print(f"  [magenta]☠️  Gift: {player.poison_stacks} Stacks[/magenta]")
    if getattr(player, "burn_stacks", 0) > 0:
        console.print(f"  [orange1]🔥 Verbrennung: {player.burn_stacks} Stacks[/orange1]")
    console.print("─" * 42)

    for i, (key, count) in enumerate(items_list):
        cdef  = CONSUMABLE_DEFS.get(key, {})
        emoji = cdef.get("emoji", "🧪")
        desc  = cdef.get("desc", "")
        console.print(f"  [[{i+1}]] {_esc(emoji)} {_esc(key):<22} ×{count}  — [dim]{_esc(desc)}[/dim]")

    console.print(f"\n  [[0]] Zurück (kein Zug verbraucht)")
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
    # Einmal-ATK-Buff vom Blutigen Altar o.ä. anwenden
    if getattr(player, "next_fight_atk_mult", 1.0) != 1.0:
        bonus = int(player.get_total_attack() * (player.next_fight_atk_mult - 1.0))
        player.combat_modifiers["attack"] = player.combat_modifiers.get("attack", 0) + bonus
        player.next_fight_atk_mult = 1.0

    seg_start_msgs = on_combat_start(player, enemy_list) if player.active_segnungen else []

    if getattr(player, "spiegel_first_fight", False) and spiegel_active(player, "kriegserfahrung", "B"):
        player.spiegel_first_fight = False
        bonus = max(1, int(player.get_total_attack() * 0.5))
        player.combat_modifiers["attack"] = player.combat_modifiers.get("attack", 0) + bonus
        seg_start_msgs.append(f"🪞⚔️ Kriegserfahrung: Erster Kampf des Dungeons — +{bonus} ATK (+50% Schaden)!")

    round_num = 0

    while player.is_alive() and any(e.is_alive() for e in enemy_list):
        round_num += 1
        _print_combat_screen(player, enemy_list, round_num)
        if round_num == 1 and seg_start_msgs:
            for m in seg_start_msgs:
                console.print(f"  [cyan]{m}[/cyan]")
        _print_action_menu(player)

        # Betäubung: Zug überspringen
        if player.stunned and "eiserner_wille" in player.active_segnungen and random.random() < 0.50:
            player.stunned = False
            console.print("\n  [cyan]🧠 Eiserner Wille: Du widerstehst der Betäubung![/cyan]")
        if player.stunned:
            player.stunned = False
            console.print("\n  [yellow]🪨 Du bist betäubt — überspringst diese Runde![/yellow]")
            input("  ENTER...")
            choice = "__stunned__"
        else:
            choice = input("\n  Deine Wahl: ").strip().lower()

        alive_before = [e for e in enemy_list if e.is_alive()]

        if choice == "__stunned__":
            pass

        elif choice not in ('a', 's', 'r', 'c', 'x', 'm', 'u', 'f', 'q', '?'):
            console.print("\n  [red]Ungültige Taste! Bitte eine der angezeigten Optionen wählen.[/red]")
            input("  ENTER...")
            continue

        # ── [?] Fähigkeiten-Hilfe (kein Zug verbraucht) ──────
        elif choice == '?':
            from content.classes import CLASS_DEFS, CLASS_ABILITY_DEFS
            clear_screen()
            pclass = player.player_class
            cdef   = CLASS_DEFS.get(pclass, {})
            adefs  = CLASS_ABILITY_DEFS.get(pclass, {})
            cds    = getattr(player, "ability_cooldowns", {})
            red    = player._energy_cost_reduction()
            print_header(f"{cdef.get('emoji','')} Fähigkeiten — {cdef.get('name','?')}")
            for k in ("S", "R", "C", "X"):
                d       = adefs.get(k, {})
                name    = d.get("name", "?")
                e_base  = d.get("energy", 0)
                cd_base = d.get("cd", 0)
                unlock  = d.get("unlock", 1)
                desc    = d.get("desc", "")
                cur_cd  = cds.get(k, 0)
                cost    = max(0, e_base - red) if e_base > 0 else 0
                e_str   = f"{cost}E" if cost > 0 else "—"
                cd_str  = "1×/Kampf" if cd_base == 99 else (f"{cd_base}Rd" if cd_base else "—")
                if player.level < unlock:
                    status = f"[dim]🔒 LVL {unlock}[/dim]"
                    row_c  = "dim"
                elif cd_base == 99 and cur_cd:
                    status = "[red]❌ Benutzt[/red]"
                    row_c  = "red"
                elif cur_cd > 0:
                    status = f"[yellow]⏳ {cur_cd}Rd[/yellow]"
                    row_c  = "yellow"
                else:
                    status = "[green]✅ Bereit[/green]"
                    row_c  = "cyan"
                console.print(f"  [{row_c}][[{k}]] {_esc(name)}  ({e_str}, CD:{cd_str})[/{row_c}]  {status}")
                console.print(f"  [dim]    {_esc(desc)}[/dim]")
                console.print()
            input("  ENTER...")
            continue

        # ── [S/R/C/X] Klassen-Fähigkeiten ────────────────────
        elif choice in ('s', 'r', 'c', 'x'):
            from content.classes import CLASS_ABILITY_DEFS
            key    = choice.upper()
            pclass = player.player_class
            adefs  = CLASS_ABILITY_DEFS.get(pclass, {})
            adef   = adefs.get(key, {})
            unlock = adef.get("unlock", 1)
            if player.level < unlock:
                console.print(f"  [dim]🔒 {_esc(adef.get('name', key))} wird bei Level {unlock} freigeschaltet![/dim]")
                input("  ENTER...")
                continue
            if key == "R" and pclass == "warrior" and getattr(player, "class_variant", None) == "berserker":
                console.print("  [dim]💢 Ein Berserker kennt keinen Schildwall![/dim]")
                input("  ENTER...")
                continue
            cds    = getattr(player, "ability_cooldowns", {"S":0,"R":0,"C":0,"X":0})
            cur_cd = cds.get(key, 0)
            if cur_cd > 0:
                cd_info = "1×/Kampf benutzt" if cur_cd == 99 else f"noch {cur_cd} Runden"
                console.print(f"  [yellow]⏳ {_esc(adef.get('name', key))} auf Abklingzeit! ({cd_info})[/yellow]")
                input("  ENTER...")
                continue
            # Energie-Vorprüfung
            e_base = adef.get("energy", 0)
            e_cost = max(0, e_base - player._energy_cost_reduction()) if e_base > 0 else 0
            if player.energy < e_cost:
                console.print(f"  [red]⚡ Nicht genug Energie für {_esc(adef.get('name','?'))}! ({player.energy}/{e_cost})[/red]")
                input("  ENTER...")
                continue
            # Zielauswahl (needs_target kommt aus CLASS_ABILITY_DEFS)
            needs_t = adef.get("needs_target", False)
            target  = None
            if needs_t:
                tidx = _pick_target(enemy_list)
                if tidx < 0:
                    continue
                target = enemy_list[tidx]
            _result_header(player, enemy_list)
            console.print(f"  [bold magenta]🌟 {_esc(adef.get('name', key))}[/bold magenta]")
            console.print()
            # Fähigkeit ausführen
            living = [e for e in enemy_list if e.is_alive()]
            res    = None
            if pclass == "warrior":
                if key == "S":   res = brutaler_hieb(player, target)
                elif key == "R": res = schildwall(player)
                elif key == "C": res = schildstoss(player, target)
                elif key == "X": res = kriegsschrei(player)
            elif pclass == "rogue":
                if key == "S":   res = aus_dem_schatten(player)
                elif key == "R": res = giftklinge(player, target)
                elif key == "C": res = blendpulver(player, target)
                elif key == "X": res = rauchbombe(player)
            elif pclass == "mage":
                if key == "S":   res = arkane_entladung(player, living)
                elif key == "R": res = froststrahl(player, target)
                elif key == "C": res = feuerball(player, target)
                elif key == "X": res = mana_schild_aktivieren(player)
            # Rauchbombe: garantierter Rückzug
            if res == "__FLEE__":
                console.print("  [cyan]💨 Du verschwindest im Rauch...[/cyan]")
                input("  ENTER...")
                return "fled"
            # Ergebnis ausgeben + Waffenpassiv
            _PHYS_PASSIVES = {
                "warrior": {"S", "C"},
                "rogue":   {"R"},
                "mage":    set(),
            }
            if isinstance(res, tuple):
                msg, dmg = res
                player.stats["damage_dealt"] += dmg
                console.print(f"  {msg}")
                if dmg > 0 and key in _PHYS_PASSIVES.get(pclass, set()) and target:
                    _apply_weapon_passive(player, target, dmg)
            elif res:
                console.print(f"  {res}")
            # Cooldown setzen
            cd_val = adef.get("cd", 0)
            if cd_val > 0:
                cds[key] = cd_val

        # ── [M] Magieschild ───────────────────────────────────
        elif choice == 'm':
            if not player.shield_ready:
                console.print("  [red]Magieschild nicht verfügbar![/red]")
                input("  ENTER...")
                continue
            player.shield_ready  = False
            player.shield_active = True
            _result_header(player, enemy_list)
            console.print("  [blue]🔵 Magieschild aktiviert! Der nächste Angriff wird geblockt.[/blue]")

        # ── [A] Angriff ───────────────────────────────────────
        elif choice == 'a':
            if getattr(player, "seg_raserei_ready", False):
                player.seg_raserei_ready = False
                _result_header(player, enemy_list)
                console.print("  [bold red]🔥 RASEREI — Angriff auf alle Gegner![/bold red]")
                console.print()
                for e in [x for x in enemy_list if x.is_alive()]:
                    if _check_swallow(e):
                        console.print(f"  [dim]🌪 {_esc(e.name)} verschluckt deinen Angriff![/dim]")
                        continue
                    msg, dmg = player.attack_target(e)
                    player.stats["damage_dealt"] += dmg
                    console.print(f"  [dim]{_esc(e.name)}:[/dim] {msg}")
                    _apply_weapon_passive(player, e, dmg)
            else:
                tidx = _pick_target(enemy_list)
                if tidx < 0:
                    continue
                target = enemy_list[tidx]
                _result_header(player, enemy_list)
                console.print("  [bold]⚔  Angriff[/bold]")
                console.print()
                if _check_swallow(target):
                    console.print(f"  [dim]🌪 {_esc(target.name)} verschluckt deinen Angriff![/dim]")
                else:
                    msg, dmg = player.attack_target(target)
                    player.stats["damage_dealt"] += dmg
                    console.print(f"  {msg}")
                    _apply_weapon_passive(player, target, dmg)
                    if ("finstere_klinge" in player.active_segnungen
                            and target.is_alive() and random.random() < 0.10):
                        console.print("  [magenta]🗡️  Finstere Klinge: Dein Angriff wiederholt sich![/magenta]")
                        msg2, dmg2 = player.attack_target(target)
                        player.stats["damage_dealt"] += dmg2
                        console.print(f"  {msg2}")
                        _apply_weapon_passive(player, target, dmg2)

        # ── [U] Verbrauchsgegenstände ─────────────────────────
        elif choice == 'u':
            result = consumable_menu(player)
            if result == "":
                continue
            _result_header(player, enemy_list)
            console.print("  [bold]🧪 Verbrauchsgegenstand[/bold]")
            console.print()
            console.print(f"  {result}")

        # ── [F] Fliehen ───────────────────────────────────────
        elif choice == 'f':
            if player.try_flee():
                clear_screen()
                console.print("  [green]Du fliehst erfolgreich aus dem Kampf![/green]")
                return "fled"
            _result_header(player, enemy_list)
            console.print("  [red]Flucht fehlgeschlagen! Der Feind greift an...[/red]")

        # ── [Q] Beenden ───────────────────────────────────────
        elif choice == 'q':
            clear_screen()
            console.print("  [dim]Du verlässt das Spiel. Auf Wiedersehen![/dim]")
            exit()

        # ── Status-Ticks (Gegner) ─────────────────────────────
        giftmeister = "giftmeister" in player.active_segnungen
        for e in enemy_list:
            if e.is_alive():
                burn_before = getattr(e, "burn_stacks", 0)
                tick_msgs = [m for m in (e.check_bleed(), e.check_poison(keep_stacks=giftmeister), e.check_burn()) if m]
                glut_msg  = check_glut_burst(player, e, burn_before)
                if glut_msg:
                    tick_msgs.append(glut_msg)
                if tick_msgs:
                    console.print(f"  {'  |  '.join(tick_msgs)}")

        # ── Kill-Hooks (Segnungen) ────────────────────────────
        if player.active_segnungen:
            for e in alive_before:
                if not e.is_alive():
                    for m in on_kill(player, e):
                        console.print(f"  {m}")

        # ── Status-Ticks (Spieler) ────────────────────────────
        player_ticks = [m for m in (player.check_bleed(), player.check_poison(), player.check_burn()) if m]
        if player_ticks:
            console.print(f"  {'  |  '.join(player_ticks)}")
        zc = check_zweite_chance(player)
        if zc:
            console.print(f"  {zc}")
        sl = check_spiegel_leben(player)
        if sl:
            console.print(f"  {sl}")

        # ── Gegner-Angriffe ───────────────────────────────────
        console.print()
        for e in enemy_list:
            if not player.is_alive():
                break
            if not e.is_alive():
                continue
            if getattr(e, "stunned", False):
                e.stunned = False
                console.print(f"  🪨 [yellow]{_esc(e.name)} ist betäubt und überspringt diese Runde![/yellow]")
                continue
            elif getattr(e, "blind_turns", 0) > 0:
                e.blind_turns -= 1
                rem = f"({e.blind_turns} verbleibend)" if e.blind_turns > 0 else "(Blindheit beendet)"
                console.print(f"  💨 [cyan]{_esc(e.name)} ist geblendet — verfehlt den Angriff! {rem}[/cyan]")
                continue
            if round_num == 1 and "schattenform" in player.active_segnungen:
                console.print(f"  🌑 [green]Schattenform: Du weichst dem Angriff von {_esc(e.name)} aus![/green]")
                continue
            track_status  = player.active_segnungen or spiegel_active(player, "dunkelresistenz", "A")
            before_status = status_snapshot(player) if track_status else None
            if getattr(player, "block_next", False):
                player.block_charges -= 1
                if player.block_charges <= 0:
                    player.block_next = False
                rem = f" ({player.block_charges} verbleibend)" if player.block_charges > 0 else ""
                console.print(f"  🛡️  [bold]Schildwall blockt {_esc(e.name)}s Angriff![/bold]{rem}")
            elif player.shield_active:
                player.shield_active = False
                console.print(f"  🔵 [bold]Magieschild blockt den Angriff von {_esc(e.name)}![/bold]")
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
                    console.print(f"  🔮 [blue]Mana-Schild absorbiert [cyan]{absorbed}[/cyan] Energie — "
                                  f"[red]{leftover}[/red] Restschaden! (HP: {player.hp}/{player.max_hp})[/blue]")
                else:
                    console.print(f"  🔮 [blue]Mana-Schild absorbiert [cyan]{dmg}[/cyan] Schaden vollständig! "
                                  f"(Energie: {player.energy}/{player.max_energy})[/blue]")
            else:
                dodge = player.dodge_chance
                if dodge > 0 and random.random() < dodge:
                    console.print(f"  💨 [green]Du weichst dem Angriff von {_esc(e.name)} aus![/green]")
                else:
                    specials   = player.get_set_specials()
                    block_roll = (0.15 if "drachen_block" in specials else 0) + (0.20 if "schuppen_block" in specials else 0)
                    if block_roll > 0 and random.random() < block_roll:
                        console.print(f"  🐉 [bold]Drachenschuppen blockt {_esc(e.name)}s Angriff vollständig![/bold]")
                    else:
                        msg, dmg = e.attack_target(player)
                        player.stats["damage_taken"] += dmg
                        console.print(f"  {msg}")
                        if player.active_segnungen:
                            for m in on_player_hit(player, e, dmg):
                                console.print(f"  {m}")
            ability_chance = getattr(e, "boss_ability_chance", 0.30)
            if getattr(e, "rank", 1) == 5 and hasattr(e, "boss_ability") and random.random() < ability_chance:
                console.print(f"  {e.boss_ability(player)}")
            if player.active_segnungen:
                for m in check_vergeltung(player, e, before_status):
                    console.print(f"  {m}")
                zc = check_zweite_chance(player)
                if zc:
                    console.print(f"  {zc}")
            for m in check_dunkelresistenz(player, before_status):
                console.print(f"  {m}")
            sl = check_spiegel_leben(player)
            if sl:
                console.print(f"  {sl}")

        # ── Cooldowns dekrementieren ──────────────────────────
        cds = getattr(player, "ability_cooldowns", {})
        for k in list(cds):
            if 0 < cds[k] < 99:
                cds[k] -= 1
                if cds[k] == 0:
                    from content.classes import CLASS_ABILITY_DEFS
                    aname = CLASS_ABILITY_DEFS.get(player.player_class, {}).get(k, {}).get("name", k)
                    console.print(f"  [green]✅ {_esc(aname)} ist wieder bereit! [[{k}]][/green]")

        player.regenerate()

        if (not any(e.is_alive() for e in enemy_list) and player.is_alive()
                and spiegel_active(player, "zaehigkeit", "B") and player.hp < player.max_hp):
            healed = min(5, player.max_hp - player.hp)
            player.hp += healed
            console.print(f"  [green]🪞❤️ Zähigkeit: +{healed} HP nach dem Kampf[/green]")

        # Finaler HP-Stand am Ende jeder Runde
        console.print()
        hp_b = hp_bar(player.hp, player.max_hp, width=12)
        en_b = energy_bar(player.energy, player.max_energy, width=10)
        console.print(f"  HP {hp_b} [white]{player.hp}/{player.max_hp}[/white]  "
                      f"EN {en_b} [white]{player.energy}/{player.max_energy}[/white]")

        input("\n  Nächste Runde (ENTER)...")

    if not player.is_alive():
        return "defeat"
    return "victory"


# ── Beute-Sammlung ────────────────────────────────────────────────────────────

def collect_loot(player, enemy_group) -> list:
    zone_id      = getattr(player, "current_zone", "wald")
    all_messages = []
    for enemy in enemy_group:
        rolls      = getattr(enemy, "loot_rolls", 1)
        loot_items = roll_zone_loot(zone_id, rolls=rolls)
        msgs       = apply_loot(player, loot_items)
        if msgs:
            all_messages.append(f"\n  [dim]{_esc(enemy.name)}[/dim]")
            all_messages.extend(msgs)
    return all_messages
