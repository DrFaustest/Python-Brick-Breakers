import pygame as pg
from settings import *

from typing import *

class Collision:
    def __init__(self, ball, paddle, bricks, scoreboard):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.scoreboard = scoreboard

    def check_wall_collision(self):
        # Check for collision with left, right, and top walls
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width:
            self.ball.speed_x *= -1  # Reverse horizontal direction
        if self.ball.rect.top <= 0:
            self.ball.speed_y *= -1  # Reverse vertical direction

        # reattach ball to paddle if it hits the bottom wall
        if self.ball.rect.bottom >= self.screen_height:
            self.ball.attached_to_paddle = True
            self.ball.speed_x = 0
            self.ball.speed_y = 0
            self.ball.x = self.paddle.rect.centerx
            self.ball.y = self.paddle.rect.top - self.ball.radius
            self.ball.rect.x = self.ball.x - self.ball.radius
            self.ball.rect.y = self.ball.y - self.ball.radius 
            self.scoreboard.decrease_score()

        # Add bottom wall collision if needed (usually results in game over)

    def check_paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y *= -1  # Reverse vertical direction

    def check_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed and self.ball.rect.colliderect(brick.rect):
                self.ball.speed_y *= -1  # Reverse vertical direction
                brick.is_destroyed = True  # Mark the brick as destroyed
                self.scoreboard.increase_score()
                break


    def update(self):
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()