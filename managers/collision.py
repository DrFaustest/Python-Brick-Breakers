import pygame as pg
from settings import Settings
import math
import random
from typing import List
from objects.ball import Ball
from objects.paddle import Paddle
from objects.brick import Brick
from ui.scoreboard import Scoreboard
from ui.player_lives import PlayerLives
from ui.level_banner import LevelBanner

class Collision(pg.sprite.Sprite):
    def __init__(self, ball: Ball, paddle: Paddle, bricks: List[Brick], scoreboard: Scoreboard, player_lives: PlayerLives, screen: pg.Surface):
        """
        Initializes a Collision object.

        Args:
            ball (Ball): The ball object.
            paddle (Paddle): The paddle object.
            bricks (List[Brick]): A list of brick objects.
            scoreboard (Scoreboard): The scoreboard object.
            player_lives (PlayerLives): The player lives object.
            screen (pg.Surface): The game screen surface.
        """
        super().__init__()
        self.settings = Settings()
        self.screen = screen
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = self.settings.get("SCREEN_WIDTH")
        self.screen_height = self.settings.get("SCREEN_HEIGHT")
        self.MAX_REFLECTION_ANGLE = self.settings.get("MAX_REFLECTION_ANGLE")
        self.BALL_SPEED = self.settings.get("BALL_SPEED")
        self.MIN_Y_VELOCITY = self.settings.get("MIN_Y_VELOCITY")
        self.scoreboard = scoreboard
        self.paddle_hit = False
        self.lives = player_lives
        self.level_banner = LevelBanner()


    def check_paddle_collision(self) -> None:
        """
        Checks for collision with the paddle and updates the ball's velocity accordingly.
        """
        if pg.sprite.collide_rect(self.ball, self.paddle) and not self.paddle_hit:
            self.paddle_hit = True
            offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            reflection_angle = offset * self.MAX_REFLECTION_ANGLE
            new_vx = math.cos(math.radians(reflection_angle)) * self.BALL_SPEED * (1 if offset > 0 else -1)
            speed_difference = self.BALL_SPEED ** 2 - new_vx ** 2
            speed_difference = max(0, speed_difference)  # Ensure that the value inside the square root is not negative
            new_vy = -math.sqrt(speed_difference)
            if abs(new_vy) < self.MIN_Y_VELOCITY:  # Ensure minimum vertical velocity
                new_vy = -self.MIN_Y_VELOCITY if new_vy < 0 else self.MIN_Y_VELOCITY
            if new_vy > 0: # Ensure that the ball is always moving upwards after hitting the paddle
                new_vy = -new_vy
            self.ball.velocity = pg.math.Vector2(new_vx, new_vy)
            spin_change = reflection_angle * 0.1
            self.ball.spin += spin_change
        elif not pg.sprite.collide_rect(self.ball, self.paddle):
            self.paddle_hit = False

    def check_wall_collision(self) -> None:
        """
        Checks for collision with the walls and updates the ball's velocity accordingly.
        """
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width:
            self.bounce(pg.math.Vector2(1, 0))
        if self.ball.rect.top <= 0:
            self.bounce(pg.math.Vector2(0, 1))

        if self.ball.rect.bottom >= self.screen_height:
            self.ball.attached_to_paddle = True
            self.ball.velocity = pg.math.Vector2(0, 0)
            self.level_banner.display_ball_lost_message(self.screen, self.screen_width, self.screen_height)
            self.scoreboard.decrease_score()
            self.lives.decrease_lives()


    def check_brick_collision(self) -> None:
        """
        Checks for collision with the bricks and updates the ball's velocity accordingly.
        """
        for brick in self.bricks:
            if not brick.is_destroyed and pg.sprite.collide_rect(self.ball, brick):
                collision_normal = pg.math.Vector2()
                if self.ball.velocity.x > 0 and self.ball.rect.right >= brick.rect.left:
                    collision_normal.x = -1
                elif self.ball.velocity.x < 0 and self.ball.rect.left <= brick.rect.right:
                    collision_normal.x = 1
                if self.ball.velocity.y > 0 and self.ball.rect.bottom >= brick.rect.top:
                    collision_normal.y = -1
                elif self.ball.velocity.y < 0 and self.ball.rect.top <= brick.rect.bottom:
                    collision_normal.y = 1
                self.bounce(collision_normal)  # Use the bounce method to handle collision
                brick.destroy()
                self.scoreboard.increase_score()
                break  # Stop checking after handling collision to avoid multiple responses

    def bounce(self, collision_normal: pg.math.Vector2) -> None:
        """
        Adjusts the ball's velocity based on the collision normal.

        Args:
            collision_normal (pg.math.Vector2): The normal vector of the collision surface.
        """
        self.ball.velocity = self.ball.velocity.reflect(collision_normal)
        angle_variation = random.uniform(-5, 5)
        angle_rad = math.radians(angle_variation)
        self.ball.velocity = self.ball.velocity.rotate(angle_rad)
        self.ball.spin += angle_variation * 0.75
        if abs(self.ball.velocity[1]) < self.MIN_Y_VELOCITY:
            self.ball.velocity[1] = self.MIN_Y_VELOCITY if self.ball.velocity[1] > 0 else -self.MIN_Y_VELOCITY

    def check_ball_stuck(self) -> None:
        """
        Checks if the ball is stuck and adjusts its velocity accordingly.
        """
        if self.ball.velocity[1] == 0:
            self.ball.velocity[1] = self.BALL_SPEED if self.ball.rect.centery > self.screen_height // 2 else -self.BALL_SPEED

        if self.ball.velocity[0] == 0 and (self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width):
            self.ball.velocity[0] = self.BALL_SPEED if self.ball.rect.centerx > self.screen_width // 2 else -self.BALL_SPEED

    def update(self) -> None:
        """
        Updates the collision detection.
        """
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
        self.check_ball_stuck()
