import math
import pygame as pg
from objects.ball import Ball
from objects.paddle import Paddle


def test_ball_launch_sets_velocity() -> None:
    paddle = Paddle()
    ball = Ball(paddle)
    launch_event = pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE)

    ball.handle_event(launch_event)

    assert ball.attached_to_paddle is False
    assert math.isclose(ball.velocity.length(), ball.BALL_SPEED, rel_tol=0.05)
    assert ball.velocity.y < 0  # launches upward from center


def test_paddle_stays_within_bounds() -> None:
    paddle = Paddle()
    # Move far left
    for _ in range(50):
        paddle.move("left")
    assert paddle.rect.left >= 0

    # Move far right
    for _ in range(200):
        paddle.move("right")
    assert paddle.rect.right <= paddle.screen_width
