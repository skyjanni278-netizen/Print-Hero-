import random

MAX_INVENTORY_SLOTS = 20  # Jeder einzigartige Stapel (Consumable/Junk) + jedes Equipment = 1 Slot


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

        self.equipment = {
            "weapon": {"name": "Fäuste",       "attack": 0},
            "chest":  {"name": "Lumpen",       "armor": 0},
            "head":   {"name": "Kein Helm",    "armor": 0},
            "feet":   {"name": "Keine Schuhe", "armor": 0},
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
        from loot_tables import CONSUMABLE_DEFS
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
        from loot_tables import CONSUMABLE_DEFS
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
    def get_total_attack(self):
        return self.attack + self.equipment["weapon"]["attack"]

    def get_total_armor(self):
        return (self.armor
                + self.equipment["chest"]["armor"]
                + self.equipment["head"]["armor"]
                + self.equipment["feet"]["armor"])

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
        2: ("Cleave (C)",       "10 Energie – Angriff + 3 Blutungsstacks"),
        3: ("Rundumschlag (R)", "15 Energie – Trifft alle Gegner"),
        5: ("Himmelsschlag (S)","20 Energie – Starker Einzelangriff +5 Schaden"),
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
            print(f"✨ {self.name} ist nun Level {self.level}!")
            if self.level in self.SKILL_UNLOCKS:
                skill_name, skill_desc = self.SKILL_UNLOCKS[self.level]
                print(f"🔓 Neue Fähigkeit freigeschaltet: {skill_name}")
                print(f"   → {skill_desc}")

    def is_alive(self):
        return self.hp > 0

    def attack_target(self, target):
        raw_damage  = random.randint(self.get_effective_min_attack(), self.get_total_attack())
        real_damage = self.apply_armor_reduction(raw_damage, target.get_total_armor())
        target.hp   = max(0, target.hp - real_damage)
        return f"{self.name} macht {real_damage} Schaden!"

    def try_flee(self):
        return random.randint(1, 20) >= 10

    def regenerate(self):
        self.energy = min(self.max_energy, self.energy + self.energy_regen)
        return f"{self.name} regeneriert {self.energy_regen} Energie."

    def heavenstrike(self, target):
        cost = 20
        if self.energy >= cost:
            raw_damage  = random.randint(self.get_effective_min_attack(), self.get_total_attack()) + 5
            real_damage = self.apply_armor_reduction(raw_damage, target.get_total_armor())
            target.hp = max(0, target.hp - real_damage)
            self.energy -= cost
            return f"{self.name} führt einen Himmelsschlag aus und macht {real_damage} Schaden!"
        return f"{self.name} hat nicht genug Energie für einen Himmelsschlag!"

    def whirlwind(self, enemy_list):
        cost = 15
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
        cost = 10
        if self.energy >= cost:
            self.energy -= cost
            raw_damage  = random.randint(self.get_effective_min_attack(), self.get_total_attack())
            real_damage = self.apply_armor_reduction(raw_damage, target.get_total_armor())
            target.hp = max(0, target.hp - real_damage)
            target.bleed_stacks = max(target.bleed_stacks, 3)
            return f"{self.name} führt einen Cleave aus und macht {real_damage} Schaden! {target.name} erhält {target.bleed_stacks} Blutungsstacks!"
        return "Nicht genug Energie!"

    def check_bleed(self):
        if self.bleed_stacks > 0:
            damage = 3
            self.hp = max(0, self.hp - damage)
            self.bleed_stacks -= 1
            return f"{self.name} erleidet {damage} Schaden durch Blutung!"

    def use_consumable(self, key: str) -> str:
        from loot_tables import CONSUMABLE_DEFS
        consumables = self.inventory.get("Consumables", {})
        if consumables.get(key, 0) <= 0:
            return f"Du hast kein(e) {key}!"
        cdef = CONSUMABLE_DEFS.get(key)
        if not cdef:
            return f"Unbekanntes Item: {key}"

        consumables[key] -= 1
        if consumables[key] == 0:
            del consumables[key]

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
            self.attack += value
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
            else:
                msgs.append("keine Blutung vorhanden")
            return f"{emoji} {self.name} benutzt {key}! " + ", ".join(msgs) + "."
        return f"{emoji} {self.name} benutzt {key}."

