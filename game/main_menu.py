from typing import List
import pygame as pg
from ui.button import Button
from game.game_state import GameState
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
    - background: The background image of the main menu.
    - buttons: The list of buttons in the main menu.

    Methods:
    - __init__(self, game: Game) -> None: Initializes the MainMenu object.
    - create_buttons(self) -> List[Button]: Creates the buttons for the main menu.
    - update(self, events: List[pg.event.Event]) -> None: Updates the main menu state based on user events.
    - draw(self) -> None: Draws the main menu on the screen.
    """

    def __init__(self, game) -> None:
        """
        Initializes the MainMenu object.

        Parameters:
        - game: The game object.
        """
        super().__init__(game)
        self.background = pg.image.load(self.settings.get("BACKGROUND_IMG")).convert()
        self.background = pg.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.buttons = self.create_buttons()

    def create_buttons(self) -> List[Button]:
        """
        Creates the buttons for the main menu.

        Returns:
        - buttons: The list of buttons in the main menu.
        """
        play_button_image = pg.image.load(self.settings.get("PLAY_BUTTON_IMG")).convert_alpha()
        settings_button_image = pg.image.load(self.settings.get("SETTINGS_BUTTON_IMG")).convert_alpha()
        high_scores_button_image = pg.image.load(self.settings.get("HIGH_SCORES_BUTTON_IMG")).convert_alpha()
        play_button_image = pg.transform.scale(play_button_image, (200, 100))
        settings_button_image = pg.transform.scale(settings_button_image, (200, 100))
        high_scores_button_image = pg.transform.scale(high_scores_button_image, (200, 100))
        buttons = []
        buttons.append(Button(self.screen, 300, 100, 200, 100, "", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Playing"), play_button_image))
        buttons.append(Button(self.screen, 300, 250, 200, 100, "", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Settings"), settings_button_image))
        buttons.append(Button(self.screen, 300, 400, 200, 100, "", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("GameOver"), high_scores_button_image))
        buttons.append(Button(self.screen, 700, 500, 50, 50, "", self.WHITE, self.GREEN, self.BLACK, self.game.background_music.change_music_state, self.game.background_music.current_image))
        return buttons

    def update(self, events: List[pg.event.Event]) -> None:
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

    def draw(self) -> None:
        """
        Draws the main menu on the screen.
        """
        self.game.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()
