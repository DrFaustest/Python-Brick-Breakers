# settings.py
import pygame as pg
import math

# Screen dimensions
SCALE = 1
SCREEN_WIDTH = 800 * SCALE
SCREEN_HEIGHT = 600 * SCALE
BRICK_SIZE = (100 * SCALE, 20 * SCALE)


# Key bindings
KEY_MOVE_LEFT = pg.K_LEFT 
KEY_MOVE_RIGHT = pg.K_RIGHT  
KEY_PAUSE = pg.K_p 
KEY_QUIT = pg.K_DELETE 

# Game settings+
FPS = 120  # Frames per second
PADDLE_SPEED = 25
PADDLE_SIZE = (100 * SCALE, 20 * SCALE)
BALL_SPEED = 5
DIFFICULTY = 1  
VOLUME = .5 
# Colors (RGB)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

MAX_REFLECTION_ANGLE = 90
MIN_Y_VELOCITY = -1.5
BALL_RADIUS = 30 * SCALE / 2

BALL_IMG = "img/retro_snow_ball.png"
PADDLE_IMG = "img/paddle.png"
BRICK_IMG = "img/brick_img.png"
BACKGROUND_IMG = "img/background_4.webp"
SOUND_ENABLED_IMAGE = "img/sound_image.png"
SOUND_DISABLED_IMAGE = "img/sound_muted.png"