from abc import ABC, abstractmethod
from .descriptors import BoundedStat

class Human:
    hp = BoundedStat("hp", 0, 500)
    mp = BoundedStat("mp", 0, 200)
    strength = BoundedStat("strength", 1, 100)
    agility = BoundedStat("agility", 1, 100)
    intellect = BoundedStat("intellect", 1, 100)

    def __init__(self, name, level, hp, mp, strength, agility, intellect):
        self.name = name
        self.level = level
        self.hp = hp
        self.mp = mp
        self.strength = strength
        self.agility = agility
        self.intellect = intellect

    @property
    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} (Level {self.level}) HP: {self.hp}, MP: {self.mp}"

class Character(Human, ABC):
    def __init__(self, name, level, hp, mp, strength, agility, intellect):
        super().__init__(name, level, hp, mp, strength, agility, intellect)

    @abstractmethod
    def basic_attack(self, target):
        pass

    @abstractmethod
    def use_skill(self, skill_name, target=None, allies=None):
        pass