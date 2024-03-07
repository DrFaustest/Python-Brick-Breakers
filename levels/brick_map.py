from settings import Settings
import random

def generate_brick_map():
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
