

class GameState:
    def __init__(self, game):
        self.game = game

    def update(self, events):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError
