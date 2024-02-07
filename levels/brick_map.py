import settings
import random

def generate_brick_map():
    # Calculate max bricks per row and column
    max_bricks_x = settings.SCREEN_WIDTH // settings.BRICK_WIDTH
    max_bricks_y = (settings.SCREEN_HEIGHT // 2) // settings.BRICK_HEIGHT  # Ensure bricks don't pass halfway

    # Calculate total bricks based on difficulty (1 to 10)
    total_bricks = int((max_bricks_x * max_bricks_y) * (settings.DIFFICULTY / 10))

    # Initialize empty grid
    grid = [[0 for _ in range(max_bricks_x)] for _ in range(max_bricks_y)]

    # Generate unique brick positions
    brick_positions = set()
    while len(brick_positions) < total_bricks:
        x = random.randint(0, max_bricks_x - 1)
        y = random.randint(0, max_bricks_y - 1)
        brick_positions.add((x, y))


    # Fill the grid with bricks based on generated positions
    for x, y in brick_positions:
        grid[y][x] = 1  # Mark the position with a brick

    return grid

if __name__ == "__main__":
    # Example usage
    brick_map = generate_brick_map(50, 20, 5)
    print(brick_map)