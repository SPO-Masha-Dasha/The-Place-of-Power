from effects.effect_library import ShieldEffect, StunEffect, StatDebuff

class Skill:
    def __init__(self, name, cost, cooldown, effect=None):
        self.name = name
        self.cost = cost
        self.cooldown = cooldown
        self.effect = effect

# Библиотека навыков
Skills = {
    "Luke": {
        "силовой толчок": Skill(name="силовой толчок", cost=15, cooldown=1, effect=None),
        "силовой щит": Skill(name="силовой щит", cost=20, cooldown=2, effect=ShieldEffect(duration=2, value=25)),
        "исцеление": Skill(name="исцеление", cost=25, cooldown=3, effect=None),
    },
    "Yoda": {
        "запутывание разума": Skill(name="запутывание разума", cost=20, cooldown=2, effect=StatDebuff(stat="intellect", amount=15, duration=2)),
        "мудрость силы": Skill(name="мудрость силы", cost=30, cooldown=3, effect=None),
        "вдохновение союзников": Skill(name="вдохновение союзников", cost=25, cooldown=3, effect=ShieldEffect(duration=3, value=15)),
    },
    "R2D2": {
        "электрошок": Skill(name="электрошок", cost=30, cooldown=1, effect=StunEffect(duration=1)),
        "экстренный ремонт": Skill(name="экстренный ремонт", cost=40, cooldown=2, effect=None),
    },
}