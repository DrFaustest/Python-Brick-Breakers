import pygame as pg
from settings import Settings

class Scoreboard:
    def __init__(self, font_size: int = 30, color: tuple = (255, 255, 255)):
        """
        Initialize the Scoreboard object.

        Args:
            font_size (int): The font size of the score text. Default is 30.
            color (tuple): The color of the score text. Default is WHITE.
        """
        self.settings = Settings()
        self.SCREEN_WIDTH: int = self.settings.get("SCREEN_WIDTH")
        self.SCREEN_HEIGHT: int = self.settings.get("SCREEN_HEIGHT")
        self.score: int = 0
        self.font: pg.font.Font = pg.font.SysFont(None, font_size)
        self.color: tuple = color
        self.x: int = self.SCREEN_WIDTH - 120
        self.y: int = self.SCREEN_HEIGHT - 25

    def increase_score(self, points: int = 10) -> None:
        """
        Increase the score by the specified number of points.

        Args:
            points (int): The number of points to increase the score by. Default is 10.
        """
        self.score += points

    def decrease_score(self, points: int = 10) -> None:
        """
        Decrease the score by the specified number of points.

        Args:
            points (int): The number of points to decrease the score by. Default is 10.
        """
        self.score -= points

    def draw(self, screen: pg.Surface) -> None:
        """
        Draw the score on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the score on.
        """
        score_text = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_text, (self.x, self.y))
