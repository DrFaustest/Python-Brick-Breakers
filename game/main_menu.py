import pygame as pg
from ui.button import Button
from game.game_state import GameState
from settings import *
from utils.background_music import BackgroundMusic

class MainMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.background = pg.image.load(BACKGROUND_IMG).convert()
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = self.create_buttons()
        

    def create_buttons(self):
        buttons = []
        buttons.append(Button(300, 150, 200, 100, "Play", WHITE, GREEN, BLACK, lambda: self.game.change_state("Playing")))
        buttons.append(Button(300, 300, 200, 100, "Settings", WHITE, GREEN, BLACK, lambda: self.game.change_state("Settings")))
        buttons.append(Button(700, 500, 50, 50, "", WHITE, GREEN, BLACK, self.game.background_music.change_music_state, self.game.background_music.current_image))
        return buttons

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.handle_event(event)
                    self.buttons[2].image = self.game.background_music.current_image

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(self.game.screen)