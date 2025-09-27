from .base import BaseCharacter
from core.exceptions import NotEnoughResourceError, SkillOnCooldownError
from effects.effect_library import ShieldEffect, StatDebuff, StunEffect
import random


class LukeSkywalker(BaseCharacter):
    def __init__(self):
        super().__init__(
            name="Люк Скайуокер",
            level=1,
            hp=120,
            mp=80,
            strength=15,
            agility=20,
            intellect=15
        )
        self.max_mp = 80

    def use_skill(self, skill_name, target=None, allies=None):
        skill_name = skill_name.lower()

        if skill_name == "силовой толчок":
            if self.mp < 15:
                raise NotEnoughResourceError("Недостаточно MP для силового толчка")
            if "силовой толчок" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            damage = 25 + (self.strength // 2)
            # Учитываем щит цели
            actual_damage = damage
            if target.shield > 0:
                shield_mitigation = min(target.shield, damage)
                actual_damage -= shield_mitigation
                target.shield -= shield_mitigation

            target.hp -= actual_damage
            self.mp -= 15
            self.cooldowns["силовой толчок"] = 1
            self.log(f"{self.name} использует Силовой толчок и наносит {actual_damage} урона {target.name}")

        elif skill_name == "силовой щит":
            if self.mp < 20:
                raise NotEnoughResourceError("Недостаточно MP для силового щита")
            if "силовой щит" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            self.mp -= 20
            self.cooldowns["силовой щит"] = 2
            shield_effect = ShieldEffect(duration=2, value=25)
            self.effects.append(shield_effect)
            self.log(f"{self.name} активирует Силовой щит (+25 защиты на 2 хода)")

        elif skill_name == "исцеление":
            if self.mp < 25:
                raise NotEnoughResourceError("Недостаточно MP для исцеления")
            if "исцеление" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            heal_amount = 40
            self.hp = min(self.hp + heal_amount, 120)  # Не превышаем максимальное HP
            self.mp -= 25
            self.cooldowns["исцеление"] = 3
            self.log(f"{self.name} исцеляется на {heal_amount} HP")

        else:
            self.log(f"{self.name} пытается использовать неизвестный скилл {skill_name}")


class MasterYoda(BaseCharacter):
    def __init__(self):
        super().__init__(
            name="Мастер Йода",
            level=1,
            hp=80,
            mp=120,
            strength=10,
            agility=25,
            intellect=30
        )
        self.accuracy = 70  # %
        self.max_mp = 120

    def use_skill(self, skill_name, target=None, allies=None):
        skill_name = skill_name.lower()

        if skill_name == "запутывание разума":
            if self.mp < 20:
                raise NotEnoughResourceError("Недостаточно MP")
            if "запутывание разума" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            damage = 15 + (self.intellect // 2)
            # Учитываем щит цели
            actual_damage = damage
            if target.shield > 0:
                shield_mitigation = min(target.shield, damage)
                actual_damage -= shield_mitigation
                target.shield -= shield_mitigation

            target.hp -= actual_damage
            self.mp -= 20
            self.cooldowns["запутывание разума"] = 1

            # Применяем дебафф интеллекта
            debuff = StatDebuff(stat='intellect', amount=15, duration=2)
            target.effects.append(debuff)
            self.log(
                f"{self.name} использует Запутывание разума --- {target.name} получает {actual_damage} урона и -15 интеллекта на 2 хода")


        elif skill_name == "мудрость силы":
            if self.mp < 30:
                raise NotEnoughResourceError("Недостаточно MP")
            if "мудрость силы" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            if allies is None:
                allies = []

            for ally in allies:
                if ally.is_alive:
                    heal = 40
                    ally.hp = min(ally.hp + heal, getattr(ally, 'max_hp', ally.hp + heal))
                    # Снимаем негативные эффекты
                    ally.effects = [e for e in ally.effects if e.name not in ["яд", "горение"]]
                    self.log(f"{self.name} исцеляет {ally.name} на {heal} HP и снимает негативные эффекты")

            self.mp -= 30
            self.cooldowns["мудрость силы"] = 3

        elif skill_name == "вдохновение союзников":
            if self.mp < 25:
                raise NotEnoughResourceError("Недостаточно MP")
            if "вдохновение союзников" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            if allies is None:
                allies = []

            for ally in allies:
                if ally.is_alive:
                    shield_effect = ShieldEffect(duration=3, value=15)
                    ally.effects.append(shield_effect)
                    self.log(f"{self.name} вдохновляет {ally.name} (+15 защиты на 3 хода)")

            self.mp -= 25
            self.cooldowns["вдохновение союзников"] = 3

        else:
            self.log(f"{self.name} пытается использовать неизвестный скилл {skill_name}")


class R2D2(BaseCharacter):
    def __init__(self):
        super().__init__(
            name="R2-D2",
            level=1,
            hp=80,
            mp=0,
            strength=25,
            agility=18,
            intellect=10
        )
        self.energy = 100
        self.max_energy = 100

    def regenerate_energy(self):
        self.energy = min(self.max_energy, self.energy + 10)

    def use_skill(self, skill_name, target=None, allies=None):
        skill_name = skill_name.lower()

        if skill_name == "электрошок":
            if self.energy < 30:
                raise NotEnoughResourceError("Недостаточно энергии")

            damage = 30 + (self.strength // 2)
            # Учитываем щит цели
            actual_damage = damage
            if target.shield > 0:
                shield_mitigation = min(target.shield, damage)
                actual_damage -= shield_mitigation
                target.shield -= shield_mitigation

            target.hp -= actual_damage
            stunned = random.random() < 0.2

            if stunned:
                stun_effect = StunEffect(duration=1)
                target.effects.append(stun_effect)
                self.log(f"{self.name} электрошокирует {target.name} на {actual_damage} урона и оглушает!")
            else:
                self.log(f"{self.name} наносит {actual_damage} урона {target.name} электрошоком.")

            self.energy -= 30

        elif skill_name == "экстренный ремонт":
            if self.energy < 40:
                raise NotEnoughResourceError("Недостаточно энергии")
            if "экстренный ремонт" in self.cooldowns:
                raise SkillOnCooldownError("Скилл на перезарядке")

            heal = 15
            self.hp = min(self.hp + heal, 80)  # Не превышаем максимальное HP
            self.energy -= 40
            self.cooldowns["экстренный ремонт"] = 2
            self.log(f"{self.name} проводит экстренный ремонт и восстанавливает {heal} HP.")

        else:
            self.log(f"{self.name} пытается использовать неизвестный скилл {skill_name}")