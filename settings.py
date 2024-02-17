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
FPS = 120  # Frames per second
PADDLE_SPEED = 25  # Update with the actual speed value
BALL_SPEED = 5 # Update with the actual speed value
DIFFICULTY = 1  # Update with the changeable difficulty level
VOLUME = .5  # Update with the actual volume level
# Colors (RGB)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

MAX_REFLECTION_ANGLE = 75 # Maximum reflection angle for paddle collision
BALL_RADIUS = 15  # Update with the actual radius value

BALL_IMG = "img/retro_snow_ball.png"
PADDLE_IMG = "img/paddle.png"
BRICK_IMG = "img/brick_img.png"
BACKGROUND_IMG = "img/background_4.webp"
SOUND_ENABLED_IMAGE = "img/sound_image.png"
SOUND_DISABLED_IMAGE = "img/sound_muted.png"