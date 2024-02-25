import pygame as pg
from settings import *

class Paddle:
    def __init__(self) -> None:
        """
        Initializes a Paddle object.

        The Paddle object represents the player's paddle in the game.
        It loads the paddle image, sets its initial position, speed, and other attributes.

        Args:
            None

        Returns:
            None
        """
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
        Moves the paddle in the specified direction.

        Args:
            direction (str): The direction to move the paddle. Can be "left" or "right".

        Returns:
            None
        """
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


    def draw(self, screen) -> None:
        """
        Draws the paddle on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the paddle on.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)