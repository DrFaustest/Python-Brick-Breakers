#this file houses all of the commonly used objects in the game
from settings import *
import pygame as pg
import math
import json

class Button:
    def __init__(self, x, y, width = 200, height = 100, text = "Change ME", color =(WHITE) , hover_color = (0, 255, 0), text_color = (BLACK), action = None):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.font = pg.font.SysFont("Arial", 50)
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.color

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                if self.action is not None:
                    self.action()

class Paddle:
    def __init__(self, x, y, width, height, SCREEN_WIDTH, color=(WHITE)):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.speed = PADDLE_SPEED
        self.screen_width = SCREEN_WIDTH
        self.position_accumulator = x  # Floating-point accumulator for precise movement

    def move(self, direction):
        if direction == "left":
            self.position_accumulator -= self.speed
        elif direction == "right":
            self.position_accumulator += self.speed

        # Update rect position with truncated value of accumulator
        self.rect.x = int(self.position_accumulator)

        # Boundary checks
        if self.rect.x < 0:
            self.rect.x = 0
            self.position_accumulator = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.position_accumulator = self.screen_width - self.rect.width


    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, paddle, radius=10, color=(WHITE)):
        self.radius = radius
        self.color = color
        self.paddle = paddle
        self.x = paddle.rect.centerx
        self.y = paddle.rect.top - radius
        self.rect = pg.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        self.speed_x = 0
        self.speed_y = 0
        self.attached_to_paddle = True

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.attached_to_paddle:
            self.speed_x = BALL_SPEED
            self.speed_y = -BALL_SPEED
            self.attached_to_paddle = False

    def update(self):
        if self.attached_to_paddle:
            self.x = self.paddle.rect.centerx
            self.y = self.paddle.rect.top - self.radius
        else:
            self.x += self.speed_x
            self.y += self.speed_y

        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Red color (you can change this)
        self.is_destroyed = False  # A flag to track if the brick is destroyed

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

    def destroy(self):
        self.is_destroyed = True
        self.color = (0, 0, 0)  # Black color


class Level:
    def __init__(self, current_level):
        with open("levels.json", "r") as file:
            all_levels = json.load(file)["levels"]
        if current_level < len(all_levels):
            self.level_data = all_levels[current_level]
        else:
            print("All levels are complete")
            raise ValueError("Level does not exist")

        self.level_name = self.level_data['name']
        self.level_map = self.level_data['layout']
        self.bricks = []
        self.level_complete = False
        self.load_level(self.level_map)

    def load_level(self, level_data):
        screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        brick_width, brick_height = screen_width // len(level_data[0]), (screen_height // len(level_data)) //2

        for row_index, row in enumerate(level_data):
            for col_index, col in enumerate(row):
                if col == 1:
                    brick = self.create_brick(col_index, row_index, brick_width, brick_height)
                    self.bricks.append(brick)
    

    def create_brick(self, x_index, y_index, brick_width, brick_height):
        x, y = x_index * brick_width, y_index * brick_height
        return Brick(x, y, brick_width, brick_height)

    def draw(self, screen):
        for brick in self.bricks:
            if not brick.is_destroyed:
                brick.draw(screen)

    def is_level_complete(self):
        return all(brick.is_destroyed for brick in self.bricks)

    # Add other methods like update, collision detection, etc.


class Scoreboard:
    def __init__(self, x, y, font_size=30, color=(255, 255, 255)):
        self.score = 0
        self.font = pg.font.SysFont(None, font_size)
        self.color = color
        self.x = x
        self.y = y

    def increase_score(self, points=10):
        # Increase the score by the given number of points
        self.score += points

    def update(self):
        # This method can be used to update any other information on the scoreboard if needed
        pass

    def draw(self, screen):
        # Render the score and draw it on the screen
        score_text = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_text, (self.x, self.y))

class Collision:
    def __init__(self, ball, paddle, bricks):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def check_wall_collision(self):
        # Check for collision with left, right, and top walls
        if self.ball.rect.left <= 0 or self.ball.rect.right >= self.screen_width:
            self.ball.speed_x *= -1  # Reverse horizontal direction
        if self.ball.rect.top <= 0:
            self.ball.speed_y *= -1  # Reverse vertical direction

        # Add bottom wall collision if needed (usually results in game over)

    def check_paddle_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y *= -1  # Reverse vertical direction

    def check_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed and self.ball.rect.colliderect(brick.rect):
                self.ball.speed_y *= -1  # Reverse vertical direction
                brick.is_destroyed = True  # Mark the brick as destroyed
                break


    def update(self):
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()

    
class InputEvent:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[KEY_MOVE_LEFT]:
            self.paddle.move("left")
        elif keys[KEY_MOVE_RIGHT]:
            self.paddle.move("right")
        if keys[pg.K_SPACE]:
            self.ball.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE))

class LevelBanner:
    def __init__(self, font_size=50, color=(255, 255, 255)):
        self.font = pg.font.SysFont("Arial", font_size)
        self.color = color

    def display(self, screen, level_number, screen_width, screen_height):
        level_text = self.font.render(f"Level {level_number}", True, self.color)
        text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(level_text, text_rect)
        pg.display.flip()  # Update the display
        pg.time.wait(2000)  # Wait for a couple of seconds

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
        self.game.ball.y = self.game.paddle.rect.top - self.game.ball.radius
        self.game.ball.speed_x = 0
        self.game.ball.speed_y = 0
        self.game.ball.attached_to_paddle = True

        # Reset collision detection with the new bricks
        self.game.collision = Collision(self.game.ball, self.game.paddle, self.game.bricks)


