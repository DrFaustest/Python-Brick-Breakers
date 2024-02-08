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
from managers.collision import Collision
from managers.input import InputEvent
from managers.game_reset import GameReset


class Game():
    def __init__(self, screen):
        self.screen: pg.Surface = screen
        self.state: str = "Start"
        self.screen_width: int = SCREEN_WIDTH
        self.screen_height: int = SCREEN_HEIGHT
        self.background_image: pg.Surface = pg.image.load("img/background.png")
        self.background_image = pg.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.current_level_index: int = 0
        self.level: Level = Level(self.current_level_index)
        self.bricks: list[Brick] = self.level.bricks


        self.paddle: Paddle = Paddle()
        self.ball: Ball = Ball(self.paddle)
        self.scoreboard: Scoreboard = Scoreboard()  # Position of the scoreboard
        self.collision: Collision = Collision(self.ball, self.paddle, self.bricks, self.scoreboard)
        self.input_handler: InputEvent = InputEvent(self.paddle, self.ball)
        self.level_banner: LevelBanner = LevelBanner()
        self.game_reset: GameReset = GameReset(self)

    def start(self):
        self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)
        
        def change_to_playing():
            self.state: str = "Playing"
            self.screen.fill((0, 0, 0))

        play_button: Button = Button(300, 150, 200, 100, "Play", (255, 255, 255), (0, 255, 0), (0, 0, 0), change_to_playing)
        play_button.draw(self.screen)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                play_button.handle_event(event)

    def update(self):
        if self.state == "Playing":
            self.input_handler.handle_input()
            self.ball.update()
            self.collision.update()
            if self.level.is_level_complete():
                self.current_level_index += 1
                if DIFFICULTY < 10:
                    settings.DIFFICULTY += 0.2
                try:
                    self.game_reset.reset()
                    self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)
                except ValueError:
                    self.state: str = "Game Over"
                    self.screen.fill(WHITE)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        # Draw game objects
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)




    def game_over(self):
        pass
