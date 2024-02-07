# settings.py
import pygame as pg
import math

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 100
BRICK_HEIGHT = 20

# Key bindings
KEY_MOVE_LEFT = pg.K_LEFT  # Update with the actual key code or name
KEY_MOVE_RIGHT = pg.K_RIGHT  # Update with the actual key code or name
KEY_PAUSE = pg.K_p  # Update with the actual key code or name
KEY_QUIT = pg.K_DELETE  # Update with the actual key code or name

# Game settings+
FPS = 60  # Frames per second
PADDLE_SPEED = .5  # Update with the actual speed value
BALL_SPEED = .4  # Update with the actual speed value
DIFFICULTY = 1  # Update with the changeable difficulty level

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_REFLECTION_ANGLE = 90 # Maximum reflection angle for paddle collision
