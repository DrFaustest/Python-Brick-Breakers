import pygame as pg
from game.game_state import GameState
from ui.button import Button
from ui.text_box import TextBox
from utils.score_saver import ScoreSaver
from settings import Settings


class GameOver(GameState):
    """Represents the game over state of the game.

    This class inherits from the GameState class and handles the game over logic,
    including displaying the player's score, allowing the player to enter their name
    for high score submission, and providing options to go back to the main menu.

    Attributes:
        WHITE (tuple): The RGB color value for white.
        GREEN (tuple): The RGB color value for green.
        BLACK (tuple): The RGB color value for black.
        score (int): The player's score.
        screen (pygame.Surface): The game screen.
        score_saver (ScoreSaver): The score saver object for saving high scores.
        new_high_score (bool): Indicates if the player achieved a new high score.
        state (str): The current state of the game over screen.
        text_box (TextBox): The text box for entering the player's name.
        submit_button (Button): The button for submitting the high score.
        back_button (Button): The button for going back to the main menu.
    """

    def __init__(self, game):
        """Initializes the GameOver object.

        Args:
            game (Game): The game object.
        """
        super().__init__(game)
        settings = Settings()
        self.WHITE = settings.get("WHITE")
        self.GREEN = settings.get("GREEN")
        self.BLACK = settings.get("BLACK")
        self.score = game.player_score
        self.screen = game.screen
        self.score_saver = ScoreSaver()
        self.new_high_score = self.score_saver.check_high_score(self.score)
        self.state = 'ENTER_NAME' if self.new_high_score else 'DISPLAY_SCORE'
        self.text_box = TextBox(300, 200, 200, 50, self.submit_score, "Enter Name") if self.new_high_score else None
        self.submit_button = Button(self.screen, 300, 300, 200, 50, "Submit", self.WHITE, self.GREEN, self.BLACK, self.submit_score) if self.new_high_score else None
        self.back_button = Button(self.screen, 300, 400, 300, 50, "Back to Menu", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("MainMenu"))

    def submit_score(self):
        """Submits the player's high score.

        If the player achieved a new high score, their name and score are added to the
        score saver object. The player's score is reset to 0, and the state is changed
        to 'DISPLAY_SCORE'.
        """
        if self.new_high_score:
            name = self.text_box.text
            self.score_saver.add_score(name, self.score)
            self.game.player_score = 0
        self.state = 'DISPLAY_SCORE'

    def update(self, events):
        """Updates the game over screen.

        Handles the events and updates the state of the game over screen accordingly.

        Args:
            events (list): A list of pygame events.
        """
        for event in events:
            if self.state == 'ENTER_NAME':
                self.text_box.handle_event(event)
                self.submit_button.handle_event(event)
            elif self.state == 'DISPLAY_SCORE':
                self.back_button.handle_event(event)

    def draw(self):
        """Draws the game over screen.

        Draws the appropriate elements on the game screen based on the current state.
        """
        self.screen.fill(self.BLACK)
        if self.state == 'ENTER_NAME':
            self.text_box.draw(self.screen)
            self.submit_button.draw()
        elif self.state == 'DISPLAY_SCORE':
            display_scores = self.score_saver.score_display()
            for i, line in enumerate(display_scores):
                score_text = pg.font.Font(None, 36).render(line, True, self.WHITE)
                self.screen.blit(score_text, (50, 50 + i * 30))
            self.back_button.draw()
