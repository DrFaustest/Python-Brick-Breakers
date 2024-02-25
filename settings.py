# settings.py

import pygame as pg

# Screen dimensions
SCALE = 1
SCREEN_WIDTH = 800 * SCALE
SCREEN_HEIGHT = 600 * SCALE
BRICK_SIZE = (100 * SCALE, 20 * SCALE)
BACKGROUND_IMAGES = ["img/background.webp", "img/background_2.webp", "img/background_3.webp", "img/background_4.webp"]
BRICK_IMAGES = ["img/brick_img.png", "img/brick_img1.png"]
BALL_IMAGES = ["img/future_ball.png","img/retro_snow_ball.png","img/ring_ball.png"]
PADDLE_IMAGES = ["img/paddle.png"]

# Key bindings
KEY_MOVE_LEFT = pg.K_LEFT 
KEY_MOVE_RIGHT = pg.K_RIGHT  
KEY_PAUSE = pg.K_p 
KEY_QUIT = pg.K_DELETE 

# Game settings
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

BALL_IMG = BALL_IMAGES[0]
PADDLE_IMG = PADDLE_IMAGES[0]
BRICK_IMG = BRICK_IMAGES[0]
BACKGROUND_IMG = BACKGROUND_IMAGES[0]
SOUND_ENABLED_IMAGE = "img/sound_image.png"
SOUND_DISABLED_IMAGE = "img/sound_muted.png"