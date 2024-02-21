from settings import *
import levels.brick_map as brick_map
from objects.brick import Brick

class Level:
    def __init__(self, current_level):
        self.current_level = current_level
        self.level_name = current_level+1
        self.level_map = brick_map.generate_brick_map()
        self.bricks = []
        self.level_complete = False
        self.load_level(self.level_map)

    def load_level(self, level_data):
        # Create bricks based on the level data
        for row_index, row in enumerate(level_data):
            for col_index, col in enumerate(row):
                if col == 1:
                    brick = self.create_brick(col_index, row_index)
                    self.bricks.append(brick)
    
    def create_brick(self, x_index, y_index):
        x, y = x_index * BRICK_SIZE[0], y_index * BRICK_SIZE[1]
        return Brick(x, y)

    def draw(self, screen):
        for brick in self.bricks:
            if not brick.is_destroyed:
                brick.draw(screen)

    def is_level_complete(self):
        return all(brick.is_destroyed for brick in self.bricks)
