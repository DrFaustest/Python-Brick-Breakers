from settings import Settings
from objects.brick import Brick
import pygame
import random
from typing import List, Tuple

class Level:
    def __init__(self, current_level: int) -> None:
        """
        Initializes a Level object.

        Parameters:
        - current_level (int): The current level number.
        """
        self.settings = Settings()
        self.BRICK_SIZE: Tuple[int, int] = self.settings.get("BRICK_SIZE")
        self.current_level: int = current_level
        self.level_name: int = current_level + 1
        self.level_map: List[List[int]] = self.generate_brick_map()
        self.bricks: pygame.sprite.Group = pygame.sprite.Group()
        self.level_complete: bool = False
        self.load_level(self.level_map)

    def load_level(self, level_data: List[List[int]]) -> None:
        """
        Loads the level by creating bricks based on the level data.

        Parameters:
        - level_data (list): The map of bricks for the level.
        """
        for row_index, row in enumerate(level_data):
            for col_index, col in enumerate(row):
                if col == 1:
                    brick = self.create_brick(col_index, row_index)
                    self.bricks.add(brick)
    
    def create_brick(self, x_index: int, y_index: int) -> Brick:
        """
        Creates a Brick object at the specified position.

        Parameters:
        - x_index (int): The x-index of the brick in the level map.
        - y_index (int): The y-index of the brick in the level map.

        Returns:
        - Brick: The created Brick object.
        """
        x, y = x_index * self.BRICK_SIZE[0], y_index * self.BRICK_SIZE[1]
        return Brick(x, y)

    def draw(self, screen) -> None:
        """
        Draws the non-destroyed bricks on the screen.

        Parameters:
        - screen: The screen to draw on.
        """
        self.bricks.draw(screen)

    def is_level_complete(self) -> bool:
        """
        Checks if all bricks in the level are destroyed.

        Returns:
        - bool: True if all bricks are destroyed, False otherwise.
        """
        return all(brick.is_destroyed for brick in self.bricks)
    
    def generate_brick_map(self) -> List[List[int]]:
        """
        Generates a brick map based on the game settings and difficulty level.

        Returns:
        - grid (list): A 2D list representing the brick map, where 0 represents an empty space and 1 represents a brick.
        """
        settings = Settings()
        SCREEN_WIDTH: int = settings.get("SCREEN_WIDTH")
        SCREEN_HEIGHT: int = settings.get("SCREEN_HEIGHT")
        BRICK_SIZE: Tuple[int, int] = settings.get("BRICK_SIZE")
        DIFFICULTY: int = settings.get("DIFFICULTY")
        # Determine max bricks and percentage of bricks to be generated
        max_bricks_x: int = SCREEN_WIDTH // BRICK_SIZE[0]
        max_bricks_y: int = (SCREEN_HEIGHT // 2) // BRICK_SIZE[1]
        total_bricks: int = int((max_bricks_x * max_bricks_y) * (DIFFICULTY / 10))
        # Generate the brick map with random brick positions
        grid: List[List[int]] = [[0 for _ in range(max_bricks_x)] for _ in range(max_bricks_y)]
        brick_positions: set = set()
        while len(brick_positions) < total_bricks:
            x: int = random.randint(0, max_bricks_x - 1)
            y: int = random.randint(0, max_bricks_y - 1)
            brick_positions.add((x, y))
        for x, y in brick_positions:
            grid[y][x] = 1
        return grid
