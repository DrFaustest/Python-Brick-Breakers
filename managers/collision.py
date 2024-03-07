import pygame as pg
from settings import Settings
import math
import random


class Collision(pg.sprite.Sprite):
    def __init__(self, ball, paddle, bricks, scoreboard, player_lives):
        """
        Initializes a Collision object.

        Args:
            ball (Ball): The ball object.
            paddle (Paddle): The paddle object.
            bricks (list): A list of brick objects.
            scoreboard (Scoreboard): The scoreboard object.
            player_lives (PlayerLives): The player lives object.
        """
        super().__init__()
        self.settings = Settings()
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


    def check_paddle_collision(self):
        """
        Checks for collision with the paddle and updates the ball's velocity accordingly.
        """
        if pg.sprite.collide_rect(self.ball, self.paddle) and not self.paddle_hit:
            self.paddle_hit = True
            offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            reflection_angle = offset * self.MAX_REFLECTION_ANGLE
            new_vx = math.cos(math.radians(reflection_angle)) * self.BALL_SPEED * (1 if offset > 0 else -1)
            new_vy = -math.sqrt(self.BALL_SPEED ** 2 - new_vx ** 2)
            if new_vy > self.MIN_Y_VELOCITY:
                new_vy = self.MIN_Y_VELOCITY
                new_vx = math.copysign(math.sqrt(self.BALL_SPEED ** 2 - new_vy ** 2), new_vx)
            self.ball.velocity = pg.math.Vector2(new_vx, new_vy)
        elif not pg.sprite.collide_rect(self.ball, self.paddle):
            self.paddle_hit = False

    def check_wall_collision(self):
        """
        Checks for collision with the walls and updates the ball's velocity accordingly.
        """
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width:
            self.bounce(pg.math.Vector2(1, 0))  # Horizontal normal
        if self.ball.rect.top <= 0:
            self.bounce(pg.math.Vector2(0, 1))  # Vertical normal

        # Handle the bottom screen collision separately as it might reset the ball
        if self.ball.rect.bottom >= self.screen_height:
            self.ball.attached_to_paddle = True
            self.ball.velocity = pg.math.Vector2(0, 0)
            self.scoreboard.decrease_score()
            self.lives.decrease_lives()

    def check_brick_collision(self):
        """
        Checks for collision with the bricks and updates the ball's velocity accordingly.
        """
        for brick in self.bricks:
            if not brick.is_destroyed and pg.sprite.collide_rect(self.ball, brick):
                # Determine the collision normal based on the ball's position relative to the brick
                if self.ball.velocity.x > 0:  # Coming from the left
                    if self.ball.rect.right >= brick.rect.left and self.ball.rect.left < brick.rect.left:
                        self.bounce(pg.math.Vector2(1, 0))  # Horizontal normal
                elif self.ball.velocity.x < 0:  # Coming from the right
                    if self.ball.rect.left <= brick.rect.right and self.ball.rect.right > brick.rect.right:
                        self.bounce(pg.math.Vector2(-1, 0))  # Horizontal normal

                if self.ball.velocity.y > 0:  # Coming from the top
                    if self.ball.rect.bottom >= brick.rect.top and self.ball.rect.top < brick.rect.top:
                        self.bounce(pg.math.Vector2(0, 1))  # Vertical normal
                elif self.ball.velocity.y < 0:  # Coming from the bottom
                    if self.ball.rect.top <= brick.rect.bottom and self.ball.rect.bottom > brick.rect.bottom:
                        self.bounce(pg.math.Vector2(0, -1))  # Vertical normal

                brick.destroy()
                self.scoreboard.increase_score()
                break

    def bounce(self, collision_normal):
        """
        Adjusts the ball's velocity based on the collision normal.

        Args:
            collision_normal (pg.math.Vector2): The normal vector of the collision surface.
        """
        # Reflect the ball's velocity vector over the collision normal
        self.ball.velocity = self.ball.velocity.reflect(collision_normal)

        # Add a slight randomness to avoid infinite loops in certain scenarios
        angle_variation = random.uniform(-10, 10)  # You can adjust the range as needed
        angle_rad = math.radians(angle_variation)
        self.ball.velocity = self.ball.velocity.rotate(angle_rad)
    
    def check_ball_stuck(self):
        # Adjust the y velocity if it's 0 to ensure the ball moves vertically.
        if self.ball.velocity.y == 0:
            self.ball.velocity.y = self.BALL_SPEED if self.ball.rect.centery > self.screen_height // 2 else -self.BALL_SPEED

        # If the ball is stuck on the left or right wall, invert the x velocity.
        if self.ball.velocity.x == 0 and (self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width):
            self.ball.velocity.x = self.BALL_SPEED if self.ball.rect.centerx > self.screen_width // 2 else -self.BALL_SPEED


    def update(self):
        """
        Updates the collision detection.
        """
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
        self.check_ball_stuck()
