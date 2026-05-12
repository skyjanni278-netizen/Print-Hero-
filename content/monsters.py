import random
from core.player import Character

# Neue Status-Typen fuer Boss-Faehigkeiten
# player.stunned        → Spieler ueberspringt naechste Runde
# player.armor_debuff   → Temporaere DEF-Reduktion diesen Kampf
# player.poison_stacks  → Schaden pro Runde wie Blutung


RANK_CONFIG = {
    1: {"title": "",            "hp_mult": 1.0,  "atk_mult": 1.0,  "loot_rolls": 1, "xp_mult": 1.0},
    2: {"title": "⚔️ Starker",  "hp_mult": 1.4,  "atk_mult": 1.3,  "loot_rolls": 2, "xp_mult": 1.4},
    3: {"title": "💀 Eliter",   "hp_mult": 2.0,  "atk_mult": 1.6,  "loot_rolls": 3, "xp_mult": 2.0},
    4: {"title": "👑 Champion", "hp_mult": 3.0,  "atk_mult": 2.0,  "loot_rolls": 4, "xp_mult": 3.0},
    5: {"title": "🔥 Boss",     "hp_mult": 5.0,  "atk_mult": 2.8,  "loot_rolls": 6, "xp_mult": 5.0},
}


def _apply_rank(mob, base_hp, base_attack, base_xp, rank):
    cfg = RANK_CONFIG.get(rank, RANK_CONFIG[1])
    mob.rank       = rank
    mob.loot_rolls = cfg["loot_rolls"]

    mob.max_hp   = max(1, int(base_hp     * cfg["hp_mult"]))
    mob.hp       = mob.max_hp
    mob.attack   = max(1, int(base_attack * cfg["atk_mult"]))
    # min_attack für Gegner: ~50% des max-Angriffs, mindestens 1
    mob.min_attack = max(1, int(mob.attack * 0.5))
    mob.xp_value  = int(base_xp * cfg["xp_mult"])

    title = cfg["title"]
    mob.name = f"{title} {mob.name}".strip() if title else mob.name



