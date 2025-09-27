class BoundedStat:
    def __init__(self, name, min_value, max_value, allow_negative=False):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.allow_negative = allow_negative
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.min_value)

    def __set__(self, instance, value):
        if not self.allow_negative and value < self.min_value:
            value = self.min_value  # Вместо ошибки - ставим минимум
        if value > self.max_value:
            value = self.max_value
        if value < self.min_value:
            value = self.min_value
        setattr(instance, self.private_name, value)