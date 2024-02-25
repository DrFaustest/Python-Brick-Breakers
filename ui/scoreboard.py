import pygame as pg
from settings import *

class Scoreboard:
    def __init__(self, font_size=30, color=WHITE):
        """
        Initialize the Scoreboard object.

        Args:
            font_size (int): The font size of the score text. Default is 30.
            color (tuple): The color of the score text. Default is WHITE.
        """
        self.score = 0
        self.font = pg.font.SysFont(None, font_size)
        self.color = color
        self.x = SCREEN_WIDTH - 120
        self.y = SCREEN_HEIGHT - 25

    def increase_score(self, points=10):
        """
        Increase the score by the specified number of points.

        Args:
            points (int): The number of points to increase the score by. Default is 10.
        """
        self.score += points

    def decrease_score(self, points=10):
        """
        Decrease the score by the specified number of points.

        Args:
            points (int): The number of points to decrease the score by. Default is 10.
        """
        self.score -= points

    def draw(self, screen):
        """
        Draw the score on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the score on.
        """
        score_text = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_text, (self.x, self.y))