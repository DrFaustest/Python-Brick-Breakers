import pygame as pg
from settings import *

class Brick:
    image = pg.image.load(BRICK_IMG)
    image = pg.transform.scale(image, (BRICK_WIDTH, BRICK_HEIGHT))
    
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.is_destroyed = False  # A flag to track if the brick is destroyed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def destroy(self):
        self.is_destroyed = True