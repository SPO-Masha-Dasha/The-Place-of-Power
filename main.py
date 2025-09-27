#!/usr/bin/env python3
"""
Главный файл для запуска игры "The Place of Power"
"""

from characters.heroes import LukeSkywalker, MasterYoda, R2D2
from characters.boss import Boss
from battle.battle_engine import Battle
from items.item_library import magic_word, auto_exam


def main():
    print("Добро пожаловать в игру 'The Place of Power'!")
    print("=" * 50)

    # Создание героев
    print("Создаем команду героев...")
    luke = LukeSkywalker()
    yoda = MasterYoda()
    r2d2 = R2D2()

    party = [luke, yoda, r2d2]

    # Показываем информацию о героях
    print("\n Ваша команда:")
    for hero in party:
        print(f"  - {hero.name}: HP {hero.hp}, MP {hero.mp}, Сила {hero.strength}")

    # Создание босса
    print("\n Подготовка босса...")
    vader = Boss()
    print(f"  - {vader.name}: HP {vader.hp}, MP {vader.mp}, Сила {vader.strength}")

    # Начальные предметы
    inventory = [magic_word, auto_exam]
    print(f"\n Вам доступны предметы: {', '.join(item.name for item in inventory)}")

    # Запуск битвы
    print("\n Начинаем битву!")
    print("=" * 50)

    battle = Battle(party, vader, inventory)
    battle.start()

    print("\n" + "=" * 50)
    print("Игра завершена. Спасибо за игру!")


if __name__ == "__main__":
    main()