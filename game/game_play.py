import pygame as pg
from settings import *
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
from game.game_state import GameState
import settings as settings


class GamePlay(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = game.screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.difficulty = DIFFICULTY
        self.background_image = pg.image.load(BACKGROUND_IMG).convert()
        self.background_image = pg.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_level_index = 0
        self.level: Level = Level(self.current_level_index)
        self.bricks = self.level.bricks
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.scoreboard = Scoreboard()
        self.lives = PlayerLives()
        self.collision = Collision(self.ball, self.paddle, self.bricks, self.scoreboard, self.lives)
        self.input_handler = InputEvent(self.paddle, self.ball)
        self.level_banner = LevelBanner()
        self.game_reset = GameReset(self)

    def update(self, events: list):
        """Update the game logic in the playing state."""
        self.input_handler.handle_input()
        self.ball.update()
        self.collision.update()
        if self.level.is_level_complete():
            self.handle_level_complete()
        if self.lives.lives == 0:
            settings.DIFFICULTY = 1
            self.game.player_score = self.scoreboard.score
            self.game.change_state("GameOver")
    
    def handle_level_complete(self):
        self.current_level_index += 1
        if settings.DIFFICULTY < 10:
            settings.DIFFICULTY += 0.2
        self.game_reset.reset()
        self.level_banner.display(self.screen, self.current_level_index + 1, SCREEN_WIDTH,SCREEN_HEIGHT)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.lives.draw(self.screen)