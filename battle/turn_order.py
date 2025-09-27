import random


class TurnOrder:
    def __init__(self, characters):
        self.characters = [char for char in characters if char.is_alive]
        self.current_index = 0
        self.turn_queue = []

    def roll_initiative(self):
        """Определяет порядок ходов на основе ловкости + случайность"""
        self.turn_queue = sorted(
            self.characters,
            key=lambda char: char.agility + random.randint(1, 20),
            reverse=True
        )
        self.current_index = 0

    def __iter__(self):
        self.roll_initiative()
        return self

    def __next__(self):
        if self.current_index >= len(self.turn_queue):
            raise StopIteration

        character = self.turn_queue[self.current_index]
        self.current_index += 1
        return character