class Effect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def on_apply(self, character):
        """При первом применении эффекта"""
        pass

    def on_turn_start(self, character):
        """В начале хода персонажа"""
        pass

    def on_turn_end(self, character):
        """В конце хода персонажа"""
        pass

    def on_remove(self, character):
        """При удалении эффекта"""
        pass


class ShieldEffect(Effect):
    def __init__(self, duration, value):
        super().__init__("щит", duration)
        self.value = value

    def on_apply(self, character):
        character.shield = getattr(character, 'shield', 0) + self.value
        character.log(f"{character.name} получает щит +{self.value}")

    def on_remove(self, character):
        character.shield = max(0, character.shield - self.value)
        character.log(f"{character.name}: эффект щита исчез.")


class StatDebuff(Effect):
    def __init__(self, stat, amount, duration):
        super().__init__(f"дебафф {stat}", duration)
        self.stat = stat
        self.amount = amount
        self.original_value = None

    def on_apply(self, character):
        if not hasattr(character, "_original_stats"):
            character._original_stats = {}

        if self.stat not in character._original_stats:
            self.original_value = getattr(character, self.stat)
            character._original_stats[self.stat] = self.original_value

        new_value = max(1, getattr(character, self.stat) - self.amount)
        setattr(character, self.stat, new_value)
        character.log(f"{character.name} получает -{self.amount} к {self.stat}")

    def on_remove(self, character):
        if self.original_value is not None:
            setattr(character, self.stat, self.original_value)
            if self.stat in getattr(character, '_original_stats', {}):
                del character._original_stats[self.stat]
        character.log(f"{character.name}: дебафф {self.stat} исчез.")


class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__("оглушение", duration)

    def on_apply(self, character):
        character.stunned = True
        character.log(f"{character.name} оглушён!")

    def on_remove(self, character):
        character.stunned = False
        character.log(f"{character.name} больше не оглушен.")


class SilenceEffect(Effect):
    def __init__(self, duration):
        super().__init__("немота", duration)
        self.original_can_use_skills = None

    def on_apply(self, character):
        self.original_can_use_skills = getattr(character, 'can_use_skills', True)
        character.can_use_skills = False
        character.log(f"{character.name} получил немоту и не может использовать навыки!")

    def on_remove(self, character):
        if self.original_can_use_skills is not None:
            character.can_use_skills = self.original_can_use_skills
        character.log(f"{character.name} снова может использовать навыки.")


class FearEffect(Effect):
    def __init__(self, duration):
        super().__init__("страх", duration)
        self.accuracy_reduction = 0.2  # -20% точности

    def on_apply(self, character):
        character.log(f"{character.name} испытывает страх! Точность снижена.")

    def on_turn_start(self, character):
        # В реальной игре здесь бы уменьшалась точность атак
        pass

    def on_remove(self, character):
        character.log(f"{character.name} преодолел страх.")