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
        # Use pg.math.Vector2 for position
        self.position = pg.math.Vector2(paddle.rect.centerx, paddle.rect.top - self.BALL_RADIUS)

        self.rect = pg.Rect(self.position.x - BALL_RADIUS, self.position.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        # Use pg.math.Vector2 for velocity
        self.velocity = pg.math.Vector2(0, 0)
        self.attached_to_paddle: bool = True

    def handle_event(self, event: pg.event.Event) -> None:
        if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE or
        event.type == pg.MOUSEBUTTONDOWN) and self.attached_to_paddle:
            # Use pg.math.Vector2 for angle calculation
            angle = pg.math.Vector2(self.paddle.rect.centerx - self.position.x, self.paddle.rect.centery - self.position.y).angle_to(pg.math.Vector2(1, 0))
            angle = max(45, min(135, angle))
            self.velocity = pg.math.Vector2(BALL_SPEED, 0).rotate(-angle)  # Note: Pygame rotates counterclockwise, hence the negative angle for correct direction
            self.attached_to_paddle = False

    def update(self) -> None:
        if self.attached_to_paddle:
            # Update position based on the paddle's position if attached
            self.position.x = self.paddle.rect.centerx
            self.position.y = self.paddle.rect.top - self.BALL_RADIUS
        else:
            # Update position based on velocity if not attached
            # Removed unnecessary velocity.magnitude() call
            pass  # This pass statement is just to highlight the removal, it does nothing and can be omitted

        # Update rect for collision detection, now using vector addition for position update
        self.position += self.velocity
        self.rect.x = int(self.position.x - self.BALL_RADIUS)
        self.rect.y = int(self.position.y - self.BALL_RADIUS)

    def draw(self, screen):
        # Draw the ball using its vector position
        screen.blit(self.image, self.rect)
