from settings import *
import levels.brick_map as brick_map
from objects.brick import Brick

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
        - bricks (list): The list of Brick objects in the level.
        - level_complete (bool): Indicates if the level is complete.
        """
        self.current_level = current_level
        self.level_name = current_level + 1
        self.level_map = brick_map.generate_brick_map()
        self.bricks = []
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
                    self.bricks.append(brick)
    
    def create_brick(self, x_index, y_index):
        """
        Creates a Brick object at the specified position.

        Parameters:
        - x_index (int): The x-index of the brick in the level map.
        - y_index (int): The y-index of the brick in the level map.

        Returns:
        - Brick: The created Brick object.
        """
        x, y = x_index * BRICK_SIZE[0], y_index * BRICK_SIZE[1]
        return Brick(x, y)

    def draw(self, screen):
        """
        Draws the non-destroyed bricks on the screen.

        Parameters:
        - screen: The screen to draw on.
        """
        for brick in self.bricks:
            if not brick.is_destroyed:
                brick.draw(screen)

    def is_level_complete(self):
        """
        Checks if all bricks in the level are destroyed.

        Returns:
        - bool: True if all bricks are destroyed, False otherwise.
        """
        return all(brick.is_destroyed for brick in self.bricks)
