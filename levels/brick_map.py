import settings
import random

def generate_brick_map():
    # Determmin max bricks and percentage of bricks to be generated
    max_bricks_x = settings.SCREEN_WIDTH // settings.BRICK_SIZE[0]
    max_bricks_y = (settings.SCREEN_HEIGHT // 2) // settings.BRICK_SIZE[1]
    total_bricks = int((max_bricks_x * max_bricks_y) * (settings.DIFFICULTY / 10))
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
