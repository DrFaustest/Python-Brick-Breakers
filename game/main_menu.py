import pygame as pg
from ui.button import Button
from game.game_state import GameState
from settings import Settings
from utils.background_music import BackgroundMusic

class MainMenu(GameState):
    def __init__(self, game):
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
        buttons = []
        buttons.append(Button(self.screen,300, 100, 200, 100, "Play", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Playing")))
        buttons.append(Button(self.screen,300, 250, 200, 100, "Settings", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("Settings")))
        buttons.append(Button(self.screen,300, 400, 200, 100, "High Scores", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("GameOver")))
        buttons.append(Button(self.screen,700, 500, 50, 50, "", self.WHITE, self.GREEN, self.BLACK, self.game.background_music.change_music_state, self.game.background_music.current_image))
        return buttons

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.handle_event(event)
                    self.buttons[3].image = self.game.background_music.current_image

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw()