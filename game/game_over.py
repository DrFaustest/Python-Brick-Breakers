import pygame
from game.game_state import GameState
from settings import *
from ui.button import Button
from ui.text_box import TextBox
from ui.scoreboard import Scoreboard
from utils.score_saver import ScoreSaver

class GameOver(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.state = 'CHECK_SCORE'  # Initial state
        self.score = PLAYER_SCORE
        self.score_saver = ScoreSaver()
        self.new_high_score = self.score_saver.check_high_score(self.score)
        self.name_entry = None
        self.submit_button = None
        self.back_button = Button(300, 400, 200, 50, "Back to Menu", WHITE, GREEN, BLACK, lambda: self.game.change_state("MainMenu"))


    def update(self, events):
        for event in events:
            if self.state == 'CHECK_SCORE':
                if self.new_high_score:
                    self.state = 'ENTER_NAME'
                    self.name_entry = TextBox(300, 200, 200, 50, "Enter Name")
                    self.submit_button = Button(300, 300, 200, 50, "Submit", WHITE, GREEN, BLACK, self.submit_score)
                else:
                    self.state = 'SHOW_SCORE'
            elif self.state == 'ENTER_NAME':
                self.name_entry.handle_event(event)
                self.submit_button.handle_event(event)
            elif self.state == 'SHOW_SCORE':
                self.back_button.handle_event(event)

    def submit_score(self):
        self.score_saver.save_score(self.name_entry.text, self.score)
        self.state = 'SHOW_SCORE'


    def draw(self):
        self.screen.fill(BLACK)  # Background for the game over screen
        if self.state == 'CHECK_SCORE':
            # Render a checking score message or a simple pause before showing the result
            font = pygame.font.Font(None, 36)
            text = font.render("Checking score...", True, WHITE)
            self.screen.blit(text, (300, 200))
        elif self.state == 'ENTER_NAME':
            self.name_entry.draw(self.screen)
            self.submit_button.draw(self.screen)
        elif self.state == 'SHOW_SCORE':
            # Display the score and possibly the high score table
            self.scoreboard = Scoreboard(100, 100, self.score_saver.check_high_score(self.score))
            self.scoreboard.draw(self.screen)
            self.back_button.draw(self.screen)


#get the score from the game play and check if it is a high score if not then display the score and a button to go back to the main menu. if it is a high score then display a text box with the prompt "Enter your name" and a submit button. once the name is submitted then display the high scores and a button to go back to the main menu.