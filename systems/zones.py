import random
from content.monsters import (
    Slime, ShadowWolf, Goblin, WoodTroll,
    Zombie, Skeleton, Bandit, VenomSpider,
    Assassin, IceWitch, StoneGolem, DarkKnight,
    Dragon, FireDemon,
    ForestSpirit, Lich, SandWorm,
)

ZONE_DEFS = {
    "wald": {
        "name":          "Wald",
        "emoji":         "🌲",
        "desc":          "Dunkle Wälder, voll wilder Bestien.",
        "unlock_level":  1,
        "rank_weights":  [65, 28,  7,  0,  0],
        "group_size":    (1, 2),
        "monsters":      [(Slime, 25), (ShadowWolf, 35), (Goblin, 20), (WoodTroll, 10), (ForestSpirit, 10)],
        "boss_class":    WoodTroll,
        "dungeon_count": 3,
    },
    "ruinen": {
        "name":          "Ruinen",
        "emoji":         "🏚️",
        "desc":          "Verfallene Gemäuer, von Untoten heimgesucht.",
        "unlock_level":  2,
        "rank_weights":  [50, 33, 14,  3,  0],
        "group_size":    (1, 3),
        "monsters":      [(Zombie, 30), (Skeleton, 30), (Bandit, 20), (WoodTroll, 10), (Lich, 10)],
        "boss_class":    StoneGolem,
        "dungeon_count": 4,
    },
    "wueste": {
        "name":          "Wüste",
        "emoji":         "🏜️",
        "desc":          "Glühender Sand und gnadenlose Räuber.",
        "unlock_level":  4,
        "rank_weights":  [30, 35, 25,  9,  1],
        "group_size":    (1, 3),
        "monsters":      [(Bandit, 25), (Assassin, 25), (VenomSpider, 20), (Goblin, 15), (SandWorm, 15)],
        "boss_class":    Assassin,
        "dungeon_count": 5,
    },
    "vulkan": {
        "name":          "Vulkan",
        "emoji":         "🌋",
        "desc":          "Flammende Abgründe voller Dämonen.",
        "unlock_level":  6,
        "rank_weights":  [15, 30, 30, 20,  5],
        "group_size":    (1, 3),
        "monsters":      [(FireDemon, 35), (StoneGolem, 30), (Dragon, 25), (DarkKnight, 10)],
        "boss_class":    Dragon,
        "dungeon_count": 6,
    },
    "dunkelreich": {
        "name":          "Dunkel-Reich",
        "emoji":         "💀",
        "desc":          "Das Reich der Finsternis — nur für die Stärksten.",
        "unlock_level":  8,
        "rank_weights":  [ 5, 20, 30, 30, 15],
        "group_size":    (2, 4),
        "monsters":      [(DarkKnight, 30), (IceWitch, 25), (Dragon, 25), (FireDemon, 20)],
        "boss_class":    DarkKnight,
        "dungeon_count": 7,
    },
}

ZONE_ORDER = ["wald", "ruinen", "wueste", "vulkan", "dunkelreich"]

ZONE_FLAVOR = {
    "wald": [
        "Die Bäume flüstern alte Geheimnisse. Zwischen den Ästen glitzern gefährliche Augen.",
        "Moosbedeckte Pfade winden sich tiefer in die Dunkelheit. Hier hat die Sonne keine Kraft mehr.",
        "Ein Knacken im Unterholz — du bist nicht allein.",
    ],
    "ruinen": [
        "Gebrochene Mauern recken sich zum grauen Himmel. Die Toten hier kennen keinen Frieden.",
        "Zwischen verwitterten Steinen flüstert der Wind wie klagende Seelen.",
        "Einst stand hier eine stolze Festung. Jetzt nur noch Asche und Knochen.",
    ],
    "wueste": [
        "Die Sonne brennt erbarmungslos. Hinter jedem Sandhügel könnte der Tod lauern.",
        "Hitzewellen lassen die Luft flimmern. Banditen kennen diese Wüste besser als du.",
        "Kein Schatten, kein Wasser. Nur Sand, Stille — und das Rascheln von Stahl.",
    ],
    "vulkan": [
        "Der Boden zittert. Aus tiefen Spalten steigt glühende Asche empor.",
        "Die Hitze ist fast unerträglich. Nur Bestien, die aus dem Feuer geboren wurden, gedeihen hier.",
        "Lavafontänen beleuchten den Weg in die Hölle. Zurückzugehen ist keine Option mehr.",
    ],
    "dunkelreich": [
        "Absolute Finsternis. Selbst das Licht deiner Fackel wagt sich kaum vorwärts.",
        "Hier herrscht etwas Uraltes. Etwas, das weit mächtiger ist als du.",
        "Die Luft riecht nach Verwesung und verbotener Magie. Jeder Schritt könnte dein letzter sein.",
    ],
}


def _is_zone_unlocked(player, zone_id: str) -> bool:
    idx = ZONE_ORDER.index(zone_id)
    if idx == 0:
        return True
    if player.level < ZONE_DEFS[zone_id]["unlock_level"]:
        return False
    prev_zone = ZONE_ORDER[idx - 1]
    zp = getattr(player, "zone_progress", {})
    return zp.get(prev_zone, {}).get("boss_defeated", False)


def get_unlocked_zones(player_or_level) -> list:
    if isinstance(player_or_level, int):
        return [zid for zid in ZONE_ORDER if player_or_level >= ZONE_DEFS[zid]["unlock_level"]]
    return [zid for zid in ZONE_ORDER if _is_zone_unlocked(player_or_level, zid)]


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
        mult       = min(1.3 ** ng, 3.0)
        mob.max_hp = max(1, int(mob.max_hp * mult))
        mob.hp     = mob.max_hp
        mob.attack = max(1, int(mob.attack * mult))

    # Basis-Buff normale Gegner (+10%)
    mob.max_hp = max(1, int(mob.max_hp * 1.1))
    mob.hp     = mob.max_hp
    mob.attack = max(1, int(mob.attack * 1.1))

    return mob
