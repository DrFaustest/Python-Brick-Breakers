import pygame as pg
from levels.level import Level


def test_level_brick_rows_match_group() -> None:
    level = Level(0)
    total_row_bricks = sum(len(row) for row in level.brick_rows.values())
    assert total_row_bricks == len(level.bricks)
    # Every brick in rows is part of the sprite group
    assert all(brick in level.bricks for row in level.brick_rows.values() for brick in row)


def test_get_ball_collision_rows_includes_current_row() -> None:
    level = Level(0)
    row_height = level.BRICK_SIZE[1]
    ball_rect = pg.Rect(0, row_height * 2, level.BRICK_SIZE[0], level.BRICK_SIZE[1])
    rows = level.get_ball_collision_rows(ball_rect, pg.math.Vector2(0, 0))
    assert 2 in rows
