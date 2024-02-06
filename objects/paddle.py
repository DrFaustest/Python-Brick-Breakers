import pygame as pg
from settings import *

class Paddle:
    def __init__(self):
        self.rect = pg.Rect(350, 550, 100, 20)
        self.color = WHITE
        self.speed = PADDLE_SPEED
        self.screen_width = SCREEN_WIDTH
        self.position_accumulator = 350  # Floating-point accumulator for precise movement

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