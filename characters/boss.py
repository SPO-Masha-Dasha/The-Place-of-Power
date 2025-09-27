import random
from .base import BaseCharacter
from core.mixins import LoggerMixin
from effects.effect_library import ShieldEffect, SilenceEffect, StunEffect, FearEffect


class Boss(BaseCharacter, LoggerMixin):
    def __init__(self):
        super().__init__(
            name="Дарт Вейдер",
            level=10,
            hp=150,
            mp=100,
            strength=50,
            agility=15,
            intellect=30
        )
        self.max_hp = 150
        self.phase = 1
        self.perished = False
        self.reborn = False
        self.damage_multiplier = 1
        self.skip_next_turn = False

    def update_phase(self):
        previous_phase = self.phase
        hp_percent = (self.hp / self.max_hp) * 100

        if hp_percent > 60:
            self.phase = 1
        elif 41 <= hp_percent <= 60:
            self.phase = 2
        elif 21 <= hp_percent <= 40:
            self.phase = 3
        elif 11 <= hp_percent <= 20:
            self.phase = 4
        else:
            self.phase = 5

        if self.phase != previous_phase:
            self.log(f"Фаза изменена: {previous_phase} -> {self.phase} ({hp_percent:.2f}%)")

    def take_turn(self, targets, allies=None):
        self.update_phase()
        # Применяем эффекты к себе
        self.apply_effects()

        # Проверяем, должен ли босс пропустить ход
        if self.skip_next_turn:
            self.log(f"{self.name} пропускает ход из-за отвлечения!")
            self.skip_next_turn = False
            return

        # Проверяем оглушение
        if self.stunned:
            self.log(f"{self.name} пропускает ход --- он оглушён.")
            return

        # Если нет живых целей, пропустить
        living_targets = [t for t in targets if t.is_alive]
        if not living_targets:
            return

        target = random.choice(living_targets)

        # ФАЗА 1 --- Отрицание
        if self.phase == 1:
            choice = random.choice(["удушение", "штурмовик", "бафф"])
            if choice == "удушение":
                self.force_choke(target)
            elif choice == "штурмовик":
                self.summon_trooper(allies)
            else:  # "бафф"
                self.shield_up()

        # ФАЗА 2 --- Гнев
        elif self.phase == 2:
            choice = random.choice(["молния", "подавление", "поглощение"])
            if choice == "молния":
                self.force_lightning(targets)
            elif choice == "подавление":
                self.will_suppression(target)
            else:
                self.force_drain(target)

        # ФАЗЫ 3 и 4 --- Торг / Депрессия
        elif self.phase in (3, 4):
            choice = random.choice(["круг", "лечение", "страх"])
            if choice == "круг":
                self.circle_of_force(targets)
            elif choice == "лечение":
                self.self_heal()
            else:
                self.mass_fear(targets)

        # ФАЗА 5 --- Я твой отец
        elif self.phase == 5:
            choice = random.choice(["финал", "перерождение", "месть"])
            if choice == "финал" and not self.perished:
                self.final_flash(targets)
            elif choice == "перерождение" and not self.reborn:
                self.rebirth()
            else:
                self.vow_of_vengeance()

    # === Фаза 1 ===
    def force_choke(self, target):
        damage = 35 * self.damage_multiplier
        # Учитываем щит цели
        actual_damage = damage
        if target.shield > 0:
            shield_mitigation = min(target.shield, damage)
            actual_damage -= shield_mitigation
            target.shield -= shield_mitigation

        target.hp -= actual_damage
        self.log(f"{self.name} использует Силовое удушение --- {target.name} получает {actual_damage} урона.")

    def summon_trooper(self, allies):
        # Создаем простого штурмовика
        from .base import BaseCharacter
        trooper = BaseCharacter(name="Штурмовик", level=1, hp=50, mp=0, strength=10, agility=10, intellect=1)
        trooper.max_hp = 50

        if allies is not None:
            allies.append(trooper)
        self.log(f"{self.name} призывает Штурмовика (50 HP).")

    def shield_up(self):
        shield_effect = ShieldEffect(duration=2, value=20)
        self.effects.append(shield_effect)
        self.log(f"{self.name} активирует защиту: щит +20 на 2 хода.")

    # === Фаза 2 ===
    def force_lightning(self, targets):
        living_targets = [t for t in targets if t.is_alive]
        targets_to_hit = random.sample(living_targets, min(2, len(living_targets)))

        for target in targets_to_hit:
            damage = 45 * self.damage_multiplier
            # Учитываем щит цели
            actual_damage = damage
            if target.shield > 0:
                shield_mitigation = min(target.shield, damage)
                actual_damage -= shield_mitigation
                target.shield -= shield_mitigation

            target.hp -= actual_damage
            self.log(f"{self.name} наносит {actual_damage} урона {target.name} Молнией Силы.")

    def will_suppression(self, target):
        self.log(f"{self.name} накладывает немоту на {target.name} (2 хода).")
        silence_effect = SilenceEffect(duration=2)
        target.effects.append(silence_effect)

    def force_drain(self, target):
        amount = 20
        drained = min(target.mp, amount)
        target.mp -= drained
        self.mp += drained
        self.log(f"{self.name} поглощает {drained} MP у {target.name}.")

    # === Фазы 3,4 ===
    def circle_of_force(self, targets):
        damage = 60 * self.damage_multiplier
        for target in targets:
            if target.is_alive:
                # Учитываем щит цели
                actual_damage = damage
                if target.shield > 0:
                    shield_mitigation = min(target.shield, damage)
                    actual_damage -= shield_mitigation
                    target.shield -= shield_mitigation

                target.hp -= actual_damage
        self.log(f"{self.name} применяет Круг Силы --- {damage} урона всем.")

    def self_heal(self):
        heal = 50
        self.hp += heal
        self.max_hp -= 30
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.log(f"{self.name} исцеляется на {heal} HP, но теряет 30 от максимума HP.")

    def mass_fear(self, targets):
        for target in targets:
            if target.is_alive:
                fear_effect = FearEffect(duration=3)
                target.effects.append(fear_effect)
        self.log(f"{self.name} накладывает Страх на всех врагов.")

    # === Фаза 5 ===
    def final_flash(self, targets):
        damage = 100 * self.damage_multiplier
        for target in targets:
            if target.is_alive:
                # Учитываем щит цели
                actual_damage = damage
                if target.shield > 0:
                    shield_mitigation = min(target.shield, damage)
                    actual_damage -= shield_mitigation
                    target.shield -= shield_mitigation

                target.hp -= actual_damage

        self.perished = True
        self.hp = 0
        self.log(f"{self.name} использует Финальную вспышку! Все получают {damage} урона. {self.name} погибает!")

    def rebirth(self):
        if self.hp <= 0 and not self.reborn:
            self.hp = int(self.max_hp * 0.3)
            self.reborn = True
            self.log(f"{self.name} восстает с {self.hp} HP.")

    def vow_of_vengeance(self):
        self.damage_multiplier = 2
        self.log(f"{self.name} даёт Клятву мести --- урон ×2 теперь, но он получит больше урона.")