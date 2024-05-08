import pygame as pg
from game.game_state import GameState
from ui.button import Button
from ui.text_box import TextBox
from utils.score_saver import ScoreSaver
from settings import Settings

class GameOver(GameState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.score: int = game.player_score
        self.score_saver: ScoreSaver = ScoreSaver()
        self.new_high_score: bool = self.score_saver.check_high_score(self.score)
        self.state: str = 'ENTER_NAME' if self.new_high_score else 'DISPLAY_SCORE'
        self.text_box: TextBox = TextBox(300, 200, 200, 50, self.submit_score, "Enter Name") if self.new_high_score else None
        self.submit_button: Button = Button(self.screen, 300, 300, 200, 50, "Submit", self.WHITE, self.GREEN, self.BLACK, self.submit_score) if self.new_high_score else None
        self.back_button: Button = Button(self.screen, 300, 400, 300, 50, "Back to Menu", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("MainMenu"))

    def submit_score(self) -> None:
        if self.text_box.text == '':
            self.submit_button.error=True
            return
        if self.new_high_score:
            name: str = self.text_box.text
            self.score_saver.add_score(name, self.score)
            self.score_saver.save_scores()
            self.game.player_score = 0
        self.state = 'DISPLAY_SCORE'

    def update(self, events: list) -> None:
        for event in events:
            if self.state == 'ENTER_NAME':
                self.text_box.handle_event(event)
                self.submit_button.handle_event(event)
            elif self.state == 'DISPLAY_SCORE':
                self.back_button.handle_event(event)

    def draw(self) -> None:
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
