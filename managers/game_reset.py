import pygame as pg
from levels.level import Level
from managers.collision import Collision
from objects.paddle import Paddle
from objects.ball import Ball
from ui.scoreboard import Scoreboard
from typing import *
from settings import *

class GameReset:
    def __init__(self, game):
        self.game = game

    def reset(self):
        # Load the new level
        self.game.level = Level(self.game.current_level_index)
        self.game.bricks = self.game.level.bricks

        # Reset paddle position
        self.game.paddle.rect.centerx = self.game.screen_width // 2
        self.game.paddle.rect.y = 550  # Assuming a fixed Y position

        # Reset ball position and state
        self.game.ball.x = self.game.paddle.rect.centerx
        self.game.ball.y = self.game.paddle.rect.top - BALL_RADIUS
        self.game.ball.speed_x = 0
        self.game.ball.speed_y = 0
        self.game.ball.attached_to_paddle = True

        # Reset collision detection with the new bricks
        self.game.collision = Collision(self.game.ball, self.game.paddle, self.game.bricks, self.game.scoreboard, self.game.lives)

    def full_reset(self):
        self.game.current_level_index = 0
        self.game.scoreboard.score = 0
        self.game.lives.lives = 3
        self.reset()




