import pygame as pg
from settings import Settings
class Brick(pg.sprite.Sprite):
    """
    Represents a brick object in the game.

    Attributes:
        rect (pygame.Rect): The rectangular area occupied by the brick.
        is_destroyed (bool): A flag to track if the brick is destroyed.

    Methods:
        __init__(x, y): Initializes a new instance of the Brick class.
        update(): Updates the state of the brick.
        draw(screen): Draws the brick on the screen.
        destroy(): Marks the brick as destroyed.
    """

    def __init__(self, x, y):
        """
        Initializes a new instance of the Brick class.

        Args:
            x (int): The x-coordinate of the top-left corner of the brick.
            y (int): The y-coordinate of the top-left corner of the brick.
        """
        super().__init__()
        self.settings = Settings()
        self.BRICK_IMG = self.settings.get("BRICK_IMG")
        self.BRICK_SIZE = self.settings.get("BRICK_SIZE")
        self.image = pg.image.load(self.BRICK_IMG)
        self.image = pg.transform.scale(self.image, (self.BRICK_SIZE[0], self.BRICK_SIZE[1]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_destroyed = False

    def update(self):
        """
        Updates the state of the brick.
        """
        pass

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
        self.kill()
