#this file houses all of the commonly used objects in the game

import pygame as pg

class Button:
    def __init__(self, x, y, width = 200, height = 100, text = "Change ME", color =(255,255,255) , hover_color = (0, 255, 0), text_color = (0, 0, 0), action = None):
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
    def __init__(self, x, y, width, height, screen_width, color=(255, 255, 255)):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.speed = 1
        self.screen_width = screen_width

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < 0:  # Check for left boundary
                self.rect.x = 0
        elif direction == "right":
            self.rect.x += self.speed
            if self.rect.right > self.screen_width:  # Check for right boundary
                self.rect.right = self.screen_width

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, paddle, radius=10, color=(255, 255, 255)):
        self.radius = radius
        self.color = color
        self.paddle = paddle
        self.x = paddle.rect.centerx
        self.y = paddle.rect.top - radius
        self.rect = pg.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        self.speed_x = 1
        self.speed_y = 1
        self.attached_to_paddle = True

    def handle_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.attached_to_paddle:
            self.speed_x = 0.1  # You can adjust the initial speed and direction
            self.speed_y = -0.1
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

        # Add collision detection with walls, paddle, and bricks here

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


class Level:
    def __init__(self, level_data):
        self.bricks = []  # List to store the bricks in the level
        self.load_level(level_data)
        self.level_complete = False

    def load_level(self, level_data):
        if self.bricks is not None:
            screen_width, screen_height = 800, 600
            brick_width, brick_height = screen_width // 5, screen_height // 10
            for row_index, row in enumerate(level_data):
                for col_index, col in enumerate(row):
                    if col == 1:
                        brick = self.create_brick(col_index, row_index, brick_width, brick_height)
                        self.bricks.append(brick)
        else:
            return

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
    def __init__(self, ball, paddle, bricks, screen_width, screen_height):
        self.ball = ball
        self.paddle = paddle
        self.bricks = bricks
        self.screen_width = screen_width
        self.screen_height = screen_height

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

            # Optional: Adjust ball's horizontal speed based on where it hits the paddle

    def check_brick_collision(self):
        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                print("collision")
                self.ball.speed_y *= -1  # Reverse vertical direction
                self.bricks.is_destroyed = True  # Destroy the brick
                self.level.draw(self.screen)  # Redraw the new brick layout
                break  # Assuming one collision per update

    def update(self):
        self.check_wall_collision()
        self.check_paddle_collision()
        self.check_brick_collision()
