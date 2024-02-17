import pygame as pg
from settings import *
from objects.paddle import Paddle

class Ball:
    def __init__(self, paddle: Paddle) -> None:
        self.image = pg.image.load(BALL_IMG)
        self.image = pg.transform.scale(self.image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.BALL_RADIUS: int = BALL_RADIUS
        self.color: tuple = WHITE
        self.paddle: Paddle = paddle
        self.position = pg.math.Vector2(paddle.rect.centerx, paddle.rect.top - self.BALL_RADIUS)
        self.rect = pg.Rect(self.position.x - BALL_RADIUS, self.position.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.velocity = pg.math.Vector2(0, 0)
        self.attached_to_paddle: bool = True

    def handle_event(self, event: pg.event.Event) -> None:
        if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE or
        event.type == pg.MOUSEBUTTONDOWN) and self.attached_to_paddle:
            paddle_center_relative = (self.paddle.rect.centerx - SCREEN_WIDTH / 2) / (SCREEN_WIDTH / 2)
            initial_angle = (paddle_center_relative * 45) + 90
            self.velocity = pg.math.Vector2(BALL_SPEED, 0).rotate(-initial_angle)
            self.attached_to_paddle = False

    def update(self) -> None:
        if self.attached_to_paddle:
            self.position.x = self.paddle.rect.centerx
            self.position.y = self.paddle.rect.top - self.BALL_RADIUS
        self.position += self.velocity
        self.rect.x = int(self.position.x - self.BALL_RADIUS)
        self.rect.y = int(self.position.y - self.BALL_RADIUS)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
