class Item:
    def __init__(self, name, description, use_func, one_time=True):
        self.name = name
        self.description = description
        self.use_func = use_func
        self.one_time = one_time
        self.used = False

    def use(self, user, target=None):
        if self.one_time and self.used:
            user.log(f"{self.name} уже использован!")
            return False

        result = self.use_func(user, target)
        if result and self.one_time:
            self.used = True
        return result


# --- Эффекты предметов ---
def magic_word_effect(user, target=None):
    """Отвлекает босса на 1 ход (пропускает ход)."""
    if target and hasattr(target, "skip_next_turn"):
        target.skip_next_turn = True
        user.log(f"{user.name} использует Волшебное слово! {target.name} пропустит следующий ход.")
        return True
    else:
        user.log("Волшебное слово не сработало --- цель не является Боссом.")
        return False


def auto_exam_effect(user, target=None):
    """Гарантирует попадание следующей атаки."""
    user.next_hit_guaranteed = True
    user.log(f"{user.name} использует Зачёт автоматом! Следующая атака попадёт гарантированно.")
    return True


# --- Создание предметов ---
magic_word = Item(
    name="Волшебное слово",
    description="Отвлекает босса. Он пропустит следующий ход.",
    use_func=magic_word_effect,
    one_time=True
)

auto_exam = Item(
    name="Зачёт автоматом",
    description="Гарантирует попадание следующей атаки.",
    use_func=auto_exam_effect,
    one_time=True
)

# Словарь для быстрого доступа
ITEMS = {
    "волшебное слово": magic_word,
    "зачёт автоматом": auto_exam
}