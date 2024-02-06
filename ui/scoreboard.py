import pygame as pg
from settings import *

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

    def decrease_score(self, points=10):
        # Decrease the score by the given number of points
        self.score -= points

    def update(self):
        # This method can be used to update any other information on the scoreboard if needed
        pass

    def draw(self, screen):
        # Render the score and draw it on the screen
        score_text = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_text, (self.x, self.y))