import pytest
from characters.heroes import LukeSkywalker, MasterYoda, R2D2
from characters.boss import Boss
from battle.battle_engine import Battle


def test_battle_initialization():
    heroes = [LukeSkywalker(), MasterYoda(), R2D2()]
    boss = Boss()
    battle = Battle(heroes, boss)

    assert len(battle.heroes) == 3
    assert battle.boss.name == "Дарт Вейдер"
    assert battle.turn == 1
    assert battle.max_turns == 20


def test_turn_order_creation():
    from battle.turn_order import TurnOrder
    from characters.heroes import LukeSkywalker

    luke = LukeSkywalker()
    boss = Boss()

    turn_order = TurnOrder([luke, boss])
    turn_list = list(turn_order)

    assert len(turn_list) == 2
    assert all(char.is_alive for char in turn_list)


def test_victory_conditions():
    heroes = [LukeSkywalker()]
    boss = Boss()
    battle = Battle(heroes, boss)

    # Босс мертв - победа
    boss.hp = 0
    assert battle.check_victory() == True

    # Все герои мертвы - поражение
    boss.hp = 50
    heroes[0].hp = 0
    assert battle.check_victory() == True


def test_effect_application():
    from effects.effect_library import ShieldEffect

    luke = LukeSkywalker()
    shield = ShieldEffect(duration=2, value=25)

    initial_shield = getattr(luke, 'shield', 0)
    shield.on_apply(luke)
    assert luke.shield == initial_shield + 25

    shield.on_remove(luke)
    assert luke.shield == initial_shield