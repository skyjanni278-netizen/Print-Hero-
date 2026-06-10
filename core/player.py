import random
from config import (
    BLEED_DAMAGE, POISON_DAMAGE, BURN_DAMAGE, ENERGY_REGEN,
    LEVEL_HP_GAIN, LEVEL_ATK_GAIN, MAX_INVENTORY_SLOTS, XP_MULTIPLIERS,
)


class Character:
    def __init__(self, name, hp, attack):
        self.name = name

        self.hp = hp
        self.max_hp = hp
        self.armor = 0

        self.attack = attack
        self.min_attack = 1
        self.bleed_stacks = 0

        self.level = 1
        self.xp = 0
        self.xp_to_level_up = 30  # Lvl 1→2: ~1 Kampf

        self.max_energy = 30
        self.energy = 15
        self.energy_regen = ENERGY_REGEN

        # Temporäre Kampf-Boni – werden nach dem Kampf zurückgesetzt
        self.combat_modifiers = {"attack": 0}

        # Boss-Status-Effekte (nur während Kampf aktiv)
        self.stunned       = False
        self.poison_stacks = 0
        self.burn_stacks   = 0
        self.armor_debuff  = 0

        self.difficulty          = "normal"
        self.next_fight_xp_mult  = 1.0
        self.next_fight_atk_mult = 1.0
        self.fights_until_event  = random.randint(2, 3)

        self.skill_points  = 0
        self.skills        = set()
        self.shield_ready  = False
        self.shield_active = False

        self.equipment_upgrades = {"weapon": 0, "chest": 0, "head": 0, "feet": 0}

        self.achievements = set()

        self.player_class        = "warrior"
        self.ability_cooldowns   = {"S": 0, "R": 0, "C": 0, "X": 0}
        self.block_next          = False
        self.block_charges       = 0
        self.shadow_strike_ready = False
        self.mana_shield_active  = False
        self.passive_crit_bonus  = 0.0

        self.current_zone = "wald"
        self.schwarzmarkt_available = True
        self.shop_stock = []

        self.zone_progress = {
            zid: {"dungeons_completed": 0, "boss_defeated": False}
            for zid in ["wald", "ruinen", "wueste", "vulkan", "dunkelreich"]
        }

        self.stats = {
            "fights": 0,
            "kills": 0,
            "deaths": 0,
            "damage_dealt": 0,
            "damage_taken": 0,
            "gold_earned": 0,
            "potions_used": 0,
            "dungeons_completed": 0,
            "dungeons_fled": 0,
            "zone_kills": {},
            "zones_cleared": [],
        }

        self.equipment = {
            "weapon": {"name": "Fäuste",       "attack": 0, "type": "weapon"},
            "chest":  {"name": "Lumpen",       "armor": 0,  "type": "chest"},
            "head":   {"name": "Kein Helm",    "armor": 0,  "type": "head"},
            "feet":   {"name": "Keine Schuhe", "armor": 0,  "type": "feet"},
        }
        self.inventory = {
            "Consumables": {"Healing Potion": 2},
            "Junk":        {},   # {"Altes Seil": 3, ...}
            "Gold":        0,
            "Equipment":   []    # nicht stapelbar, 1 Slot pro Stück
        }

    # ── Inventar-Slot-Verwaltung ─────────────────────────────
    def inventory_count(self) -> int:
        c = len(self.inventory.get("Consumables", {}))
        j = len(self.inventory.get("Junk", {}))
        e = len(self.inventory.get("Equipment", []))
        return c + j + e

    def has_inventory_space(self) -> bool:
        return self.inventory_count() < MAX_INVENTORY_SLOTS

    def add_consumable(self, key: str, amount: int) -> int:
        from content.loot_tables import CONSUMABLE_DEFS
        cdef      = CONSUMABLE_DEFS.get(key, {})
        max_stack = cdef.get("max_stack", 99)

        consumables = self.inventory.setdefault("Consumables", {})
        current     = consumables.get(key, 0)

        # Neuer Stapel braucht freien Slot
        if current == 0 and not self.has_inventory_space():
            return 0

        # Wie viel passt noch auf den Stapel?
        can_add = max(0, max_stack - current)
        added   = min(amount, can_add)

        if added > 0:
            consumables[key] = current + added
        return added

    def can_add_consumable(self, key: str) -> bool:
        from content.loot_tables import CONSUMABLE_DEFS
        cdef      = CONSUMABLE_DEFS.get(key, {})
        max_stack = cdef.get("max_stack", 99)
        current   = self.inventory.get("Consumables", {}).get(key, 0)
        if current >= max_stack:
            return False
        if current == 0 and not self.has_inventory_space():
            return False
        return True

    def add_junk(self, key: str, amount: int) -> int:
        junk    = self.inventory.setdefault("Junk", {})
        current = junk.get(key, 0)

        if current == 0 and not self.has_inventory_space():
            return 0

        junk[key] = current + amount
        return amount

    # ── Stats ────────────────────────────────────────────────
    def get_set_bonus(self) -> dict:
        from content.loot_tables import get_active_sets
        atk = def_ = energy = 0
        for _, _, _, bonus in get_active_sets(self):
            atk    += bonus.get("atk", 0)
            def_   += bonus.get("def", 0)
            energy += bonus.get("energy", 0)
        return {"atk": atk, "def": def_, "energy": energy}

    def get_set_specials(self) -> set:
        from content.loot_tables import get_set_specials
        return get_set_specials(self)

    def get_effective_max_energy(self) -> int:
        return self.max_energy + self.get_set_bonus().get("energy", 0)

    def get_total_attack(self):
        skill_bonus   = 2 if "Scharfe Klingen" in self.skills else 0
        upgrade_bonus = self.equipment["weapon"].get("upgrade", self.equipment_upgrades.get("weapon", 0)) * 2
        set_bonus     = self.get_set_bonus()["atk"]
        return self.attack + self.equipment["weapon"]["attack"] + self.combat_modifiers.get("attack", 0) + skill_bonus + upgrade_bonus + set_bonus

    def reset_combat_modifiers(self):
        """Setzt alle temporären Kampfboni zurück. Nach jedem Kampf aufrufen."""
        self.combat_modifiers    = {"attack": 0}
        self.stunned             = False
        self.poison_stacks       = 0
        self.burn_stacks         = 0
        self.armor_debuff        = 0
        self.shield_active       = False
        self.block_next          = False
        self.block_charges       = 0
        self.shadow_strike_ready = False
        self.mana_shield_active  = False
        self.ability_cooldowns   = {"S": 0, "R": 0, "C": 0, "X": 0}

    def get_total_armor(self):
        skill_bonus = 3 if "Eisenhaut" in self.skills else 0
        upgrade_def = (
            self.equipment["chest"].get("upgrade", self.equipment_upgrades.get("chest", 0))
            + self.equipment["head"].get("upgrade", self.equipment_upgrades.get("head", 0))
            + self.equipment["feet"].get("upgrade", self.equipment_upgrades.get("feet", 0))
        )
        set_bonus   = self.get_set_bonus()["def"]
        return max(0, self.armor
                   + self.equipment["chest"]["armor"]
                   + self.equipment["head"]["armor"]
                   + self.equipment["feet"]["armor"]
                   + skill_bonus
                   + upgrade_def
                   + set_bonus
                   - self.armor_debuff)

    def get_effective_min_attack(self) -> int:
        weapon_bonus = self.equipment["weapon"]["attack"] // 2
        return max(1, self.min_attack + weapon_bonus)

    @staticmethod
    def apply_armor_reduction(raw_damage: int, armor: int) -> int:
        if armor <= 0:
            return raw_damage
        reduction = armor / (armor + 25)
        mitigated = int(raw_damage * reduction)
        return max(1, raw_damage - mitigated)

    # Welche Fähigkeiten bei welchem Level freigeschaltet werden
    SKILL_UNLOCKS = {
        3: ("Klassen-Fähigkeit [C]", "Klassenspezifisch mit Cooldown – Taste [C] im Kampf"),
        5: ("Klassen-Fähigkeit [X]", "Mächtige Einmal-Fähigkeit – Taste [X] im Kampf"),
    }

    def check_level_up(self) -> list:
        """Verarbeitet XP, steigt ggf. auf und gibt eine Liste von Rich-Markup-Nachrichten zurück."""
        msgs = []
        while self.xp >= self.xp_to_level_up:
            self.level += 1
            self.xp -= self.xp_to_level_up
            mult = XP_MULTIPLIERS.get(self.level - 1, 1.6)
            self.xp_to_level_up = int(self.xp_to_level_up * mult)
            self.max_hp  += LEVEL_HP_GAIN
            self.hp       = min(self.max_hp, self.hp + LEVEL_HP_GAIN)
            self.attack  += LEVEL_ATK_GAIN
            self.min_attack += LEVEL_ATK_GAIN
            self.skill_points += 1
            msgs.append(f"[bold yellow]✨ {self.name} ist nun Level {self.level}![/bold yellow]")
            msgs.append(f"[yellow]+1 Skillpunkt! (Gesamt: {self.skill_points})[/yellow]")
            if self.level in self.SKILL_UNLOCKS:
                skill_name, skill_desc = self.SKILL_UNLOCKS[self.level]
                msgs.append(f"[cyan]🔓 Neue Fähigkeit freigeschaltet: {skill_name}[/cyan]")
                msgs.append(f"[dim]  → {skill_desc}[/dim]")
            # Passive Klassen-Skalierung
            if self.player_class == "warrior" and self.level % 2 == 0:
                self.armor += 1
                msgs.append(f"[cyan]⚔️  Krieger-Passiv: +1 Rüstung durch Kampferfahrung! (Rüstung: {self.armor})[/cyan]")
            elif self.player_class == "mage" and self.level % 2 == 0:
                self.max_energy += 5
                msgs.append(f"[cyan]🔮 Magier-Passiv: +5 max. Energie durch Magiestudium! (Max. Energie: {self.max_energy})[/cyan]")
            elif self.player_class == "rogue" and self.level % 3 == 0:
                self.passive_crit_bonus += 0.05
                pct = int((0.10 + self.passive_crit_bonus) * 100)
                msgs.append(f"[cyan]🗡️  Schurken-Passiv: +5% Krit-Chance durch Präzision! (Krit: {pct}%)[/cyan]")
        return msgs

    def is_alive(self):
        return self.hp > 0

    def attack_target(self, target):
        raw_damage = random.randint(self.get_effective_min_attack(), self.get_total_attack())
        crit       = False
        ignore_def = False

        # Aus dem Schatten (Schurke): garantierter Krit + ignoriert DEF
        if self.shadow_strike_ready:
            self.shadow_strike_ready = False
            raw_damage *= 2
            crit        = True
            ignore_def  = True
        else:
            # Kritischer Treffer: 15% (+10% Schurke) Chance auf Doppelschaden
            specials    = self.get_set_specials()
            shadow_crit = 0.15 if "rogue_shadow_regen" in specials else 0.0
            set_crit    = 0.15 if "schatten_crit" in specials else 0.0
            rogue_bonus = (0.10 + self.passive_crit_bonus + shadow_crit) if self.player_class == "rogue" else 0
            base_crit   = 0.15 if "Kritischer Treffer" in self.skills else 0
            if random.random() < (base_crit + rogue_bonus + set_crit):
                raw_damage *= 2
                crit = True

        real_damage = raw_damage if ignore_def else self.apply_armor_reduction(raw_damage, target.get_total_armor())
        target.hp   = max(0, target.hp - real_damage)

        crit_tag = " 💥 KRITISCH!" if crit else ""

        # Blutgier: 20% Lifesteal
        if "Blutgier" in self.skills and random.random() < 0.20:
            heal = max(1, real_damage // 4)
            self.hp = min(self.max_hp, self.hp + heal)
            return f"{self.name} macht {real_damage} Schaden!{crit_tag} 🩸 Blutgier +{heal} HP", real_damage

        return f"{self.name} macht {real_damage} Schaden!{crit_tag}", real_damage

    def try_flee(self):
        if self.player_class == "rogue":
            return random.random() < 0.70
        return random.randint(1, 20) >= 10

    def regenerate(self):
        specials    = self.get_set_specials()
        extra_e     = 3 if "eisen_energy_regen" in specials else 0
        mage_bonus  = 3 if self.player_class == "mage" else 0
        energy_gain = self.energy_regen + (2 if "Energiefluss" in self.skills else 0) + mage_bonus + extra_e
        self.energy = min(self.get_effective_max_energy(), self.energy + energy_gain)
        msgs = [f"{self.name} regeneriert {energy_gain} Energie."]
        if "Regeneration" in self.skills:
            hp_gain = 1
            self.hp = min(self.max_hp, self.hp + hp_gain)
            msgs.append(f"+{hp_gain} HP durch Regeneration. (HP: {self.hp}/{self.max_hp})")
        if "licht_hp_regen" in specials:
            hp_gain = 3
            self.hp = min(self.max_hp, self.hp + hp_gain)
            msgs.append(f"+{hp_gain} HP Licht-Set. (HP: {self.hp}/{self.max_hp})")
        return " ".join(msgs)

    def _energy_cost_reduction(self) -> int:
        fokus    = 5 if "Fokus" in self.skills else 0
        mage_red = 5 if self.player_class == "mage" else 0
        return fokus + mage_red

    def check_bleed(self) -> str:
        if self.bleed_stacks > 0:
            if getattr(self, "immune_to_bleed_poison", False):
                self.bleed_stacks = 0
                return ""
            specials = self.get_set_specials()
            if "stahl_bleed_immune" in specials:
                self.bleed_stacks = 0
                return ""
            damage = max(0, BLEED_DAMAGE - (1 if "panzer_bleed_reduce" in specials else 0))
            self.hp = max(0, self.hp - damage)
            self.bleed_stacks -= 1
            return f"{self.name} erleidet {damage} Schaden durch Blutung! ({self.bleed_stacks} Stacks verbleibend)"
        return ""

    def check_poison(self) -> str:
        if self.poison_stacks > 0:
            if getattr(self, "immune_to_bleed_poison", False):
                self.poison_stacks = 0
                return ""
            self.hp = max(0, self.hp - POISON_DAMAGE)
            self.poison_stacks -= 1
            return f"☠️  {self.name} erleidet {POISON_DAMAGE} Giftschaden! ({self.poison_stacks} Stacks verbleibend)"
        return ""

    def check_burn(self) -> str:
        if self.burn_stacks > 0:
            if getattr(self, "immune_to_bleed_poison", False):
                self.burn_stacks = 0
                return ""
            self.hp = max(0, self.hp - BURN_DAMAGE)
            self.burn_stacks -= 1
            return f"🔥 {self.name} erleidet {BURN_DAMAGE} Verbrennungsschaden! ({self.burn_stacks} Stacks verbleibend)"
        return ""

    @property
    def dodge_chance(self) -> float:
        specials = self.get_set_specials()
        chance = 0.0
        if "leder_dodge" in specials:
            chance += 0.10
        if "schattentuch_dodge" in specials:
            chance += 0.15
        return chance

    def get_xp_bonus_mult(self) -> float:
        return 1.20 if "runen_xp_bonus" in self.get_set_specials() else 1.0

    def use_consumable(self, key: str) -> str:
        from content.loot_tables import CONSUMABLE_DEFS
        consumables = self.inventory.get("Consumables", {})
        if consumables.get(key, 0) <= 0:
            return f"Du hast kein(e) {key}!"
        cdef = CONSUMABLE_DEFS.get(key)
        if not cdef:
            return f"Unbekanntes Item: {key}"

        consumables[key] -= 1
        if consumables[key] == 0:
            del consumables[key]

        self.stats["potions_used"] += 1
        effect = cdef["effect"]
        value  = cdef.get("value", 0)
        emoji  = cdef.get("emoji", "🧪")

        if effect == "heal":
            healed = min(value, self.max_hp - self.hp)
            self.hp = min(self.max_hp, self.hp + value)
            return f"{emoji} {self.name} benutzt {key} und heilt {healed} HP! (HP: {self.hp}/{self.max_hp})"
        elif effect == "energy":
            eff_max = self.get_effective_max_energy()
            gained = min(value, eff_max - self.energy)
            self.energy = min(eff_max, self.energy + value)
            return f"{emoji} {self.name} benutzt {key} und erhält {gained} Energie! (Energie: {self.energy}/{eff_max})"
        elif effect == "attack":
            self.combat_modifiers["attack"] = self.combat_modifiers.get("attack", 0) + value
            return f"{emoji} {self.name} benutzt {key}! ATK +{value} für diesen Kampf. (ATK: {self.get_total_attack()})"
        elif effect == "cleanse":
            msgs = []
            if value > 0:
                healed = min(value, self.max_hp - self.hp)
                self.hp = min(self.max_hp, self.hp + value)
                msgs.append(f"heilt {healed} HP")
            if self.bleed_stacks > 0:
                self.bleed_stacks = 0
                msgs.append("Blutung entfernt")
            if self.poison_stacks > 0:
                self.poison_stacks = 0
                msgs.append("Gift entfernt")
            if self.burn_stacks > 0:
                self.burn_stacks = 0
                msgs.append("Verbrennung entfernt")
            if not msgs:
                msgs.append("keine Statuseffekte vorhanden")
            return f"{emoji} {self.name} benutzt {key}! " + ", ".join(msgs) + "."
        return f"{emoji} {self.name} benutzt {key}."

    # ── Serialisierung ────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialisiert den Spieler vollständig als JSON-kompatibles Dict."""
        return {
            "name":                   self.name,
            "hp":                     self.hp,
            "max_hp":                 self.max_hp,
            "attack":                 self.attack,
            "min_attack":             self.min_attack,
            "armor":                  self.armor,
            "level":                  self.level,
            "xp":                     self.xp,
            "xp_to_level_up":         self.xp_to_level_up,
            "energy":                 self.energy,
            "max_energy":             self.max_energy,
            "inventory":              self.inventory,
            "equipment":              self.equipment,
            "stats":                  self.stats,
            "difficulty":             self.difficulty,
            "skill_points":           self.skill_points,
            "skills":                 list(self.skills),
            "shield_ready":           self.shield_ready,
            "equipment_upgrades":     self.equipment_upgrades,
            "fights_until_event":     self.fights_until_event,
            "next_fight_xp_mult":     self.next_fight_xp_mult,
            "achievements":           list(self.achievements),
            "player_class":           self.player_class,
            "current_zone":           self.current_zone,
            "passive_crit_bonus":     self.passive_crit_bonus,
            "schwarzmarkt_available": self.schwarzmarkt_available,
            "shop_stock":             self.shop_stock,
            "zone_progress":          self.zone_progress,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        """Erstellt einen Character aus einem gespeicherten Dict (save.py-Format)."""
        player = cls(data["name"], data["max_hp"], data["attack"])
        player.hp              = data["hp"]
        player.min_attack      = data["min_attack"]
        player.armor           = data["armor"]
        player.level           = data["level"]
        player.xp              = data["xp"]
        player.xp_to_level_up  = data["xp_to_level_up"]
        player.energy          = data["energy"]
        player.max_energy      = data["max_energy"]
        player.equipment       = data["equipment"]

        # Legacy: type-Feld sicherstellen
        _slot_types = {"weapon": "weapon", "chest": "chest", "head": "head", "feet": "feet"}
        for eq_slot, item in player.equipment.items():
            if "type" not in item:
                item["type"] = _slot_types[eq_slot]

        player.inventory   = data["inventory"]
        _default_stats = {
            "fights": 0, "kills": 0, "deaths": 0,
            "damage_dealt": 0, "damage_taken": 0,
            "gold_earned": 0, "potions_used": 0,
            "dungeons_completed": 0, "dungeons_fled": 0,
            "zone_kills": {}, "zones_cleared": [],
        }
        player.stats               = {**_default_stats, **data.get("stats", {})}
        player.difficulty          = data.get("difficulty", "normal")
        player.fights_until_event  = data.get("fights_until_event", 2)
        player.next_fight_xp_mult  = data.get("next_fight_xp_mult", 1.0)
        player.skill_points        = data.get("skill_points", 0)
        player.skills              = set(data.get("skills", []))
        player.shield_ready        = data.get("shield_ready", False)
        player.shield_active       = False
        _default_upgrades          = {"weapon": 0, "chest": 0, "head": 0, "feet": 0}
        player.equipment_upgrades  = {**_default_upgrades, **data.get("equipment_upgrades", {})}
        player.achievements        = set(data.get("achievements", []))
        player.player_class        = data.get("player_class", "warrior")
        player.current_zone        = data.get("current_zone", "wald")
        player.ability_cooldowns   = {"S": 0, "R": 0, "C": 0, "X": 0}
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
        player.zone_progress = {**_default_zp, **data.get("zone_progress", {})}
        return player
