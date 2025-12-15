import pygame as pg
from settings import Settings
import math
import random
from typing import List
from objects.ball import Ball
from objects.paddle import Paddle
from objects.brick import Brick
from objects.moving_brick import MovingBrick
from ui.scoreboard import Scoreboard
from ui.player_lives import PlayerLives
from ui.level_banner import LevelBanner
from levels.level import Level

class Collision(pg.sprite.Sprite):
    def __init__(self, balls: List[Ball], paddle: Paddle, level: Level, scoreboard: Scoreboard, player_lives: PlayerLives, screen: pg.Surface, game_play) -> None:
        """
        Initializes a Collision object.

        Args:
            balls (List[Ball]): List of ball objects.
            paddle (Paddle): The paddle object.
            level (Level): The level object containing brick rows.
            scoreboard (Scoreboard): The scoreboard object.
            player_lives (PlayerLives): The player lives object.
            screen (pg.Surface): The game screen surface.
            game_play: Reference to the GamePlay instance for spawning balls.
        """
        super().__init__()
        self.settings = Settings()
        self.screen = screen
        self.balls = balls
        self.paddle = paddle
        self.level = level
        self.bricks = level.bricks  # Keep reference for compatibility
        self.screen_width = self.settings.get("SCREEN_WIDTH")
        self.screen_height = self.settings.get("SCREEN_HEIGHT")
        self.MAX_REFLECTION_ANGLE = self.settings.get("MAX_REFLECTION_ANGLE")
        self.BALL_SPEED = self.settings.get("BALL_SPEED")
        self.MIN_Y_VELOCITY = self.settings.get("MIN_Y_VELOCITY")
        self.BALL_RADIUS = self.settings.get("BALL_RADIUS")
        self.scoreboard = scoreboard
        self.paddle_hit_dict = {}  # Track paddle hits per ball
        self.lives = player_lives
        self.level_banner = LevelBanner()
        self.game_play = game_play

    def check_paddle_collision(self, ball: Ball) -> None:
        """
        Checks for collision with the paddle and updates the ball's velocity accordingly.
        
        Args:
            ball (Ball): The ball to check collision for.
        """
        ball_id = id(ball)
        if ball_id not in self.paddle_hit_dict:
            self.paddle_hit_dict[ball_id] = False
            
        if pg.sprite.collide_rect(ball, self.paddle) and not self.paddle_hit_dict[ball_id]:
            self.paddle_hit_dict[ball_id] = True
            offset = (ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            reflection_angle = offset * self.MAX_REFLECTION_ANGLE
            new_vx = math.cos(math.radians(reflection_angle)) * self.BALL_SPEED * (1 if offset > 0 else -1)
            speed_difference = self.BALL_SPEED ** 2 - new_vx ** 2
            speed_difference = max(0, speed_difference)  # Ensure that the value inside the square root is not negative
            new_vy = -math.sqrt(speed_difference)
            if abs(new_vy) < self.MIN_Y_VELOCITY:  # Ensure minimum vertical velocity
                new_vy = -self.MIN_Y_VELOCITY if new_vy < 0 else self.MIN_Y_VELOCITY
            if new_vy > 0:  # Ensure that the ball is always moving upwards after hitting the paddle
                new_vy = -new_vy
            ball.velocity = pg.math.Vector2(new_vx, new_vy)
        elif not pg.sprite.collide_rect(ball, self.paddle):
            self.paddle_hit_dict[ball_id] = False

    def check_wall_collision(self, ball: Ball) -> None:
        """
        Checks for collision with the walls and updates the ball's velocity accordingly.
        
        Args:
            ball (Ball): The ball to check collision for.
        """
        if ball.rect.left <= 0 or ball.rect.right >= self.screen_width:
            self.bounce(ball, pg.math.Vector2(1, 0))
        if ball.rect.top <= 0:
            self.bounce(ball, pg.math.Vector2(0, 1))

        if ball.rect.bottom >= self.screen_height:
            # Remove this ball from the list
            if ball in self.balls:
                self.balls.remove(ball)
                # Clean up paddle hit tracking
                ball_id = id(ball)
                if ball_id in self.paddle_hit_dict:
                    del self.paddle_hit_dict[ball_id]
            
            # If no balls left, respawn one and lose a life
            if len(self.balls) == 0:
                new_ball = Ball(self.paddle)
                self.balls.append(new_ball)
                self.lives.lives -= 1

    def check_brick_collision(self, ball: Ball) -> None:
        """
        Checks for collision with the bricks and updates the ball's velocity accordingly.
        Uses optimized row-based collision detection.
        
        Args:
            ball (Ball): The ball to check collision for.
        """
        # Get only the rows where the ball is or will be
        rows_to_check = self.level.get_ball_collision_rows(ball.rect, ball.velocity)
        
        # Only check bricks in relevant rows
        for row_index in rows_to_check:
            if row_index not in self.level.brick_rows:
                continue
                
            for brick in self.level.brick_rows[row_index]:
                if not brick.is_destroyed and pg.sprite.collide_rect(ball, brick):
                    collision_normal = pg.math.Vector2()
                    if ball.velocity.x > 0 and ball.rect.right >= brick.rect.left:
                        collision_normal.x = -1
                    elif ball.velocity.x < 0 and ball.rect.left <= brick.rect.right:
                        collision_normal.x = 1
                    if ball.velocity.y > 0 and ball.rect.bottom >= brick.rect.top:
                        collision_normal.y = -1
                    elif ball.velocity.y < 0 and ball.rect.top <= brick.rect.bottom:
                        collision_normal.y = 1
                    self.bounce(ball, collision_normal)
                    brick.is_destroyed = True
                    self.scoreboard.score += 10
                    
                    # Remove brick from sprite group and brick_rows
                    self.bricks.remove(brick)
                    if row_index in self.level.brick_rows:
                        if brick in self.level.brick_rows[row_index]:
                            self.level.brick_rows[row_index].remove(brick)
                    
                    # Spawn a ball if this was a moving brick
                    if isinstance(brick, MovingBrick):
                        self.spawn_ball_from_brick(brick)
                    
                    break  # Only process one brick collision per frame

    def spawn_ball_from_brick(self, brick: Brick) -> None:
        """
        Spawns a new ball from the destroyed moving brick's location.
        
        Args:
            brick (Brick): The brick that was destroyed.
        """
        # Create new ball at brick center
        new_ball = Ball(self.paddle)
        new_ball.position = pg.math.Vector2(brick.rect.centerx, brick.rect.centery)
        new_ball.rect.center = new_ball.position
        new_ball.attached_to_paddle = False
        
        # Give it a random downward velocity
        angle = random.uniform(60, 120)  # Angle between 60 and 120 degrees (downward)
        new_ball.velocity = pg.math.Vector2(self.BALL_SPEED, 0).rotate(-angle)
        
        # Add to balls list
        self.balls.append(new_ball)

    def bounce(self, ball: Ball, collision_normal: pg.math.Vector2) -> None:
        """
        Adjusts the ball's velocity based on the collision normal.

        Args:
            ball (Ball): The ball to bounce.
            collision_normal (pg.math.Vector2): The normal vector of the collision surface.
        """
        ball.velocity = ball.velocity.reflect(collision_normal)
        angle_variation = random.uniform(-5, 5)
        angle_rad = math.radians(angle_variation)
        ball.velocity = ball.velocity.rotate(angle_rad)
        ball.spin += angle_variation * 0.75
        if abs(ball.velocity[1]) < self.MIN_Y_VELOCITY:
            ball.velocity[1] = self.MIN_Y_VELOCITY if ball.velocity[1] > 0 else -self.MIN_Y_VELOCITY

    def check_ball_stuck(self, ball: Ball) -> None:
        """
        Checks if the ball is stuck and adjusts its velocity accordingly.
        
        Args:
            ball (Ball): The ball to check.
        """
        # If vertical speed is zero or extremely small, push the ball away from borders
        if abs(ball.velocity[1]) < 0.05:
            if ball.rect.top <= 0:
                ball.velocity[1] = self.BALL_SPEED  # push downward when stuck on top
            elif ball.rect.bottom >= self.screen_height:
                ball.velocity[1] = -self.BALL_SPEED  # push upward when stuck on bottom
            else:
                ball.velocity[1] = self.BALL_SPEED if ball.rect.centery < self.screen_height // 2 else -self.BALL_SPEED

        # Nudge the ball inside the playfield if clipped into the top or bottom wall
        if ball.rect.top <= 0:
            ball.rect.top = 1
            ball.position.y = ball.rect.centery
            if ball.velocity[1] < self.MIN_Y_VELOCITY:
                ball.velocity[1] = self.MIN_Y_VELOCITY
        if ball.rect.bottom >= self.screen_height:
            ball.rect.bottom = self.screen_height - 1
            ball.position.y = ball.rect.centery
            if ball.velocity[1] > -self.MIN_Y_VELOCITY:
                ball.velocity[1] = -self.MIN_Y_VELOCITY

        if abs(ball.velocity[0]) < 0.05 and (ball.rect.left <= 0 or ball.rect.right >= self.screen_width):
            ball.velocity[0] = self.BALL_SPEED if ball.rect.centerx < self.screen_width // 2 else -self.BALL_SPEED

    def check_ball_ball_collision(self) -> None:
        """
        Checks for collisions between balls and makes them bounce off each other.
        Preserves the speed (magnitude) of each ball.
        """
        if len(self.balls) < 2:
            return
        
        # Check each pair of balls only once
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                
                # Skip if either ball is attached to paddle
                if ball1.attached_to_paddle or ball2.attached_to_paddle:
                    continue
                
                # Calculate distance between centers
                dx = ball2.position.x - ball1.position.x
                dy = ball2.position.y - ball1.position.y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Check if balls are colliding (distance less than sum of radii)
                if distance < self.BALL_RADIUS * 2 and distance > 0:
                    # Calculate collision normal (direction from ball1 to ball2)
                    normal = pg.math.Vector2(dx / distance, dy / distance)
                    
                    # Separate balls to prevent overlap
                    overlap = self.BALL_RADIUS * 2 - distance
                    separation = normal * (overlap / 2 + 0.5)
                    ball1.position -= separation
                    ball2.position += separation
                    ball1.rect.center = ball1.position
                    ball2.rect.center = ball2.position
                    
                    # Calculate relative velocity
                    relative_velocity = ball1.velocity - ball2.velocity
                    velocity_along_normal = relative_velocity.dot(normal)
                    
                    # Only resolve if balls are moving towards each other
                    if velocity_along_normal > 0:
                        # Store original speeds to preserve them
                        speed1 = ball1.velocity.length()
                        speed2 = ball2.velocity.length()
                        
                        # Reflect velocities along collision normal
                        ball1.velocity -= normal * velocity_along_normal
                        ball2.velocity += normal * velocity_along_normal
                        
                        # Restore original speeds (preserve momentum)
                        if ball1.velocity.length() > 0:
                            ball1.velocity.scale_to_length(speed1)
                        if ball2.velocity.length() > 0:
                            ball2.velocity.scale_to_length(speed2)

    def update(self) -> None:
        """
        Updates the collision detection for all balls.
        """
        for ball in self.balls[:]:  # Use slice to avoid modification during iteration
            self.check_wall_collision(ball)
            self.check_paddle_collision(ball)
            self.check_brick_collision(ball)
            self.check_ball_stuck(ball)
        
        # Check ball-to-ball collisions after all individual ball checks
        self.check_ball_ball_collision()
