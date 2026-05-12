import random

MAX_INVENTORY_SLOTS = 30  # Jeder einzigartige Stapel (Consumable/Junk) + jedes Equipment = 1 Slot


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
        self.energy_regen = 3

        # Temporäre Kampf-Boni – werden nach dem Kampf zurückgesetzt
        self.combat_modifiers = {"attack": 0}

        # Boss-Status-Effekte (nur während Kampf aktiv)
        self.stunned       = False
        self.poison_stacks = 0
        self.armor_debuff  = 0

        self.difficulty          = "normal"
        self.next_fight_xp_mult  = 1.0
        self.fights_until_event  = random.randint(2, 3)

        self.skill_points  = 0
        self.skills        = set()
        self.shield_ready  = False
        self.shield_active = False

        self.equipment_upgrades = {"weapon": 0, "chest": 0, "head": 0, "feet": 0}

        self.ng_plus      = 0
        self.achievements = set()

        self.player_class        = "warrior"
        self.class_ability_used  = False
        self.class_ability2_used      = False
        self.class_ability3_used      = False
        self.block_next               = False
        self.block_charges            = 0
        self.shadow_strike_ready      = False
        self.shadow_recharge_countdown = 0
        self.mana_shield_active       = False
        self.arcane_charges_remaining = 1
        self.passive_crit_bonus       = 0.0

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
        upgrade_bonus = self.equipment_upgrades.get("weapon", 0) * 2
        set_bonus     = self.get_set_bonus()["atk"]
        return self.attack + self.equipment["weapon"]["attack"] + self.combat_modifiers.get("attack", 0) + skill_bonus + upgrade_bonus + set_bonus

    def reset_combat_modifiers(self):
        """Setzt alle temporären Kampfboni zurück. Nach jedem Kampf aufrufen."""
        self.combat_modifiers    = {"attack": 0}
        self.stunned             = False
        self.poison_stacks       = 0
        self.armor_debuff        = 0
        self.shield_active       = False
        self.block_next          = False
        self.shadow_strike_ready = False
        self.mana_shield_active       = False
        self.block_charges            = 0
        self.shadow_recharge_countdown = 0
        self.arcane_charges_remaining = 1
        self.class_ability_used  = False
        self.class_ability2_used = False
        self.class_ability3_used = False

    def get_total_armor(self):
        skill_bonus = 3 if "Eisenhaut" in self.skills else 0
        upgrade_def = self.equipment_upgrades.get("chest", 0) + self.equipment_upgrades.get("head", 0) + self.equipment_upgrades.get("feet", 0)
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
        2: ("Cleave (C)",            "10 Energie – Angriff + 3 Blutungsstacks"),
        3: ("Rundumschlag (R)",      "15 Energie – Trifft alle Gegner"),
        4: ("Klassen-Fähigkeit [1]", "Klassenspezifisch – Taste [1] im Kampf"),
        5: ("Himmelsschlag (S)",     "20 Energie – Starker Einzelangriff +5 Schaden"),
        7: ("Klassen-Fähigkeit [2]", "Klassenspezifisch – Taste [2] im Kampf"),
    }

    def check_level_up(self):
        # Dynamischer XP-Multiplikator: frühe Level schnell, spätere langsamer
        # Lvl 1→2: 30 XP (~1 Kampf), 2→3: ~60, 3→4: ~110, danach ×1.7 pro Stufe
        XP_MULTIPLIERS = {1: 2.0, 2: 1.85, 3: 1.75, 4: 1.7, 5: 1.65, 6: 1.6, 7: 1.55, 8: 1.5, 9: 1.5}
        while self.xp >= self.xp_to_level_up:
            self.level += 1
            self.xp -= self.xp_to_level_up
            mult = XP_MULTIPLIERS.get(self.level - 1, 1.6)
            self.xp_to_level_up = int(self.xp_to_level_up * mult)
            self.max_hp  += 4
            self.hp       = self.max_hp
            self.attack  += 1
            self.min_attack += 1
            self.skill_points += 1
            print(f"✨ {self.name} ist nun Level {self.level}!")
            print(f"   +1 Skillpunkt! (Gesamt: {self.skill_points})")
            if self.level in self.SKILL_UNLOCKS:
                skill_name, skill_desc = self.SKILL_UNLOCKS[self.level]
                print(f"🔓 Neue Fähigkeit freigeschaltet: {skill_name}")
                print(f"   → {skill_desc}")
            # Passive Klassen-Skalierung
            if self.player_class == "warrior" and self.level % 2 == 0:
                self.armor += 1
                print(f"⚔️  Krieger-Passiv: +1 Rüstung durch Kampferfahrung! (Rüstung: {self.armor})")
            elif self.player_class == "mage" and self.level % 2 == 0:
                self.max_energy += 5
                print(f"🔮 Magier-Passiv: +5 max. Energie durch Magiestudium! (Max. Energie: {self.max_energy})")
            elif self.player_class == "rogue" and self.level % 3 == 0:
                self.passive_crit_bonus += 0.05
                pct = int((0.15 + self.passive_crit_bonus) * 100)
                print(f"🗡️  Schurken-Passiv: +5% Krit-Chance durch Präzision! (Krit: {pct}%)")

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
            set_crit    = 0.15 if "rogue_shadow_regen" in self.get_set_specials() else 0.0
            rogue_bonus = (0.10 + self.passive_crit_bonus + set_crit) if self.player_class == "rogue" else 0
            base_crit   = 0.15 if "Kritischer Treffer" in self.skills else 0
            if random.random() < (base_crit + rogue_bonus):
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
        mage_bonus  = 3 if self.player_class == "mage" else 0
        energy_gain = self.energy_regen + (2 if "Energiefluss" in self.skills else 0) + mage_bonus
        self.energy = min(self.get_effective_max_energy(), self.energy + energy_gain)
        msgs = [f"{self.name} regeneriert {energy_gain} Energie."]
        if "Regeneration" in self.skills:
            hp_gain  = 1
            self.hp  = min(self.max_hp, self.hp + hp_gain)
            msgs.append(f"+{hp_gain} HP durch Regeneration. (HP: {self.hp}/{self.max_hp})")
        return " ".join(msgs)

    def _energy_cost_reduction(self) -> int:
        fokus    = 5 if "Fokus" in self.skills else 0
        mage_red = 5 if self.player_class == "mage" else 0
        return fokus + mage_red

    def heavenstrike(self, target):
        cost = max(5, 20 - self._energy_cost_reduction())
        if self.energy >= cost:
            raw_damage  = random.randint(self.get_effective_min_attack(), self.get_total_attack()) + 5
            real_damage = self.apply_armor_reduction(raw_damage, target.get_total_armor())
            target.hp = max(0, target.hp - real_damage)
            self.energy -= cost
            return f"{self.name} führt einen Himmelsschlag aus und macht {real_damage} Schaden!"
        return f"{self.name} hat nicht genug Energie für einen Himmelsschlag!"

    def whirlwind(self, enemy_list):
        cost = max(5, 15 - self._energy_cost_reduction())
        if self.energy >= cost:
            self.energy -= cost
            results = []
            for enemy in enemy_list:
                raw_damage  = max(1, random.randint(self.get_effective_min_attack(), self.get_total_attack()) - 2)
                real_damage = self.apply_armor_reduction(raw_damage, enemy.get_total_armor())
                enemy.hp = max(0, enemy.hp - real_damage)
                results.append(f"{enemy.name} (-{real_damage} HP)")
            return f"🌪️ {self.name} wirbelt herum!\n" + ", ".join(results)
        return "Nicht genug Energie!"

    def cleave(self, target):
        cost = max(5, 10 - self._energy_cost_reduction())
        if self.energy >= cost:
            self.energy -= cost
            raw_damage  = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            real_damage = self.apply_armor_reduction(raw_damage, target.get_total_armor())
            target.hp = max(0, target.hp - real_damage)
            target.bleed_stacks += 3
            return f"{self.name} führt einen Cleave aus und macht {real_damage} Schaden! {target.name} erhält 3 Blutungsstacks!"
        return "Nicht genug Energie!"

    def check_bleed(self) -> str:
        if self.bleed_stacks > 0:
            damage = 3
            self.hp = max(0, self.hp - damage)
            self.bleed_stacks -= 1
            return f"{self.name} erleidet {damage} Schaden durch Blutung! ({self.bleed_stacks} Stacks verbleibend)"
        return ""

    def check_poison(self) -> str:
        if self.poison_stacks > 0:
            damage = 5
            self.hp = max(0, self.hp - damage)
            self.poison_stacks -= 1
            return f"☠️  {self.name} erleidet {damage} Giftschaden! ({self.poison_stacks} Stacks verbleibend)"
        return ""

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
            gained = min(value, self.max_energy - self.energy)
            self.energy = min(self.max_energy, self.energy + value)
            return f"{emoji} {self.name} benutzt {key} und erhält {gained} Energie! (Energie: {self.energy}/{self.max_energy})"
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
            if not msgs:
                msgs.append("keine Statuseffekte vorhanden")
            return f"{emoji} {self.name} benutzt {key}! " + ", ".join(msgs) + "."
        return f"{emoji} {self.name} benutzt {key}."

    # ── Neue Klassen-Fähigkeiten (Level 4 + 7) ──────────────────

    def shield_bash(self, target):
        """Krieger Lv4: Angriff + 50% Betäubungs-Chance"""
        cost = 15
        if self.energy < cost:
            return f"Nicht genug Energie! ({self.energy}/{cost})", 0
        self.energy -= cost
        raw = random.randint(self.get_effective_min_attack(), self.get_total_attack())
        dmg = self.apply_armor_reduction(raw, target.get_total_armor())
        target.hp = max(0, target.hp - dmg)
        if random.random() < 0.50:
            target.stunned = True
            return f"🛡️  Schildstoß! {dmg} Schaden — {target.name} ist betäubt!", dmg
        return f"🛡️  Schildstoß! {dmg} Schaden.", dmg

    def warcry(self):
        """Krieger Lv7: +5 ATK für diesen Kampf"""
        cost = 20
        if self.energy < cost:
            return f"Nicht genug Energie! ({self.energy}/{cost})"
        self.energy -= cost
        self.combat_modifiers["attack"] = self.combat_modifiers.get("attack", 0) + 5
        return f"⚔️  Kriegsschrei! +5 ATK für diesen Kampf. (ATK: {self.get_total_attack()})"

    def poison_blade(self, target):
        """Schurke Lv4: Angriff + 3 Giftstacks garantiert"""
        cost = 12
        if self.energy < cost:
            return f"Nicht genug Energie! ({self.energy}/{cost})", 0
        self.energy -= cost
        raw = random.randint(self.get_effective_min_attack(), self.get_total_attack())
        dmg = self.apply_armor_reduction(raw, target.get_total_armor())
        target.hp = max(0, target.hp - dmg)
        target.poison_stacks = getattr(target, "poison_stacks", 0) + 3
        return f"🗡️  Giftklinge! {dmg} Schaden + 3 Giftstacks auf {target.name}!", dmg

    def frost_ray(self, target):
        """Magier Lv4: 15-25 Schaden (ignoriert DEF) + Betäubung"""
        cost = 18
        if self.energy < cost:
            return f"Nicht genug Energie! ({self.energy}/{cost})", 0
        self.energy -= cost
        dmg = random.randint(15, 25)
        target.hp = max(0, target.hp - dmg)
        target.stunned = True
        return f"❄️  Froststrahl! {dmg} Eisschaden (ignoriert DEF) — {target.name} ist eingefroren!", dmg

    def activate_mana_shield(self):
        """Magier Lv7: Absorbiert nächsten Angriff mit Energie statt HP"""
        self.mana_shield_active = True
        return "🔮 Mana-Schild aktiviert! Nächster Angriff wird durch Energie absorbiert."

    def start_ng_plus(self):
        from content.loot_tables import EQUIPMENT_DEFS
        from config import DIFFICULTY_SETTINGS

        self.ng_plus += 1

        # Legendäre Items aus Inventar und Ausrüstung behalten
        kept_equip = [
            item for item in self.inventory["Equipment"]
            if EQUIPMENT_DEFS.get(item["name"], {}).get("rarity") == "legendary"
        ]
        kept_gold = self.inventory["Gold"]
        kept_achievements = self.achievements

        # Reset auf Level-1-Werte
        start_hp = DIFFICULTY_SETTINGS.get(self.difficulty, {}).get("start_hp", 30)
        self.max_hp        = start_hp
        self.hp            = start_hp
        self.attack        = 10
        self.min_attack    = 1
        self.level         = 1
        self.xp            = 0
        self.xp_to_level_up = 30
        self.energy        = 15
        self.bleed_stacks  = 0
        self.combat_modifiers = {"attack": 0}

        # Ausrüstung zurücksetzen
        self.equipment = {
            "weapon": {"name": "Fäuste",       "attack": 0, "type": "weapon"},
            "chest":  {"name": "Lumpen",        "armor": 0, "type": "chest"},
            "head":   {"name": "Kein Helm",     "armor": 0, "type": "head"},
            "feet":   {"name": "Keine Schuhe",  "armor": 0, "type": "feet"},
        }
        self.equipment_upgrades = {"weapon": 0, "chest": 0, "head": 0, "feet": 0}

        # Inventar zurücksetzen, Gold + Legendaries behalten
        self.inventory = {
            "Consumables": {"Healing Potion": 2},
            "Junk":        {},
            "Gold":        kept_gold,
            "Equipment":   kept_equip,
        }

        # Skills zurücksetzen
        self.skill_points  = 0
        self.skills        = set()
        self.shield_ready  = False
        self.shield_active = False

        # Events und XP-Buff zurücksetzen
        self.next_fight_xp_mult = 1.0
        self.fights_until_event = random.randint(2, 3)

        # Achievements behalten
        self.achievements = kept_achievements

        # Zone + Shop zurücksetzen
        self.current_zone           = "wald"
        self.schwarzmarkt_available = True
        self.shop_stock             = []
        self.zone_progress = {
            zid: {"dungeons_completed": 0, "boss_defeated": False}
            for zid in ["wald", "ruinen", "wueste", "vulkan", "dunkelreich"]
        }

        # Klassen-Boni neu anwenden (Werte kommen aus apply_class)
        from content.classes import apply_class
        apply_class(self, self.player_class)

