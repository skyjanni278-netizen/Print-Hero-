import random
from content.monsters import (
    Slime, ShadowWolf, Goblin, WoodTroll,
    Zombie, Skeleton, Bandit, VenomSpider,
    Assassin, IceWitch, StoneGolem, DarkKnight,
    Dragon, FireDemon,
)

ZONE_DEFS = {
    "wald": {
        "name":         "Wald",
        "emoji":        "🌲",
        "desc":         "Dunkle Wälder, voll wilder Bestien.",
        "unlock_level": 1,
        "rank_weights": [65, 28,  7,  0,  0],
        "group_size":   (1, 2),
        "monsters":     [(Slime, 30), (ShadowWolf, 40), (Goblin, 20), (WoodTroll, 10)],
    },
    "ruinen": {
        "name":         "Ruinen",
        "emoji":        "🏚️",
        "desc":         "Verfallene Gemäuer, von Untoten heimgesucht.",
        "unlock_level": 2,
        "rank_weights": [50, 33, 14,  3,  0],
        "group_size":   (1, 3),
        "monsters":     [(Zombie, 35), (Skeleton, 35), (Bandit, 20), (WoodTroll, 10)],
    },
    "wueste": {
        "name":         "Wüste",
        "emoji":        "🏜️",
        "desc":         "Glühender Sand und gnadenlose Räuber.",
        "unlock_level": 4,
        "rank_weights": [30, 35, 25,  9,  1],
        "group_size":   (1, 3),
        "monsters":     [(Bandit, 30), (Assassin, 30), (VenomSpider, 25), (Goblin, 15)],
    },
    "vulkan": {
        "name":         "Vulkan",
        "emoji":        "🌋",
        "desc":         "Flammende Abgründe voller Dämonen.",
        "unlock_level": 6,
        "rank_weights": [15, 30, 30, 20,  5],
        "group_size":   (1, 3),
        "monsters":     [(FireDemon, 35), (StoneGolem, 30), (Dragon, 25), (DarkKnight, 10)],
    },
    "dunkelreich": {
        "name":         "Dunkel-Reich",
        "emoji":        "💀",
        "desc":         "Das Reich der Finsternis — nur für die Stärksten.",
        "unlock_level": 8,
        "rank_weights": [ 5, 20, 30, 30, 15],
        "group_size":   (2, 4),
        "monsters":     [(DarkKnight, 30), (IceWitch, 25), (Dragon, 25), (FireDemon, 20)],
    },
}

ZONE_ORDER = ["wald", "ruinen", "wueste", "vulkan", "dunkelreich"]


def get_unlocked_zones(player_level: int) -> list:
    return [zid for zid in ZONE_ORDER if player_level >= ZONE_DEFS[zid]["unlock_level"]]


def roll_rank_for_zone(zone_id: str) -> int:
    zdef = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])
    return random.choices([1, 2, 3, 4, 5], weights=zdef["rank_weights"], k=1)[0]


def create_zone_enemy(player, zone_id: str = None):
    if zone_id is None:
        zone_id = getattr(player, "current_zone", "wald")
    zdef = ZONE_DEFS.get(zone_id, ZONE_DEFS["wald"])

    classes, weights = zip(*zdef["monsters"])
    mob_class = random.choices(list(classes), weights=list(weights), k=1)[0]
    rank = roll_rank_for_zone(zone_id)
    mob  = mob_class(rank=rank)

    diff = getattr(player, "difficulty", "normal")
    if diff != "normal":
        from config import DIFFICULTY_SETTINGS
        cfg        = DIFFICULTY_SETTINGS[diff]
        mob.max_hp = max(1, int(mob.max_hp * cfg["hp_mult"]))
        mob.hp     = mob.max_hp
        mob.attack = max(1, int(mob.attack * cfg["atk_mult"]))

    ng = getattr(player, "ng_plus", 0)
    if ng > 0:
        mult       = 1.3 ** ng
        mob.max_hp = max(1, int(mob.max_hp * mult))
        mob.hp     = mob.max_hp
        mob.attack = max(1, int(mob.attack * mult))

    return mob
