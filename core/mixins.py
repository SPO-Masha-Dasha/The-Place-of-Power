import random

class CritMixin:
    crit_chance = 0.1
    crit_multiplier = 2

    def calculate_damage(self, base_damage):
        if random.random() < self.crit_chance:
            return int(base_damage * self.crit_multiplier), True
        return base_damage, False

class LoggerMixin:
    def log(self, message):
        print(message)