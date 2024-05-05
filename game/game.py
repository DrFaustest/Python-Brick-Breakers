from game.game_play import GamePlay
from game.main_menu import MainMenu
from game.settings_menu import SettingsMenu
from game.game_over import GameOver
from utils.background_music import BackgroundMusic

class Game:
    """
    Represents the main game class.

    Attributes:
    - screen: The game screen object.
    - player_score: The current score of the player.
    - background_music: The background music object.
    - music_current_image: The current image of the background music.
    - current_state: The current state of the game (MainMenu, GamePlay, SettingsMenu, GameOver).
    """

    def __init__(self, screen: object) -> None:
        """
        Initializes a new instance of the Game class.

        Parameters:
        - screen: The game screen object.
        """
        self.screen = screen
        self.player_score: int = 0
        self.background_music: BackgroundMusic = BackgroundMusic()
        self.music_current_image: str = self.background_music.current_image
        self.current_state: object = MainMenu(self)

    def change_state(self, new_state_str: str) -> None:
        """
        Changes the current state of the game.

        Parameters:
        - new_state_str: The new state string (Playing, Settings, GameOver, MainMenu).
        """
        if new_state_str == "Playing":
            self.current_state = GamePlay(self)
        elif new_state_str == "Settings":
            self.current_state = SettingsMenu(self)
        elif new_state_str == "GameOver":
            self.current_state = GameOver(self)
        elif new_state_str == "MainMenu":
            self.current_state = MainMenu(self)

    def update(self, events: list) -> None:
        """
        Updates the game state.

        Parameters:
        - events: The list of events to process.
        """
        self.current_state.update(events)

    def draw(self) -> None:
        """
        Draws the game state.
        """
        self.current_state.draw()
