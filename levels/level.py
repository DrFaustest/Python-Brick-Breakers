from settings import Settings
from objects.brick import Brick
import pygame
import random

class Level:
    def __init__(self, current_level):
        """
        Initializes a Level object.

        Parameters:
        - current_level (int): The current level number.

        Attributes:
        - current_level (int): The current level number.
        - level_name (int): The level name (current_level + 1).
        - level_map (list): The map of bricks for the level.
        - bricks (pygame.sprite.Group): The group of Brick objects in the level.
        - level_complete (bool): Indicates if the level is complete.
        """
        self.settings = Settings()
        self.BRICK_SIZE = self.settings.get("BRICK_SIZE")
        self.current_level = current_level
        self.level_name = current_level + 1
        self.level_map = self.generate_brick_map()
        self.bricks = pygame.sprite.Group()
        self.level_complete = False
        self.load_level(self.level_map)

    def load_level(self, level_data):
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
    
    def create_brick(self, x_index, y_index):
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

    def draw(self, screen):
        """
        Draws the non-destroyed bricks on the screen.

        Parameters:
        - screen: The screen to draw on.
        """
        self.bricks.draw(screen)

    def is_level_complete(self):
        """
        Checks if all bricks in the level are destroyed.

        Returns:
        - bool: True if all bricks are destroyed, False otherwise.
        """
        return all(brick.is_destroyed for brick in self.bricks)
    
    def generate_brick_map(self):
        """
        Generates a brick map based on the game settings and difficulty level.

        Returns:
        - grid (list): A 2D list representing the brick map, where 0 represents an empty space and 1 represents a brick.
        """
        settings = Settings()
        SCREEN_WIDTH = settings.get("SCREEN_WIDTH")
        SCREEN_HEIGHT = settings.get("SCREEN_HEIGHT")
        BRICK_SIZE = settings.get("BRICK_SIZE")
        DIFFICULTY = settings.get("DIFFICULTY")
        # Determine max bricks and percentage of bricks to be generated
        max_bricks_x = SCREEN_WIDTH // BRICK_SIZE[0]
        max_bricks_y = (SCREEN_HEIGHT // 2) // BRICK_SIZE[1]
        total_bricks = int((max_bricks_x * max_bricks_y) * (DIFFICULTY / 10))
        # Generate the brick map with random brick positions
        grid = [[0 for _ in range(max_bricks_x)] for _ in range(max_bricks_y)]
        brick_positions = set()
        while len(brick_positions) < total_bricks:
            x = random.randint(0, max_bricks_x - 1)
            y = random.randint(0, max_bricks_y - 1)
            brick_positions.add((x, y))
        for x, y in brick_positions:
            grid[y][x] = 1
        return grid
