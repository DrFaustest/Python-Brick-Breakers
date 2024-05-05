from typing import Tuple
from settings import Settings

class GameState:
    def __init__(self, game):
        """
        Initialize the game state.

        Args:
            game (Game): The game object.

        """
        self.game = game
        self.settings = Settings()
        self.WHITE: Tuple[int, int, int] = self.settings.get("WHITE")
        self.GREEN: Tuple[int, int, int] = self.settings.get("GREEN")
        self.BLACK: Tuple[int, int, int] = self.settings.get("BLACK")
        self.GRAY: Tuple[int, int, int] = self.settings.get("GRAY")
        self.screen = game.screen
        self.screen_width: int = self.settings.get("SCREEN_WIDTH")
        self.screen_height: int = self.settings.get("SCREEN_HEIGHT")