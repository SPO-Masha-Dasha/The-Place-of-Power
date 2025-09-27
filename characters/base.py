from core.base_models import Character
from core.exceptions import NotEnoughResourceError, SkillOnCooldownError, CharacterDeadError
from core.mixins import CritMixin, LoggerMixin


class BaseCharacter(Character, CritMixin, LoggerMixin):
    def __init__(self, name, level, hp, mp, strength, agility, intellect):
        super().__init__(name, level, hp, mp, strength, agility, intellect)
        self.cooldowns = {}  # {skill_name: turns_left}
        self.effects = []
        self.shield = 0  # Защита от щитов
        self.stunned = False  # Флаг оглушения

    def reduce_cooldowns(self):
        for skill in list(self.cooldowns.keys()):
            self.cooldowns[skill] -= 1
            if self.cooldowns[skill] <= 0:
                del self.cooldowns[skill]

    def apply_effects(self):
        # Уменьшаем длительность эффектов и применяем их
        effects_to_remove = []
        for effect in self.effects:
            effect.duration -= 1
            effect.on_turn_start(self)
            if effect.duration <= 0:
                effects_to_remove.append(effect)

        # Удаляем завершившиеся эффекты
        for effect in effects_to_remove:
            effect.on_remove(self)
            self.effects.remove(effect)

    def basic_attack(self, target):
        if not self.is_alive:
            raise CharacterDeadError(f"{self.name} мёртв и не может атаковать")

        if not target.is_alive:
            raise CharacterDeadError(f"Цель {target.name} уже мертва")

        base_damage = self.strength * 2
        damage, crit = self.calculate_damage(base_damage)

        # Учитываем щит цели
        if target.shield > 0:
            shield_mitigation = min(target.shield, damage)
            damage -= shield_mitigation
            target.shield -= shield_mitigation

        target.hp -= damage
        crit_msg = " Критический удар!" if crit else ""
        self.log(f"{self.name} атакует {target.name} и наносит {damage} урона.{crit_msg}")

    def use_skill(self, skill_name, target=None, allies=None):
        raise NotImplementedError("Метод use_skill должен быть реализован в подклассе")