class Zombie(Character):
    BASE_HP     = 20
    BASE_ATTACK = 4
    BASE_XP     = 18

    def __init__(self, rank: int = 1):
        super().__init__("Zombie", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 2
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        stacks = 3
        target.poison_stacks = getattr(target, "poison_stacks", 0) + stacks
        return f"☠️  {self.name}: Fauliger Biss! {target.name} erhält {stacks} Giftstacks!"


class Skeleton(Character):
    BASE_HP     = 12
    BASE_ATTACK = 8
    BASE_XP     = 24

    def __init__(self, rank: int = 1):
        super().__init__("Skelett", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 1
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        target.bleed_stacks += 3
        return f"🦴 {self.name}: Knochenregen! {target.name} erhält 3 Blutungsstacks!"


class Slime(Character):
    BASE_HP     = 8
    BASE_ATTACK = 3
    BASE_XP     = 10

    def __init__(self, rank: int = 1):
        super().__init__("Schleim", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        debuff = 3
        target.armor_debuff = getattr(target, "armor_debuff", 0) + debuff
        return f"🟢 {self.name}: Säurewelle! {target.name} verliert {debuff} DEF für diesen Kampf."


class Goblin(Character):
    BASE_HP     = 10
    BASE_ATTACK = 5
    BASE_XP     = 15

    def __init__(self, rank: int = 1):
        super().__init__("Goblin", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 1
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        stolen = min(random.randint(15, 30), target.inventory.get("Gold", 0))
        target.inventory["Gold"] = target.inventory.get("Gold", 0) - stolen
        return f"💰 {self.name}: Räuberische Hände! Stiehlt {stolen} Gold von {target.name}."


class Dragon(Character):
    BASE_HP     = 50
    BASE_ATTACK = 15
    BASE_XP     = 60

    def __init__(self, rank: int = 1):
        super().__init__("Drache", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 7
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        dmg = random.randint(15, 25)
        target.hp = max(0, target.hp - dmg)
        return f"🔥 {self.name}: Feueratem! {dmg} Schaden (ignoriert DEF) an {target.name}! (HP: {target.hp}/{target.max_hp})"


class Bandit(Character):
    """Schneller Angreifer – erscheint LVL 2–8, mittlere HP, hoher Angriff"""
    BASE_HP     = 14
    BASE_ATTACK = 7
    BASE_XP     = 20

    def __init__(self, rank: int = 1):
        super().__init__("Bandit", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        msg1, dmg1 = self.attack_target(target)
        return f"⚡ {self.name}: Doppelschlag!\n  {msg1}"


class WoodTroll(Character):
    """Tanky Nahkämpfer – erscheint LVL 3–9, hohe HP, mittlerer Angriff"""
    BASE_HP            = 35
    BASE_ATTACK        = 6
    BASE_XP            = 30
    boss_ability_chance = 0.15  # Betäubung seltener als Standard (30%)

    def __init__(self, rank: int = 1):
        super().__init__("Waldtroll", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 4
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        target.stunned = True
        return f"🪨 {self.name}: Erdschlag! {target.name} ist betäubt und überspringt die nächste Runde!"


class ShadowWolf(Character):
    """Rudeltier – erscheint LVL 1–6, niedrige HP, schnelle Angriffe"""
    BASE_HP     = 11
    BASE_ATTACK = 6
    BASE_XP     = 16

    def __init__(self, rank: int = 1):
        super().__init__("Schattenwolf", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def boss_ability(self, target) -> str:
        heal = random.randint(10, 20)
        self.hp = min(self.max_hp, self.hp + heal)
        return f"🐺 {self.name}: Rudel-Heul! Heilt sich selbst um {heal} HP. (HP: {self.hp}/{self.max_hp})"


class VenomSpider(Character):
    """Giftige Spinne – erscheint LVL 2–6, schwach aber vergiftet zuverlässig"""
    BASE_HP     = 9
    BASE_ATTACK = 5
    BASE_XP     = 14

    def __init__(self, rank: int = 1):
        super().__init__("Giftige Spinne", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        msg, dmg = super().attack_target(target)
        if random.random() < 0.40:
            stacks = 2
            target.poison_stacks += stacks
            return f"{msg}\n  🕷️  Giftstich! {target.name} erhält {stacks} Giftstacks.", dmg
        return msg, dmg

    def boss_ability(self, target) -> str:
        stacks = 5
        target.poison_stacks += stacks
        return f"🕷️  {self.name}: Giftwolke! {target.name} erhält {stacks} Giftstacks!"


class Assassin(Character):
    """Meuchler – erscheint LVL 3–8, niedriger HP aber kann Rüstung ignorieren"""
    BASE_HP     = 13
    BASE_ATTACK = 10
    BASE_XP     = 28

    def __init__(self, rank: int = 1):
        super().__init__("Meuchler", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        if random.random() < 0.25:
            raw = random.randint(self.get_effective_min_attack(), self.get_total_attack()) * 2
            target.hp = max(0, target.hp - raw)
            return f"🗡️  {self.name}: Meucheln! {raw} Schaden (ignoriert Rüstung) 💥 KRITISCH!", raw
        return super().attack_target(target)

    def boss_ability(self, target) -> str:
        raw = random.randint(self.get_effective_min_attack(), self.get_total_attack()) * 2
        target.hp = max(0, target.hp - raw)
        target.bleed_stacks += 3
        return f"🗡️  {self.name}: Aus dem Schatten! {raw} Schaden (ignoriert DEF) + 3 Blutungsstacks!"


class IceWitch(Character):
    """Eismagierin – erscheint LVL 4–9, kann einfrieren und Rüstung halbieren"""
    BASE_HP     = 22
    BASE_ATTACK = 11
    BASE_XP     = 35

    def __init__(self, rank: int = 1):
        super().__init__("Eismagierin", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 1
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        if random.random() < 0.30:
            raw        = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            half_armor = max(0, target.get_total_armor() // 2)
            real       = self.apply_armor_reduction(raw, half_armor)
            target.hp  = max(0, target.hp - real)
            target.stunned = True
            return f"❄️  {self.name}: Frostpfeil! {real} Eisschaden — {target.name} ist eingefroren (nächste Runde betäubt)!", real
        return super().attack_target(target)

    def boss_ability(self, target) -> str:
        dmg = random.randint(18, 28)
        target.hp = max(0, target.hp - dmg)
        debuff = 4
        target.armor_debuff += debuff
        return f"❄️  {self.name}: Eisnova! {dmg} magischen Schaden (ignoriert DEF) + -{debuff} DEF für diesen Kampf!"


class StoneGolem(Character):
    """Steingolem – erscheint LVL 5–10, sehr hohe HP und Rüstung, kann betäuben"""
    BASE_HP     = 55
    BASE_ATTACK = 8
    BASE_XP     = 45

    def __init__(self, rank: int = 1):
        super().__init__("Steingolem", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 8
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        if random.random() < 0.30:
            raw  = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            real = self.apply_armor_reduction(raw, target.get_total_armor())
            target.hp = max(0, target.hp - real)
            target.stunned = True
            return f"🪨 {self.name}: Felsstoß! {real} Schaden — {target.name} ist betäubt!", real
        return super().attack_target(target)

    def boss_ability(self, target) -> str:
        dmg = random.randint(20, 35)
        target.hp = max(0, target.hp - dmg)
        debuff = 5
        target.armor_debuff += debuff
        return f"🪨 {self.name}: Erschütterung! {dmg} Schaden (ignoriert DEF) + -{debuff} DEF für diesen Kampf!"


class DarkKnight(Character):
    """Dunkelritter – erscheint LVL 6–10, hohe HP + Rüstung, Klingenwirbel verursacht Blutung"""
    BASE_HP     = 40
    BASE_ATTACK = 12
    BASE_XP     = 50

    def __init__(self, rank: int = 1):
        super().__init__("Dunkelritter", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 6
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        if random.random() < 0.25:
            raw  = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            real = self.apply_armor_reduction(raw, target.get_total_armor())
            target.hp = max(0, target.hp - real)
            target.bleed_stacks += 3
            return f"⚔️  {self.name}: Klingenwirbel! {real} Schaden + 3 Blutungsstacks!", real
        return super().attack_target(target)

    def boss_ability(self, target) -> str:
        dmg = random.randint(25, 40)
        target.hp = max(0, target.hp - dmg)
        target.bleed_stacks += 4
        return f"⚔️  {self.name}: Dunkle Klinge! {dmg} Schaden (ignoriert DEF) + 4 Blutungsstacks!"


class FireDemon(Character):
    """Flammendämon – erscheint LVL 7–10, Feuerangriffe ignorieren halbe Rüstung"""
    BASE_HP     = 30
    BASE_ATTACK = 13
    BASE_XP     = 55

    def __init__(self, rank: int = 1):
        super().__init__("Flammendämon", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 3
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)

    def attack_target(self, target):
        if random.random() < 0.35:
            raw        = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            half_armor = max(0, target.get_total_armor() // 2)
            real       = self.apply_armor_reduction(raw, half_armor)
            target.hp  = max(0, target.hp - real)
            return f"🔥 {self.name}: Feuerball! {real} Feuerschaden (halbe DEF ignoriert)!", real
        return super().attack_target(target)

    def boss_ability(self, target) -> str:
        dmg = random.randint(20, 35)
        target.hp = max(0, target.hp - dmg)
        target.poison_stacks += 2
        return f"🔥 {self.name}: Inferno! {dmg} Feuerschaden (ignoriert DEF) + 2 Verbrennungsstacks!"


def roll_rank(player_level: int) -> int:
    """
    Höhere Spieler-Level → höhere Chance auf starke Ränge (bis LVL 10).
    Gibt einen Rang 1–5 zurück.
    """
    if player_level <= 2:
        weights = [75, 22, 3,  0,  0]   
    elif player_level <= 4:
        weights = [50, 33, 14, 3,  0]   
    elif player_level <= 6:
        weights = [30, 35, 25, 9,  1]   
    elif player_level <= 8:
        weights = [15, 30, 30, 20, 5]   
    else:
        weights = [5,  20, 30, 30, 15]  

    return random.choices([1, 2, 3, 4, 5], weights=weights, k=1)[0]
