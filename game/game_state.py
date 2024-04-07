from settings import Settings
class GameState:
    def __init__(self, game):
        self.game = game
        self.settings = Settings()
        self.WHITE = self.settings.get("WHITE")
        self.GREEN = self.settings.get("GREEN")
        self.BLACK = self.settings.get("BLACK")
        self.GRAY = self.settings.get("GRAY")
        self.screen = game.screen