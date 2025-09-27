from .turn_order import TurnOrder
from .logger import BattleLogger
from items.item_library import ITEMS
from core.exceptions import CharacterDeadError, NotEnoughResourceError, SkillOnCooldownError


class Battle:
    def __init__(self, heroes, boss, inventory=None, logger=None):
        self.heroes = heroes
        self.boss = boss
        self.allies = heroes.copy()
        self.enemies = [boss]
        self.turn = 1
        self.max_turns = 20
        self.inventory = inventory or []
        self.logger = logger or BattleLogger()
        self.battle_log = []

    def log(self, message):
        self.logger.log(message)
        self.battle_log.append(message)

    def apply_effects(self):
        """Применяет эффекты в начале раунда всем персонажам"""
        all_characters = self.allies + self.enemies

        for character in all_characters:
            if character.is_alive:
                character.apply_effects()
                character.reduce_cooldowns()

                # Регенерация энергии для R2-D2
                if hasattr(character, 'regenerate_energy'):
                    character.regenerate_energy()

    def remove_dead(self):
        """Удаляет мертвых персонажей из списков"""
        self.allies = [char for char in self.allies if char.is_alive]
        self.enemies = [char for char in self.enemies if char.is_alive]

    def check_victory(self):
        """Проверяет условия победы/поражения"""
        if not self.boss.is_alive:
            self.log("Победа! Босс повержен!")
            if self.turn <= self.max_turns:
                self.log("Бонус за быструю победу! (<= 20 раундов)")
            return True

        if not any(hero.is_alive for hero in self.heroes):
            self.log("Поражение... Все союзники мертвы.")
            return True

        if self.turn > self.max_turns:
            self.log("Превышено максимальное количество ходов! Поражение.")
            return True

        return False

    def player_action(self, hero):
        """Обрабатывает действие игрока"""
        if not hero.is_alive:
            return

        self.log(f"\n Ходит {hero.name} (HP: {hero.hp}, MP: {hero.mp})")
        self.log(f"Босс {self.boss.name}: HP {self.boss.hp}/{self.boss.max_hp}")

        # Определяем доступные способности для каждого героя
        skills_map = {
            "Люк Скайуокер": [
                "1. Силовой толчок (15 MP) - урон 25-40",
                "2. Силовой щит (20 MP) +25 защиты на 2 хода",
                "3. Исцеление (25 MP) +40 HP"
            ],
            "Мастер Йода": [
                "1. Запутывание разума (20 MP) - урон + дебафф",
                "2. Мудрость силы (30 MP) - лечение команды",
                "3. Вдохновение союзников (25 MP) + защита команды"
            ],
            "R2-D2": [
                "1. Электрошок (30 энергии) - урон + оглушение",
                "2. Экстренный ремонт (40 энергии) - самолечение"
            ]
        }

        skill_names_map = {
            "Люк Скайуокер": ["силовой толчок", "силовой щит", "исцеление"],
            "Мастер Йода": ["запутывание разума", "мудрость силы", "вдохновение союзников"],
            "R2-D2": ["электрошок", "экстренный ремонт"]
        }

        available_skills = skills_map.get(hero.name, [])
        available_skill_names = skill_names_map.get(hero.name, [])

        while True:
            self.log("Доступные действия:")
            self.log("1. Атака")
            self.log("2. Способность")
            self.log("3. Предмет")
            self.log("4. Пропуск")

            try:
                action = input("Выберите действие (1-4): ").strip()

                if action == "1":
                    hero.basic_attack(self.boss)
                    break

                elif action == "2":
                    if not available_skills:
                        self.log("У этого героя нет способностей.")
                        continue

                    self.log("Доступные способности:")
                    for skill_desc in available_skills:
                        self.log(f"   {skill_desc}")

                    skill_choice = input(f"Выберите номер способности (1-{len(available_skill_names)}): ").strip()

                    try:
                        skill_idx = int(skill_choice) - 1
                        if 0 <= skill_idx < len(available_skill_names):
                            skill_name = available_skill_names[skill_idx]
                            hero.use_skill(skill_name, self.boss, self.allies)
                            break
                        else:
                            self.log(f"Неверный номер способности. Выберите 1-{len(available_skill_names)}.")
                    except ValueError:
                        self.log(f"Введите число (1-{len(available_skill_names)}).")

                elif action == "3":
                    if not self.inventory:
                        self.log("У вас нет предметов.")
                        continue

                    self.log("Доступные предметы:")
                    for i, item in enumerate(self.inventory):
                        self.log(f"{i + 1}. {item.name} - {item.description}")

                    try:
                        idx = int(input("Выберите номер предмета: ")) - 1
                        if 0 <= idx < len(self.inventory):
                            item = self.inventory[idx]
                            item.use(hero, self.boss)
                            if item.one_time:
                                self.inventory.pop(idx)
                            break
                        else:
                            self.log("Неверный номер предмета.")
                    except ValueError:
                        self.log("Введите число.")

                elif action == "4":
                    self.log(f"{hero.name} пропускает ход.")
                    break

                else:
                    self.log("Неверное действие. Выберите 1-4.")

            except (NotEnoughResourceError, SkillOnCooldownError, CharacterDeadError) as e:
                self.log(f"Ошибка: {e}")
            except Exception as e:
                self.log(f"Неожиданная ошибка: {e}")

    def boss_action(self):
        """Обрабатывает ход босса"""
        if self.boss.skip_next_turn:
            self.log(f" {self.boss.name} отвлечён и пропускает ход!")
            self.boss.skip_next_turn = False
            return

        self.boss.take_turn(self.allies, self.heroes)

    def start(self):
        """Запускает основной цикл боя"""
        self.log("Битва начинается!")
        self.log(f"Герои против {self.boss.name}!")

        # Определяем название фазы
        phase_names = {
            1: "ФАЗА 1 - ОТРИЦАНИE",
            2: "ФАЗА 2 - ГНЕВ",
            3: "ФАЗА 3 - ТОРГ",
            4: "ФАЗА 4 - ДЕПРЕССИЯ",
            5: "ФАЗА 5 - ЛЮК, Я ТВОЙ ОТЕЦ"
        }

        self.boss.update_phase()
        previous_phase = self.boss.phase

        while True:
            # Применяем эффекты в начале раунда
            self.apply_effects()
            self.boss.update_phase()

            phase_name = phase_names.get(self.boss.phase, f"Раунд {self.turn}")
            self.log(f"\n{'═' * 50}")
            self.log(f"{phase_name} | Раунд {self.turn} | Босс: HP {self.boss.hp}/{self.boss.max_hp}")
            self.log(f"{'═' * 50}")


            # Определяем порядок ходов
            turn_order = TurnOrder(self.allies + self.enemies)

            # Обрабатываем ходы каждого персонажа
            for unit in turn_order:
                if not unit.is_alive:
                    continue

                if unit in self.allies:
                    self.player_action(unit)
                else:
                    self.boss_action()

                self.boss.update_phase()
                if self.boss.phase != previous_phase:
                    previous_phase = self.boss.phase
                    phase_name = phase_names.get(self.boss.phase, f"Фаза {self.boss.phase}")
                    self.log(f"\n{'═' * 50}")
                    self.log(f"{phase_name} | Раунд {self.turn} | Босс: HP {self.boss.hp}/{self.boss.max_hp}")
                    self.log(f"{'═' * 50}")

                # Проверяем условия победы после каждого хода
                self.remove_dead()
                if self.check_victory():
                    self.log("\n Битва завершена!")
                    return

            self.turn += 1

            if self.turn > self.max_turns:
                self.log("Превышено максимальное количество ходов!")
                break
