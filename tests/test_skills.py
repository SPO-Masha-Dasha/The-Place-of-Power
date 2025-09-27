import pytest
from skills.skill_library import Skills
from effects.effect_library import ShieldEffect, StunEffect, StatDebuff


def test_skill_library_entries():
    # Проверка, что навыки настроены
    luke_sk = Skills["Luke"]["силовой толчок"]
    assert luke_sk.name == "силовой толчок"
    assert luke_sk.cost == 15

    yoda_sk = Skills["Yoda"]["мудрость силы"]
    assert yoda_sk.name == "мудрость силы"
    assert yoda_sk.cost == 30


def test_effects_classes():
    shield = ShieldEffect(duration=2, value=20)
    assert shield.name == "щит"
    assert shield.duration == 2

    stun = StunEffect(duration=1)
    assert stun.name == "оглушение"

    debuff = StatDebuff(stat="intellect", amount=5, duration=3)
    assert debuff.stat == "intellect"
    assert debuff.amount == 5


def test_skill_effects_integration():
    # Проверяем, что у навыков есть правильные эффекты
    shield_skill = Skills["Luke"]["силовой щит"]
    assert isinstance(shield_skill.effect, ShieldEffect)
    assert shield_skill.effect.value == 25

    stun_skill = Skills["R2D2"]["электрошок"]
    assert isinstance(stun_skill.effect, StunEffect)