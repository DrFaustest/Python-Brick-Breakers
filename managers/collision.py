import pygame as pg
from settings import *
from managers.vector import Vector2D
import math

class Collision:
    def __init__(self, ball, paddle, bricks, scoreboard):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.scoreboard = scoreboard

    def check_wall_collision(self):
        # Left or Right wall collision
        if self.ball.position.x <= 0 or self.ball.position.x + self.ball.radius * 2 >= self.screen_width:
            self.ball.velocity.x *= -1
        # Top wall collision
        if self.ball.position.y <= 0:
            self.ball.velocity.y *= -1
        # Bottom wall collision
        if self.ball.position.y + self.ball.radius * 2 >= self.screen_height:
            self.ball.attached_to_paddle = True
            self.ball.velocity = Vector2D(0, 0)
            self.scoreboard.decrease_score()

    def check_paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            offset = (self.ball.position.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            reflection_angle = offset * MAX_REFLECTION_ANGLE
            self.ball.velocity.x = math.cos(reflection_angle)
            self.ball.velocity.y = -math.sin(reflection_angle)
            self.ball.velocity.set_magnitude(BALL_SPEED)

    def check_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed and self.ball.rect.colliderect(brick.rect):
                # Determine the side of the collision
                if self.ball.velocity.x > 0:  # Moving right
                    # Check if it hit the left side of the brick
                    if self.ball.rect.right >= brick.rect.left and self.ball.rect.left < brick.rect.left:
                        self.ball.velocity.x *= -1  # Reverse horizontal direction
                elif self.ball.velocity.x < 0:  # Moving left
                    # Check if it hit the right side of the brick
                    if self.ball.rect.left <= brick.rect.right and self.ball.rect.right > brick.rect.right:
                        self.ball.velocity.x *= -1
                
                if self.ball.velocity.y > 0:  # Moving down
                    # Check if it hit the top side of the brick
                    if self.ball.rect.bottom >= brick.rect.top and self.ball.rect.top < brick.rect.top:
                        self.ball.velocity.y *= -1  # Reverse vertical direction
                elif self.ball.velocity.y < 0:  # Moving up
                    # Check if it hit the bottom side of the brick
                    if self.ball.rect.top <= brick.rect.bottom and self.ball.rect.bottom > brick.rect.bottom:
                        self.ball.velocity.y *= -1
    
                brick.is_destroyed = True  # Mark the brick as destroyed
                self.scoreboard.increase_score()
                break  # Assuming one collision per update for simplicity

    def update(self):
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
