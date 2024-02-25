import pygame as pg
from settings import *

class Brick:
    """
    Represents a brick object in the game.

    Attributes:
        rect (pygame.Rect): The rectangular area occupied by the brick.
        is_destroyed (bool): A flag to track if the brick is destroyed.

    Methods:
        draw(screen): Draws the brick on the screen.
        destroy(): Marks the brick as destroyed.
    """

    image = pg.image.load(BRICK_IMG)
    image = pg.transform.scale(image, (BRICK_SIZE[0], BRICK_SIZE[1]))
    
    def __init__(self, x, y):
        """
        Initializes a new instance of the Brick class.

        Args:
            x (int): The x-coordinate of the top-left corner of the brick.
            y (int): The y-coordinate of the top-left corner of the brick.
        """
        self.rect = pg.Rect(x, y, BRICK_SIZE[0], BRICK_SIZE[1])
        self.is_destroyed = False

    def draw(self, screen):
        """
        Draws the brick on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the brick on.
        """
        screen.blit(self.image, self.rect)

    def destroy(self):
        """
        Marks the brick as destroyed.
        """
        self.is_destroyed = True