import random
from player import Character


RANK_CONFIG = {
    1: {"title": "",            "hp_mult": 1.0,  "atk_mult": 1.0,  "loot_rolls": 1, "xp_mult": 1.0},
    2: {"title": "⚔️ Starker",  "hp_mult": 1.4,  "atk_mult": 1.3,  "loot_rolls": 2, "xp_mult": 1.4},
    3: {"title": "💀 Eliter",   "hp_mult": 2.0,  "atk_mult": 1.6,  "loot_rolls": 3, "xp_mult": 2.0},
    4: {"title": "👑 Champion", "hp_mult": 3.0,  "atk_mult": 2.0,  "loot_rolls": 4, "xp_mult": 3.0},
    5: {"title": "🔥 Boss",     "hp_mult": 5.0,  "atk_mult": 2.8,  "loot_rolls": 6, "xp_mult": 5.0},
}


def _apply_rank(mob, base_hp, base_attack, base_xp, rank):
    """Wendet Rang-Multiplikatoren auf einen Mob an."""
    cfg = RANK_CONFIG.get(rank, RANK_CONFIG[1])
    mob.rank       = rank
    mob.loot_rolls = cfg["loot_rolls"]

    mob.max_hp  = max(1, int(base_hp     * cfg["hp_mult"]))
    mob.hp      = mob.max_hp
    mob.attack  = max(1, int(base_attack * cfg["atk_mult"]))
    mob.xp_value = int(base_xp * cfg["xp_mult"])

    title = cfg["title"]
    mob.name = f"{title} {mob.name}".strip() if title else mob.name



class Zombie(Character):
    BASE_HP     = 20
    BASE_ATTACK = 4
    BASE_XP     = 18   # war 60

    def __init__(self, rank: int = 1):
        super().__init__("Zombie", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 2
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)


class Skeleton(Character):
    BASE_HP     = 12
    BASE_ATTACK = 8
    BASE_XP     = 24   # war 80

    def __init__(self, rank: int = 1):
        super().__init__("Skelett", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 1
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)


class Slime(Character):
    BASE_HP     = 8
    BASE_ATTACK = 3
    BASE_XP     = 10   # war 35

    def __init__(self, rank: int = 1):
        super().__init__("Schleim", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 0
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)


class Goblin(Character):
    BASE_HP     = 10
    BASE_ATTACK = 5
    BASE_XP     = 15   # war 50

    def __init__(self, rank: int = 1):
        super().__init__("Goblin", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 1
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)


class Dragon(Character):
    BASE_HP     = 50
    BASE_ATTACK = 15
    BASE_XP     = 60   # war 200

    def __init__(self, rank: int = 1):
        super().__init__("Drache", hp=self.BASE_HP, attack=self.BASE_ATTACK)
        self.armor = 7
        _apply_rank(self, self.BASE_HP, self.BASE_ATTACK, self.BASE_XP, rank)


def roll_rank(player_level: int) -> int:
    """
    Höhere Spieler-Level → höhere Chance auf starke Ränge (bis LVL 10).
    Gibt einen Rang 1–5 zurück.
    """
    if player_level <= 2:
        weights = [75, 22, 3,  0,  0]   # fast nur Rang 1
    elif player_level <= 4:
        weights = [50, 33, 14, 3,  0]   # Rang 2 häufiger
    elif player_level <= 6:
        weights = [30, 35, 25, 9,  1]   # Rang 3 sichtbar
    elif player_level <= 8:
        weights = [15, 30, 30, 20, 5]   # Rang 4 relevant
    else:
        weights = [5,  20, 30, 30, 15]  # LVL 9-10: auch Rang 5

    return random.choices([1, 2, 3, 4, 5], weights=weights, k=1)[0]
