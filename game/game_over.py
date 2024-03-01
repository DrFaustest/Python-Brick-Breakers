import pygame as pg
from game.game_state import GameState
from ui.button import Button
from ui.text_box import TextBox
from utils.score_saver import ScoreSaver
from settings import *

class GameOver(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.score = PLAYER_SCORE
        self.screen = game.screen
        self.score_saver = ScoreSaver()
        self.new_high_score = self.score_saver.check_high_score(self.score)
        self.state = 'ENTER_NAME' if self.new_high_score else 'DISPLAY_SCORE'
        self.text_box = TextBox(300, 200, 200, 50, "Enter Name") if self.new_high_score else None
        self.submit_button = Button(300, 300, 200, 50, "Submit", WHITE, GREEN, BLACK, self.submit_score) if self.new_high_score else None
        self.back_button = Button(300, 400, 300, 50, "Back to Menu", WHITE, GREEN, BLACK, lambda: self.game.change_state("MainMenu"))

    def submit_score(self):
        if self.new_high_score:
            name = self.text_box.text
            self.score_saver.add_score(name, self.score)
        self.state = 'DISPLAY_SCORE'

    def update(self, events):
        for event in events:
            if self.state == 'ENTER_NAME':
                self.text_box.handle_event(event)
                self.submit_button.handle_event(event)
            elif self.state == 'DISPLAY_SCORE':
                self.back_button.handle_event(event)

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == 'ENTER_NAME':
            self.text_box.draw(self.screen)
            self.submit_button.draw(self.screen)
        elif self.state == 'DISPLAY_SCORE':
            # Display the score and possibly the high score list
            display_scores = self.score_saver.score_display()
            for i, line in enumerate(display_scores):
                score_text = pg.font.Font(None, 36).render(line, True, WHITE)
                self.screen.blit(score_text, (50, 50 + i * 30))
            self.back_button.draw(self.screen)
