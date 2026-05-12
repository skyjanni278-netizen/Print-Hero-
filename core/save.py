import json
import os
from core.player import Character

SAVE_DIR = "saves"

def _slot_path(slot: int) -> str:
    return os.path.join(SAVE_DIR, f"savegame_{slot}.json")

def get_save_slots() -> list:
    """Returns info dicts for all 3 slots."""
    slots = []
    for s in (1, 2, 3):
        path = _slot_path(s)
        if os.path.exists(path):
            with open(path, "r") as f:
                d = json.load(f)
            slots.append({
                "slot": s, "exists": True,
                "name": d.get("name", "?"),
                "level": d.get("level", 1),
                "player_class": d.get("player_class", "warrior"),
                "ng_plus": d.get("ng_plus", 0),
                "difficulty": d.get("difficulty", "normal"),
            })
        else:
            slots.append({"slot": s, "exists": False})
    return slots

def save_game(player):
    os.makedirs(SAVE_DIR, exist_ok=True)
    slot = getattr(player, "save_slot", 1)
    path = _slot_path(slot)
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "min_attack": player.min_attack,
        "armor": player.armor,
        "level": player.level,
        "xp": player.xp,
        "xp_to_level_up": player.xp_to_level_up,
        "energy": player.energy,
        "max_energy": player.max_energy,
        "inventory": player.inventory,
        "equipment": player.equipment,
        "stats": player.stats,
        "difficulty": player.difficulty,
        "skill_points": player.skill_points,
        "skills": list(player.skills),
        "shield_ready": player.shield_ready,
        "equipment_upgrades": player.equipment_upgrades,
        "fights_until_event": player.fights_until_event,
        "next_fight_xp_mult": player.next_fight_xp_mult,
        "ng_plus": player.ng_plus,
        "achievements": list(getattr(player, "achievements", set())),
        "player_class": getattr(player, "player_class", "warrior"),
        "current_zone": getattr(player, "current_zone", "wald"),
        "passive_crit_bonus": getattr(player, "passive_crit_bonus", 0.0),
        "schwarzmarkt_available": getattr(player, "schwarzmarkt_available", True),
        "shop_stock": getattr(player, "shop_stock", []),
        "zone_progress": getattr(player, "zone_progress", {}),
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Spielstand {slot} gespeichert!")

def load_game(slot: int = 1):
    path = _slot_path(slot)
    # Legacy fallback für alten einzelnen Spielstand
    if not os.path.exists(path):
        legacy = os.path.join(SAVE_DIR, "savegame.json")
        if os.path.exists(legacy):
            path = legacy
        elif os.path.exists("savegame.json"):
            path = "savegame.json"
        else:
            return None
    with open(path, "r") as f:
        data = json.load(f)
    player = Character(data["name"], data["max_hp"], data["attack"])
    player.hp             = data["hp"]
    player.min_attack     = data["min_attack"]
    player.armor          = data["armor"]
    player.level          = data["level"]
    player.xp             = data["xp"]
    player.xp_to_level_up = data["xp_to_level_up"]
    player.energy         = data["energy"]
    player.max_energy     = data["max_energy"]
    player.equipment      = data["equipment"]
    _slot_types = {"weapon": "weapon", "chest": "chest", "head": "head", "feet": "feet"}
    for eq_slot, item in player.equipment.items():
        if "type" not in item:
            item["type"] = _slot_types[eq_slot]
    player.inventory      = data["inventory"]
    default_stats = {"fights": 0, "kills": 0, "deaths": 0,
                     "damage_dealt": 0, "damage_taken": 0,
                     "gold_earned": 0, "potions_used": 0,
                     "dungeons_completed": 0, "dungeons_fled": 0,
                     "zone_kills": {}, "zones_cleared": []}
    player.stats               = {**default_stats, **data.get("stats", {})}
    player.difficulty          = data.get("difficulty", "normal")
    player.fights_until_event  = data.get("fights_until_event", 2)
    player.next_fight_xp_mult  = data.get("next_fight_xp_mult", 1.0)
    player.skill_points        = data.get("skill_points", 0)
    player.skills              = set(data.get("skills", []))
    player.shield_ready        = data.get("shield_ready", False)
    player.shield_active       = False
    default_upgrades           = {"weapon": 0, "chest": 0, "head": 0, "feet": 0}
    player.equipment_upgrades  = {**default_upgrades, **data.get("equipment_upgrades", {})}
    player.ng_plus             = data.get("ng_plus", 0)
    player.achievements        = set(data.get("achievements", []))
    player.player_class        = data.get("player_class", "warrior")
    player.current_zone        = data.get("current_zone", "wald")
    player.class_ability_used  = False
    player.class_ability2_used = False
    player.class_ability3_used = False
    player.block_next          = False
    player.shadow_strike_ready = False
    player.mana_shield_active  = False
    player.passive_crit_bonus      = data.get("passive_crit_bonus", 0.0)
    player.schwarzmarkt_available  = data.get("schwarzmarkt_available", True)
    player.shop_stock              = data.get("shop_stock", [])
    _default_zp = {
        zid: {"dungeons_completed": 0, "boss_defeated": False}
        for zid in ["wald", "ruinen", "wueste", "vulkan", "dunkelreich"]
    }
    player.zone_progress           = {**_default_zp, **data.get("zone_progress", {})}
    player.save_slot               = slot
    print(f"📂 Spielstand {slot} geladen!")
    return player

def save_exists():
    return (
        any(os.path.exists(_slot_path(s)) for s in (1, 2, 3))
        or os.path.exists(os.path.join(SAVE_DIR, "savegame.json"))
        or os.path.exists("savegame.json")
    )
