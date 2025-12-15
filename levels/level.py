from settings import Settings
from objects.brick import Brick
from objects.moving_brick import MovingBrick
import pygame
import random
from typing import List, Tuple, Dict

class Level:
    def __init__(self, current_level: int) -> None:
        """
        Initializes a Level object.

        Parameters:
        - current_level (int): The current level number.
        """
        self.settings = Settings()
        self.BRICK_SIZE: Tuple[int, int] = self.settings.get("BRICK_SIZE")
        self.SCREEN_WIDTH: int = self.settings.get("SCREEN_WIDTH")
        self.SCREEN_HEIGHT: int = self.settings.get("SCREEN_HEIGHT")
        self.current_level: int = current_level
        self.level_name: int = current_level + 1
        self.max_bricks_x: int = self.SCREEN_WIDTH // self.BRICK_SIZE[0]
        self.max_bricks_y: int = (self.SCREEN_HEIGHT // 2) // self.BRICK_SIZE[1]
        self.level_map: List[List[int]] = self.generate_brick_map()
        self.bricks: pygame.sprite.Group = pygame.sprite.Group()
        self.brick_rows: Dict[int, List[Brick]] = {}  # Row-based brick organization
        self.level_complete: bool = False
        self.load_level(self.level_map)

    def load_level(self, level_data: List[List[int]]) -> None:
        """
        Loads the level by creating bricks based on the level data.
        Also generates moving bricks (10% chance per row).

        Parameters:
        - level_data (list): The map of bricks for the level, where:
            - 0 = empty space
            - 1 = static brick
            - 2 = moving brick
        """
        for row_index, row in enumerate(level_data):
            # Initialize row array
            self.brick_rows[row_index] = []
            
            for col_index, col in enumerate(row):
                if col == 1:
                    brick = self.create_brick(col_index, row_index)
                    self.bricks.add(brick)
                    self.brick_rows[row_index].append(brick)
                elif col == 2:
                    brick = self.create_moving_brick(col_index, row_index)
                    self.bricks.add(brick)
                    self.brick_rows[row_index].append(brick)
    
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

    def create_moving_brick(self, x_index: int, y_index: int) -> MovingBrick:
        """
        Creates a MovingBrick object at the specified position.

        Parameters:
        - x_index (int): The x-index of the brick in the level map.
        - y_index (int): The y-index of the brick in the level map.

        Returns:
        - MovingBrick: The created MovingBrick object.
        """
        x, y = x_index * self.BRICK_SIZE[0], y_index * self.BRICK_SIZE[1]
        return MovingBrick(x, y, y_index, self)

    def update(self) -> None:
        """
        Updates all bricks in the level (for moving bricks).
        """
        for brick in self.bricks:
            if not brick.is_destroyed:
                brick.update()

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
        Includes moving bricks (type 2) with a 10-15% chance per row.

        Returns:
        - grid (list): A 2D list representing the brick map, where:
            - 0 = empty space
            - 1 = static brick
            - 2 = moving brick
        """
        DIFFICULTY: int = self.settings.get("DIFFICULTY")
        # Determine max bricks and percentage of bricks to be generated
        total_bricks: int = int((self.max_bricks_x * self.max_bricks_y) * (DIFFICULTY / 10))
        
        # Generate the brick map with random brick positions
        grid: List[List[int]] = [[0 for _ in range(self.max_bricks_x)] for _ in range(self.max_bricks_y)]
        brick_positions: set = set()
        
        while len(brick_positions) < total_bricks:
            x: int = random.randint(0, self.max_bricks_x - 1)
            y: int = random.randint(0, self.max_bricks_y - 1)
            brick_positions.add((x, y))
        
        # Place bricks and determine which should be moving
        moving_brick_chance: float = 0.15  # 15% chance of moving brick per row
        rows_with_moving_bricks: set = set()
        
        for x, y in brick_positions:
            # Decide if this row should have a moving brick
            if y not in rows_with_moving_bricks and random.random() < moving_brick_chance:
                grid[y][x] = 2  # Moving brick
                rows_with_moving_bricks.add(y)
            else:
                grid[y][x] = 1  # Static brick
        
        return grid
    
    def get_ball_collision_rows(self, ball_rect: pygame.Rect, ball_velocity: pygame.math.Vector2) -> List[int]:
        """
        Determines which brick rows the ball is currently in or will enter based on velocity.
        This optimizes collision detection by only checking relevant rows.

        Parameters:
        - ball_rect (pygame.Rect): The ball's current rectangle.
        - ball_velocity (pygame.math.Vector2): The ball's velocity vector.

        Returns:
        - List[int]: List of row indices to check for collision.
        """
        rows_to_check: set = set()
        
        # Current row(s) the ball occupies
        current_top_row: int = max(0, ball_rect.top // self.BRICK_SIZE[1])
        current_bottom_row: int = min(self.max_bricks_y - 1, ball_rect.bottom // self.BRICK_SIZE[1])
        
        for row in range(current_top_row, current_bottom_row + 1):
            rows_to_check.add(row)
        
        # Predicted row(s) based on velocity (look ahead 1 frame)
        if ball_velocity.y != 0:
            predicted_y: int = ball_rect.centery + int(ball_velocity.y)
            predicted_row: int = predicted_y // self.BRICK_SIZE[1]
            if 0 <= predicted_row < self.max_bricks_y:
                rows_to_check.add(predicted_row)
        
        return sorted(list(rows_to_check))
