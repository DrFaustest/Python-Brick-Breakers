import math
import pygame as pg
from objects.ball import Ball
from objects.paddle import Paddle
from objects.brick import Brick
from levels.level import Level
from managers.collision import Collision


class DummyScoreboard:
    def __init__(self) -> None:
        self.score = 0


class DummyLives:
    def __init__(self) -> None:
        self.lives = 3


def make_collision_with_custom_level(screen: pg.Surface) -> Collision:
    paddle = Paddle()
    level = Level(0)
    level.bricks = pg.sprite.Group()
    level.brick_rows = {0: []}
    # Place a single brick in row 0
    brick = Brick(100, 0)
    level.bricks.add(brick)
    level.brick_rows[0].append(brick)

    balls = [Ball(paddle)]
    balls[0].attached_to_paddle = False
    balls[0].position = pg.math.Vector2(brick.rect.centerx, brick.rect.bottom + 1)
    balls[0].rect.center = balls[0].position
    balls[0].velocity = pg.math.Vector2(0, -1)

    collision = Collision(balls, paddle, level, DummyScoreboard(), DummyLives(), screen, game_play=None)
    return collision


def test_brick_collision_removes_brick(screen: pg.Surface) -> None:
    collision = make_collision_with_custom_level(screen)
    brick = list(collision.level.brick_rows[0])[0]
    ball = collision.balls[0]

    collision.check_brick_collision(ball)

    assert brick.is_destroyed is True
    assert brick not in collision.level.bricks
    assert brick not in collision.level.brick_rows[0]
    assert collision.scoreboard.score == 10


def test_ball_ball_collision_preserves_speed(screen: pg.Surface) -> None:
    paddle = Paddle()
    level = Level(0)
    balls = [Ball(paddle), Ball(paddle)]
    for ball in balls:
        ball.attached_to_paddle = False
    balls[0].position = pg.math.Vector2(100, 100)
    balls[1].position = pg.math.Vector2(100 + balls[0].BALL_RADIUS * 1.8, 100)
    for ball in balls:
        ball.rect.center = ball.position
    balls[0].velocity = pg.math.Vector2(2, 0)
    balls[1].velocity = pg.math.Vector2(-2, 0)

    collision = Collision(balls, paddle, level, DummyScoreboard(), DummyLives(), screen, game_play=None)
    speed1 = balls[0].velocity.length()
    speed2 = balls[1].velocity.length()

    collision.check_ball_ball_collision()

    assert math.isclose(balls[0].velocity.length(), speed1, rel_tol=0.05)
    assert math.isclose(balls[1].velocity.length(), speed2, rel_tol=0.05)


def test_check_ball_stuck_pushes_off_top(screen: pg.Surface) -> None:
    paddle = Paddle()
    level = Level(0)
    ball = Ball(paddle)
    ball.attached_to_paddle = False
    ball.rect.top = 0
    ball.position = pg.math.Vector2(ball.rect.centerx, ball.rect.centery)
    ball.velocity = pg.math.Vector2(1, 0.0)

    collision = Collision([ball], paddle, level, DummyScoreboard(), DummyLives(), screen, game_play=None)
    collision.check_ball_stuck(ball)

    assert ball.rect.top >= 0
    assert ball.velocity.y >= collision.MIN_Y_VELOCITY
