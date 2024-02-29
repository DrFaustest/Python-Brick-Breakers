import pygame as pg
from settings import *

class Paddle(pg.sprite.Sprite):
    def __init__(self) -> None:
        """
        Initialize the Paddle object.

        This method loads the paddle image, scales it to the specified size,
        sets the initial position of the paddle, and initializes other attributes.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.original_image = pg.image.load(PADDLE_IMG)
        self.image = pg.transform.scale(self.original_image, (PADDLE_SIZE[0], PADDLE_SIZE[1]))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PADDLE_SIZE[0] // 2
        self.rect.y = SCREEN_HEIGHT - 60
        self.speed = PADDLE_SPEED
        self.screen_width = SCREEN_WIDTH
        self.position_accumulator = SCREEN_WIDTH // 2  # Floating-point accumulator for precise movement

    def move(self, direction) -> None:
        """
        Move the paddle in the specified direction.

        This method updates the position of the paddle based on the specified direction.
        It also handles boundary conditions to prevent the paddle from moving off the screen.

        Args:
            direction (str): The direction in which to move the paddle. Can be "left" or "right".

        Returns:
            None
        """
        if direction == "left":
            self.position_accumulator -= self.speed
        elif direction == "right":
            self.position_accumulator += self.speed

        self.rect.x = int(self.position_accumulator)

        if self.rect.x < 0:
            self.rect.x = 0
            self.position_accumulator = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.position_accumulator = self.screen_width - self.rect.width

    def draw(self, screen) -> None:
        """
        Draw the paddle on the screen.

        This method blits the paddle image onto the specified screen surface at the current position.

        Args:
            screen (pygame.Surface): The surface on which to draw the paddle.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)
