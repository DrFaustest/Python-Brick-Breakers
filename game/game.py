import pygame as pg
from settings import *
from game.game_play import GamePlay
from game.main_menu import MainMenu
from game.settings_menu import SettingsMenu
from game.game_over import GameOver
from utils.background_music import BackgroundMusic



class Game():
    def __init__(self, screen):
        self.screen = screen
        self.background_music: BackgroundMusic = BackgroundMusic()
        self.music_current_image = self.background_music.current_image
        self.current_state = MainMenu(self)

    def change_state(self, new_state_str):
        if new_state_str == "Playing":
            self.current_state = GamePlay(self)
        elif new_state_str == "Settings":
            self.current_state = SettingsMenu(self)
        elif new_state_str == "GameOver":
            self.current_state = GameOver(self)
        elif new_state_str == "MainMenu":
            self.current_state = MainMenu(self)


    def update(self, events):
        self.current_state.update(events)

    def draw(self):
        self.current_state.draw()
