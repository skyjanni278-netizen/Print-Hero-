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
        self.xp_to_level_up = 100

        self.max_energy = 30
        self.energy = 15
        self.energy_regen = 3

        self.equipment = {
            "weapon": {"name": "Fäuste", "attack": 0},
            "chest":  {"name": "Lumpen", "armor": 0}
        }
        self.inventory = {
            "Consumables": {"Healing Potion": 2},
            "Junk":        {},   # {"Altes Seil": 3, ...}
            "Gold":        0,
            "Equipment":   []    # nicht stapelbar, 1 Slot pro Stück
        }

    # ── Inventar-Slot-Verwaltung ─────────────────────────────
    def inventory_count(self) -> int:
        """Belegte Slots: jeder einzigartige Consumable/Junk-Stapel + jedes Equipment-Stück."""
        c = len(self.inventory.get("Consumables", {}))
        j = len(self.inventory.get("Junk", {}))
        e = len(self.inventory.get("Equipment", []))
        return c + j + e

    def has_inventory_space(self) -> bool:
        return self.inventory_count() < MAX_INVENTORY_SLOTS

    def add_consumable(self, key: str, amount: int) -> int:
        """
        Fügt `amount` Einheiten eines Consumables hinzu.
        Berücksichtigt Stack-Limit und freie Slots.
        Gibt die tatsächlich hinzugefügte Menge zurück.
        """
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
        """True wenn mindestens 1 Einheit hinzugefügt werden kann."""
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
        """
        Junk hat kein Stack-Limit, aber braucht einen freien Slot für neue Typen.
        Gibt die tatsächlich hinzugefügte Menge zurück.
        """
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
        return self.armor + self.equipment["chest"]["armor"]

    def check_level_up(self):
        while self.xp >= self.xp_to_level_up:
            self.level += 1
            self.xp -= self.xp_to_level_up
            self.xp_to_level_up = int(self.xp_to_level_up * 1.5)
            self.max_hp  += 5
            self.hp       = self.max_hp
            self.attack  += 2
            self.min_attack += 1
            print(f"✨ {self.name} ist nun Level {self.level}!")

    def is_alive(self):
        return self.hp > 0

    def attack_target(self, target):
        base_damage = random.randint(self.min_attack, self.get_total_attack())
        real_damage = max(0, base_damage - target.get_total_armor())
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
            damage = random.randint(self.min_attack, self.attack) + 5
            target.hp = max(0, target.hp - damage)
            self.energy -= cost
            return f"{self.name} führt einen Himmelsschlag aus und macht {damage} Schaden!"
        return f"{self.name} hat nicht genug Energie für einen Himmelsschlag!"

    def whirlwind(self, enemy_list):
        cost = 15
        if self.energy >= cost:
            self.energy -= cost
            results = []
            for enemy in enemy_list:
                damage = max(1, random.randint(self.min_attack, self.attack) - 2)
                enemy.hp = max(0, enemy.hp - damage)
                results.append(f"{enemy.name} (-{damage} HP)")
            return f"🌪️ {self.name} wirbelt herum!\n" + ", ".join(results)
        return "Nicht genug Energie!"

    def cleave(self, target):
        cost = 10
        if self.energy >= cost:
            self.energy -= cost
            damage = random.randint(self.min_attack, self.attack)
            target.hp = max(0, target.hp - damage)
            target.bleed_stacks = max(target.bleed_stacks, 3)
            return f"{self.name} führt einen Cleave aus und macht {damage} Schaden! {target.name} erhält {target.bleed_stacks} Blutungsstacks!"
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

    def add_loot(self, item_name, amount):
        if item_name in self.inventory:
            self.inventory[item_name] += amount
        else:
            self.inventory[item_name] = amount
        print(f"{self.name} erhält {amount}x {item_name}!")
