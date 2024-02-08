import pygame as pg
from settings import *
from objects.paddle import Paddle
from managers.vector import Vector2D


class Ball:
    def __init__(self, paddle: Paddle, radius: int =10, color: tuple =(WHITE)) -> None:
        self.image = pg.image.load(BALL_IMG)
        self.image = pg.transform.scale(self.image, (radius * 2, radius * 2))
        self.radius: int = radius
        self.color: tuple = color
        self.paddle: Paddle = paddle
        self.position = Vector2D(paddle.rect.centerx, paddle.rect.top - self.radius)

        self.rect = pg.Rect(self.position.x - radius, self.position.y - radius, radius * 2, radius * 2)
        self.velocity = Vector2D(0, 0)
        self.attached_to_paddle: bool = True

    def handle_event(self, event: pg.event.Event) -> None:
        if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE or
        event.type == pg.MOUSEBUTTONDOWN) and self.attached_to_paddle:
        # Set initial velocity when the ball is released
            self.velocity = Vector2D(BALL_SPEED, -BALL_SPEED)
            self.attached_to_paddle = False
        

    def update(self) -> None:
        if self.attached_to_paddle:
            # Update position based on the paddle's position if attached
            self.position.x = self.paddle.rect.centerx
            self.position.y = self.paddle.rect.top - self.radius
        else:
            # Update position based on velocity if not attached
            self.velocity.set_magnitude(BALL_SPEED)

        # Update rect for collision detection
        self.position += self.velocity
        self.rect.x = int(self.position.x - self.radius)
        self.rect.y = int(self.position.y - self.radius)

    def draw(self, screen):
        # Draw the ball using its vector position
        screen.blit(self.image, self.rect)