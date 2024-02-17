import pygame as pg
from settings import *
import math


class Collision:
    def __init__(self, ball, paddle, bricks, scoreboard):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.scoreboard = scoreboard
        self.paddle_hit=False

    def check_wall_collision(self):
        if (self.ball.position.x - BALL_RADIUS) <= 0 or (self.ball.position.x + BALL_RADIUS * 2) >= self.screen_width:
            self.ball.velocity.x *= -1
        if (self.ball.position.y-BALL_RADIUS) <= 0:
            self.ball.velocity.y *= -1
        if self.ball.position.y + BALL_RADIUS * 2 >= self.screen_height:
            self.ball.attached_to_paddle = True
            self.ball.velocity = pg.math.Vector2(0, 0)
            self.scoreboard.decrease_score()

    def check_paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect) and not self.paddle_hit:
            self.paddle_hit = True
            offset = (self.ball.position.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            reflection_angle = offset * MAX_REFLECTION_ANGLE
            new_vx = math.cos(math.radians(reflection_angle)) * BALL_SPEED * (1 if offset > 0 else -1)
            new_vy = -math.sqrt(BALL_SPEED**2 - new_vx**2)
            if new_vy > MIN_Y_VELOCITY:
                new_vy = MIN_Y_VELOCITY
                new_vx = math.copysign(math.sqrt(BALL_SPEED**2 - new_vy**2), new_vx)
            self.ball.velocity = pg.math.Vector2(new_vx, new_vy)
        elif not self.ball.rect.colliderect(self.paddle.rect):
            self.paddle_hit = False

    def check_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed and self.ball.rect.colliderect(brick.rect):
                if self.ball.velocity.x > 0:
                    if self.ball.rect.right >= brick.rect.left and self.ball.rect.left < brick.rect.left:
                        self.ball.velocity.x *= -1 
                elif self.ball.velocity.x < 0:
                    if self.ball.rect.left <= brick.rect.right and self.ball.rect.right > brick.rect.right:
                        self.ball.velocity.x *= -1
                
                if self.ball.velocity.y > 0:
                    if self.ball.rect.bottom >= brick.rect.top and self.ball.rect.top < brick.rect.top:
                        self.ball.velocity.y *= -1
                elif self.ball.velocity.y < 0:
                    if self.ball.rect.top <= brick.rect.bottom and self.ball.rect.bottom > brick.rect.bottom:
                        self.ball.velocity.y *= -1
                brick.is_destroyed = True
                self.scoreboard.increase_score()
                break

    def update(self):
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
