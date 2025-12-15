import pygame as pg
from settings import Settings
from objects.brick import Brick
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from levels.level import Level

class MovingBrick(Brick):
    """
    Represents a moving brick that travels horizontally across the screen.

    Attributes:
        velocity (int): The horizontal velocity of the brick.
        row_index (int): The row this brick belongs to.
        level (Level): Reference to the level for collision detection.
        is_frozen (bool): Whether the brick is frozen due to row density.
        collision_cooldown (int): Frames to wait before checking collision again.

    Methods:
        __init__(x, y, row_index, level): Initializes a new MovingBrick.
        update(): Updates the brick's position and handles collisions.
        check_wall_collision(): Checks if the brick hits screen boundaries.
        check_potential_collision(): Predicts if brick will collide next frame.
        should_be_frozen(): Determines if brick should freeze based on row density.
    """

    def __init__(self, x: int, y: int, row_index: int, level: 'Level') -> None:
        """
        Initializes a new instance of the MovingBrick class.

        Args:
            x: The x-coordinate of the top-left corner of the brick.
            y: The y-coordinate of the top-left corner of the brick.
            row_index: The row this brick belongs to.
            level: Reference to the level for collision detection.
        """
        super().__init__(x, y)
        self.settings = Settings()
        self.SCREEN_WIDTH: int = self.settings.get("SCREEN_WIDTH")
        self.BRICK_SIZE: list = self.settings.get("BRICK_SIZE")
        self.velocity: int = 3  # Horizontal movement speed
        self.row_index: int = row_index
        self.level = level
        self.is_frozen: bool = False
        self.collision_cooldown: int = 0  # Prevent rapid collision toggles
        # Randomly start moving left or right
        import random
        self.velocity *= random.choice([-1, 1])

    def update(self) -> None:
        """
        Updates the brick's position and handles collisions.
        """
        if self.is_destroyed:
            return

        # Decrease collision cooldown
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        # Check if brick should be frozen based on row density
        self.is_frozen = self.should_be_frozen()
        
        if not self.is_frozen:
            # Check for potential collisions in the direction we're moving
            will_collide = self.check_potential_collision()
            
            if will_collide and self.collision_cooldown == 0:
                # Reverse direction and set cooldown
                self.velocity *= -1
                self.collision_cooldown = 10  # Wait 10 frames before next collision
            else:
                # Move the brick
                self.rect.x += self.velocity
            
            # Check collisions with walls
            self.check_wall_collision()
        
        # Call parent update for any base class functionality
        super().update()

    def check_wall_collision(self) -> None:
        """
        Checks if the brick hits screen boundaries and reverses direction.
        """
        if self.rect.left <= 0:
            self.velocity = abs(self.velocity)  # Ensure moving right
            self.rect.left = 0
            self.collision_cooldown = 5
        elif self.rect.right >= self.SCREEN_WIDTH:
            self.velocity = -abs(self.velocity)  # Ensure moving left
            self.rect.right = self.SCREEN_WIDTH
            self.collision_cooldown = 5

    def check_potential_collision(self) -> bool:
        """
        Checks if the brick will collide with another brick in the next frame.
        
        Returns:
            bool: True if a collision is imminent, False otherwise.
        """
        if self.row_index not in self.level.brick_rows:
            return False

        # Create a test rect for the next position
        test_rect = self.rect.copy()
        test_rect.x += self.velocity
        
        for brick in self.level.brick_rows[self.row_index]:
            if brick is not self and not brick.is_destroyed:
                # Check if the test position overlaps with another brick
                if test_rect.colliderect(brick.rect):
                    return True
        
        return False

    def should_be_frozen(self) -> bool:
        """
        Determines if brick should freeze based on row density.
        If more than half the possible brick positions in the row are occupied, freeze.

        Returns:
            bool: True if brick should be frozen, False otherwise.
        """
        if self.row_index not in self.level.brick_rows:
            return False

        # Count active (non-destroyed) bricks in this row
        active_bricks = sum(1 for brick in self.level.brick_rows[self.row_index] 
                           if not brick.is_destroyed)
        
        # Get max possible bricks in a row
        max_bricks_in_row = self.level.max_bricks_x
        
        # Freeze if more than half the row is filled
        return active_bricks > (max_bricks_in_row / 2)
