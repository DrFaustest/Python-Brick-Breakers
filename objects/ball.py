import pygame as pg
from settings import *
from objects.paddle import Paddle


class Ball:
    def __init__(self, paddle: Paddle, radius: int =10, color: tuple =(WHITE)) -> None:
        self.radius: int = radius
        self.color: tuple = color
        self.paddle: Paddle = paddle
        self.x: int = paddle.rect.centerx
        self.y: int = paddle.rect.top - radius
        self.rect: pg.Rect = pg.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        self.speed_x: int = 0
        self.speed_y: int = 0
        self.attached_to_paddle: bool = True

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.attached_to_paddle:
            self.speed_x = BALL_SPEED
            self.speed_y = -BALL_SPEED
            self.attached_to_paddle = False
        if event.type == pg.MOUSEBUTTONDOWN and self.attached_to_paddle:
            self.speed_x = BALL_SPEED
            self.speed_y = -BALL_SPEED
            self.attached_to_paddle = False
        

    def update(self) -> None:
        if self.attached_to_paddle:
            self.x = self.paddle.rect.centerx
            self.y = self.paddle.rect.top - self.radius
        else:
            self.x += self.speed_x
            self.y += self.speed_y

        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)