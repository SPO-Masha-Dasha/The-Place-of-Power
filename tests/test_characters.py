import pytest
from characters.heroes import LukeSkywalker, MasterYoda, R2D2
from characters.boss import Boss
from core.exceptions import NotEnoughResourceError, SkillOnCooldownError, CharacterDeadError


def test_luke_basic_attack_and_hp():
    luke = LukeSkywalker()
    enemy = Boss()
    initial_hp = enemy.hp
    luke.basic_attack(enemy)
    assert enemy.hp < initial_hp


def test_luke_skill_cooldown_and_mp():
    luke = LukeSkywalker()
    enemy = Boss()

    # Использовать силовой толчок
    luke.use_skill("силовой толчок", enemy)
    with pytest.raises(SkillOnCooldownError):
        luke.use_skill("силовой толчок", enemy)

    # Если mp недостаточно
    luke.mp = 0
    with pytest.raises(NotEnoughResourceError):
        luke.use_skill("силовой щит", enemy)


def test_yoda_mind_confuse_and_debuff():
    yoda = MasterYoda()
    enemy = Boss()
    initial_int = enemy.intellect
    yoda.use_skill("запутывание разума", enemy, allies=None)
    # Дебафф интеллекта применяется
    assert enemy.intellect <= initial_int


def test_r2d2_shock_and_repair():
    r2 = R2D2()
    enemy = Boss()

    # Сила удара должна уменьшить HP
    r2.use_skill("электрошок", enemy)
    assert enemy.hp < 150

    # Ремонт восстанавливает собственное HP
    r2.hp = 10
    r2.use_skill("экстренный ремонт", enemy)
    assert r2.hp > 10


def test_boss_phase_switching():
    boss = Boss()
    boss.hp = 80  # Чуть больше половины
    boss.update_phase()
    assert boss.phase == 2

    boss.hp = 30
    boss.update_phase()
    assert boss.phase >= 3


def test_character_dead_error():
    luke = LukeSkywalker()
    enemy = Boss()
    luke.hp = 0

    with pytest.raises(CharacterDeadError):
        luke.basic_attack(enemy)


def test_bounded_stat_limits():
    from core.base_models import Human

    human = Human("Test", 1, 600, 300, 150, 150, 150)  # Значения выше максимума
    assert human.hp == 500  # Должно ограничиться
    assert human.mp == 200  # Должно ограничиться
    assert human.strength == 100  # Должно ограничиться