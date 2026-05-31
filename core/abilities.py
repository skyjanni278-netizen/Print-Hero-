import random

# Alle 12 Klassen-Fähigkeiten als Standalone-Funktionen.
# Werden von core/combat.py aufgerufen — kein direkter Zugriff auf Character nötig.
# Zukünftige Segnung-Hooks (v3.0) werden hier eingehängt.


def _cost(player, base: int) -> int:
    return max(5, base - player._energy_cost_reduction())


# ── KRIEGER ──────────────────────────────────────────────────────────────────

def brutaler_hieb(player, target) -> tuple:
    cost = _cost(player, 18)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    raw = random.randint(player.get_effective_min_attack(), player.get_total_attack()) + 6
    dmg = player.apply_armor_reduction(raw, int(target.get_total_armor() * 0.70))
    target.hp = max(0, target.hp - dmg)
    return f"⚔️  Brutaler Hieb! {dmg} Schaden (30% Rüstung ignoriert).", dmg


def schildwall(player) -> str:
    cost = _cost(player, 10)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})"
    player.energy -= cost
    has_2block = "warrior_2block" in player.get_set_specials()
    player.block_charges = 2 if has_2block else 1
    player.block_next    = True
    extra = " (Eisenfestung: 2 Angriffe!)" if has_2block else ""
    return f"🛡️  Schildwall aktiviert!{extra}"


def schildstoss(player, target) -> tuple:
    cost = _cost(player, 20)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    raw = random.randint(player.get_effective_min_attack(), player.get_total_attack())
    dmg = player.apply_armor_reduction(raw, target.get_total_armor())
    target.hp = max(0, target.hp - dmg)
    if random.random() < 0.50:
        target.stunned = True
        return f"🛡️  Schildstoß! {dmg} Schaden — {target.name} ist betäubt!", dmg
    return f"🛡️  Schildstoß! {dmg} Schaden.", dmg


def kriegsschrei(player) -> str:
    cost = _cost(player, 25)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})"
    player.energy -= cost
    player.combat_modifiers["attack"] = player.combat_modifiers.get("attack", 0) + 5
    return f"⚔️  Kriegsschrei! +5 ATK für diesen Kampf. (ATK: {player.get_total_attack()})"


# ── SCHURKE ──────────────────────────────────────────────────────────────────

def aus_dem_schatten(player) -> str:
    cost = _cost(player, 15)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})"
    player.energy -= cost
    player.shadow_strike_ready = True
    has_regen = "rogue_shadow_regen" in player.get_set_specials()
    suffix = " (Schatten-Robe: +15% Krit aktiv)" if has_regen else ""
    return f"🗡️  Aus dem Schatten! Nächster Angriff: Krit + ignoriert DEF.{suffix}"


def giftklinge(player, target) -> tuple:
    cost = _cost(player, 12)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    raw = random.randint(player.get_effective_min_attack(), player.get_total_attack())
    dmg = player.apply_armor_reduction(raw, target.get_total_armor())
    target.hp          = max(0, target.hp - dmg)
    target.poison_stacks = getattr(target, "poison_stacks", 0) + 3
    return f"🗡️  Giftklinge! {dmg} Schaden + 3 Giftstacks auf {target.name}!", dmg


def blendpulver(player, target) -> str:
    cost = _cost(player, 20)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})"
    player.energy -= cost
    target.blind_turns = getattr(target, "blind_turns", 0) + 2
    return f"💨 Blendpulver! {target.name} ist geblendet und verfehlt 2 Angriffe!"


def rauchbombe(player) -> str:
    cost = _cost(player, 10)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})"
    player.energy -= cost
    return "__FLEE__"


# ── MAGIER ───────────────────────────────────────────────────────────────────

def arkane_entladung(player, enemy_list) -> tuple:
    cost = _cost(player, 15)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    double = "mage_double_arcane" in player.get_set_specials()
    hits   = 2 if double else 1
    dmg    = random.randint(6 + player.level * 2, 12 + player.level * 3)
    living = [e for e in enemy_list if e.is_alive()]
    for e in living:
        e.hp = max(0, e.hp - dmg * hits)
    names  = ", ".join(e.name for e in living)
    suffix = " (Arkane Roben: 2× Treffer!)" if double else ""
    return (
        f"✨ Arkane Entladung! {dmg * hits} Schaden (ignoriert DEF) an: {names}{suffix}",
        dmg * hits * len(living),
    )


def froststrahl(player, target) -> tuple:
    cost = _cost(player, 18)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    dmg = random.randint(15, 25)
    target.hp      = max(0, target.hp - dmg)
    target.stunned = True
    return f"❄️  Froststrahl! {dmg} Eisschaden (ignoriert DEF) — {target.name} ist eingefroren!", dmg


def feuerball(player, target) -> tuple:
    cost = _cost(player, 22)
    if player.energy < cost:
        return f"Nicht genug Energie! ({player.energy}/{cost})", 0
    player.energy -= cost
    raw = random.randint(player.get_effective_min_attack(), player.get_total_attack()) + 4
    dmg = player.apply_armor_reduction(raw, target.get_total_armor())
    target.hp          = max(0, target.hp - dmg)
    target.burn_stacks = getattr(target, "burn_stacks", 0) + 3
    return f"🔥 Feuerball! {dmg} Schaden + 3 Verbrennungsstacks auf {target.name}!", dmg


def mana_schild_aktivieren(player) -> str:
    player.mana_shield_active = True
    return "🔮 Mana-Schild aktiviert! Nächster Angriff wird durch Energie absorbiert."
