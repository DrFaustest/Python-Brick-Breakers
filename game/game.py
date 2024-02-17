import pygame as pg
from settings import * 
import settings
from typing import *
from ui.button import Button
from objects.paddle import Paddle
from objects.ball import Ball
from objects.brick import Brick
from levels.level import Level
from ui.level_banner import LevelBanner
from ui.scoreboard import Scoreboard
from ui.player_lives import PlayerLives
from managers.collision import Collision
from managers.input import InputEvent
from managers.game_reset import GameReset
from utils.background_music import BackgroundMusic

class Game():
    def __init__(self, screen):
        self.screen: pg.Surface = screen   
        self.state: str = "Start"
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT
        self.background_image: pg.Surface = pg.image.load(BACKGROUND_IMG)
        self.background_image = pg.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.current_level_index: int = 0
        self.level: Level = Level(self.current_level_index)
        self.bricks: list[Brick] = self.level.bricks
        self.paddle: Paddle = Paddle()
        self.ball: Ball = Ball(self.paddle)
        self.scoreboard: Scoreboard = Scoreboard()  # Position of the scoreboard
        self.lives: PlayerLives = PlayerLives()
        self.collision: Collision = Collision(self.ball, self.paddle, self.bricks, self.scoreboard, self.lives)
        self.input_handler: InputEvent = InputEvent(self.paddle, self.ball)
        self.level_banner: LevelBanner = LevelBanner()
        self.game_reset: GameReset = GameReset(self)
        self.background_music: BackgroundMusic = BackgroundMusic()
        self.buttons: list[Button] = []
        self.setup_start_state()  # Setup for the start state
        

    def setup_start_state(self):
        self.buttons.clear()
        self.sound_button = (Button(700, 500, 50, 50, "", WHITE, GREEN, BLACK, self.change_music_state, self.background_music.current_image))
        self.buttons.append(self.sound_button)
        self.buttons.append(Button(300, 150, 200, 100, "Play", WHITE, GREEN, BLACK, self.change_to_playing))
        self.buttons.append(Button(300, 300, 200, 100, "Settings", WHITE, GREEN, BLACK, self.change_to_settings))
    
    def change_to_playing(self):
        self.state: str = "Playing"
        self.screen.fill((0, 0, 0))
    def change_to_settings(self):
        self.state: str = "Settings"
        self.screen.fill((0, 0, 0))
    def change_music_state(self):
        self.background_music.change_music_state()
        self.sound_button.image = self.background_music.current_image

        
    def update_start(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.handle_event(event)

    def draw_start(self):
        self.screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)


    def update_playing(self):
        self.input_handler.handle_input()
        self.ball.update()
        self.collision.update()
        if self.level.is_level_complete():
            self.handle_level_complete()
        if self.lives.lives == 0:
            self.state: str = "GameOver"
    
    def handle_level_complete(self):
        self.current_level_index += 1  # Move to the next level
        if DIFFICULTY < 10:
            settings.DIFFICULTY += 0.2  # Increase difficulty, if applicable

        self.game_reset.reset()  # Reset game elements for the next level
        # Optionally, display a level completion banner/message
        self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width,    self.screen_height)

    def draw_playing(self):
        self.screen.blit(self.background_image, (0, 0))
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.lives.draw(self.screen)

    def update_game_over(self, events):
    # Display a "Game Over" message and wait for player input to reset the game
        for event in events:
            if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                self.game_reset.full_reset()
                self.state = "Start"

    def draw_game_over(self):
        # Fill the screen with a different color or a game over screen
        self.screen.fill((0, 0, 0))  # Example: fill the screen with black
        # Display "Game Over" text
        font = pg.font.SysFont(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        self.screen.blit(text, text_rect)

    def update(self, events):
        if self.state == "Start":
            self.update_start(events)
        elif self.state == "Playing":
            self.update_playing()
        elif self.state == "GameOver":
            self.update_game_over(events)

    def draw(self):
        if self.state == "Start":
            self.draw_start()
        elif self.state == "Playing":
            self.draw_playing()
        elif self.state == "GameOver":
            self.draw_game_over()
