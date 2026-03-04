import random
from player import Character


class Zombie(Character):
    def __init__(self):
        super().__init__("Zombie", hp=20, attack=4)
        self.xp_value = 60
        self.armor = 2
        self.loot_table = {
            "Healing Potions": (0, 2),
            "Gold": (1, 5),
        }
        self.equipment_drop_chance = 0.1
        self.equipment_table = {
            "weapon": [("Sword", 2)],
            "chest": [("Armor", 1)]
        }


class Skeleton(Character):
    def __init__(self):
        super().__init__("Skelett", hp=12, attack=8)
        self.xp_value = 80
        self.armor = 1
        self.loot_table = {
            "Healing Potions": (0, 2),
            "Gold": (5, 15),
        }
        self.equipment_drop_chance = 0.2
        self.equipment_table = {
            "weapon": [("Iron Sword", 3)],
            "chest": [("Leather Armor", 2)]
        }


class Slime(Character):
    def __init__(self):
        super().__init__("Schleim", hp=8, attack=3)
        self.xp_value = 35
        self.armor = 0
        self.loot_table = {
            "Healing Potions": (0, 1),
            "Gold": (1, 3),
        }
        self.equipment_drop_chance = 0.05
        self.equipment_table = {
            "weapon": [("Slime Club", 1)],
            "chest": [("Slime Armor", 1)]
        }


class Goblin(Character):
    def __init__(self):
        super().__init__("Goblin", hp=10, attack=5)
        self.xp_value = 50
        self.armor = 1
        self.loot_table = {
            "Healing Potions": (0, 1),
            "Gold": (5, 15),
        }
        self.equipment_drop_chance = 0.15
        self.equipment_table = {
            "weapon": [("Dagger", 2)],
            "chest": [("Leather Armor", 1)]
        }


class Dragon(Character):
    def __init__(self):
        super().__init__("Drache", hp=50, attack=15)
        self.xp_value = 200
        self.armor = 7
        self.loot_table = {
            "Healing Potions": (2, 4),
            "Gold": (10, 25),
        }
        self.equipment_drop_chance = 0.3
        self.equipment_table = {
            "weapon": [("Dragon Tooth", 10)],
            "chest": [("Dragon Hide", 5)]
        }
