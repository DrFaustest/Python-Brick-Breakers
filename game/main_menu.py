import pygame as pg
from ui.button import Button
from game.game_state import GameState
from settings import Settings
from utils.background_music import BackgroundMusic

class MainMenu(GameState):
    """
    Represents the main menu state of the game.

    Attributes:
    - game: The game object.
    - screen: The game screen.
    - settings: The game settings.
    - screen_width: The width of the game screen.
    - screen_height: The height of the game screen.
    - WHITE: The color white.
    - GREEN: The color green.
    - BLACK: The color black.
    - background: The background image of the main menu.
    - buttons: The list of buttons in the main menu.

    Methods:
    - __init__(self, game): Initializes the MainMenu object.
    - create_buttons(self): Creates the buttons for the main menu.
    - update(self, events): Updates the main menu state based on user events.
    - draw(self): Draws the main menu on the screen.
    """

    def __init__(self, game):
        """
        Initializes the MainMenu object.

        Parameters:
        - game: The game object.
        """
        super().__init__(game)
        self.screen = game.screen
        self.settings = Settings()
        self.screen_width = self.settings.get("SCREEN_WIDTH")
        self.screen_height = self.settings.get("SCREEN_HEIGHT")
        self.WHITE = self.settings.get("WHITE")
        self.GREEN = self.settings.get("GREEN")
        self.BLACK = self.settings.get("BLACK")
        self.background = pg.image.load(self.settings.get("BACKGROUND_IMG")).convert()
        self.background = pg.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.buttons = self.create_buttons()
        

    def create_buttons(self):
        """
        Creates the buttons for the main menu.

        Returns:
        - buttons: The list of buttons in the main menu.
        """
        buttons = []
        buttons.append(Button(self.screen,300, 100, 200, 100, "Play", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Playing")))
        buttons.append(Button(self.screen,300, 250, 200, 100, "Settings", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Settings")))
        buttons.append(Button(self.screen,300, 400, 200, 100, "High Scores", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("GameOver")))
        buttons.append(Button(self.screen,700, 500, 50, 50, "", self.WHITE, self.GREEN, self.BLACK, self.game.background_music.change_music_state, self.game.background_music.current_image))
        return buttons

    def update(self, events):
        """
        Updates the main menu state based on user events.

        Parameters:
        - events: The list of user events.
        """
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.handle_event(event)
                    self.buttons[3].image = self.game.background_music.current_image

    def draw(self):
        """
        Draws the main menu on the screen.
        """
        self.game.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()