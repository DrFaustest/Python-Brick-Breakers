import pygame as pg
from settings import Settings
from objects.paddle import Paddle

class Ball(pg.sprite.Sprite):
    def __init__(self, paddle: Paddle) -> None:
        """
        Initialize the Ball object.

        Args:
            paddle (Paddle): The paddle object.

        Returns:
            None
        """
        super().__init__()
        self.settings = Settings()
        self.SCREEN_WIDTH = self.settings.get("SCREEN_WIDTH")
        self.BALL_RADIUS = self.settings.get("BALL_RADIUS")
        self.BALL_SPEED = self.settings.get("BALL_SPEED")
        self.WHITE = self.settings.get("WHITE")
        self.BALL_IMG = self.settings.get("BALL_IMG")
        self.image = pg.image.load(self.BALL_IMG)
        self.image = pg.transform.scale(self.image, (self.BALL_RADIUS * 2, self.BALL_RADIUS * 2))
        self.BALL_RADIUS: int = self.BALL_RADIUS
        self.color: tuple = self.WHITE
        self.paddle: Paddle = paddle
        self.position = pg.math.Vector2(paddle.rect.centerx, paddle.rect.top - self.BALL_RADIUS)
        self.rect = self.image.get_rect(center=self.position)
        self.velocity = pg.math.Vector2(0, 0)
        self.attached_to_paddle: bool = True

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Handle the events for the Ball object.

        Args:
            event (pg.event.Event): The event object.

        Returns:
            None
        """
        if (event.type == pg.KEYDOWN and event.key == pg.K_SPACE or
        event.type == pg.MOUSEBUTTONDOWN) and self.attached_to_paddle:
            paddle_center_relative = (self.paddle.rect.centerx - self.SCREEN_WIDTH / 2) / (self.SCREEN_WIDTH / 2)
            initial_angle = (paddle_center_relative * 45) + 90
            self.velocity = pg.math.Vector2(self.BALL_SPEED, 0).rotate(-initial_angle)
            self.attached_to_paddle = False

    def update(self) -> None:
        """
        Update the Ball object.

        Args:
            None

        Returns:
            None
        """
        if self.attached_to_paddle:
            self.position.x = self.paddle.rect.centerx
            self.position.y = self.paddle.rect.top - self.BALL_RADIUS
        self.position += self.velocity
        self.rect.center = self.position

    def draw(self, screen) -> None:
        """
        Draw the Ball object on the screen.

        Args:
            screen: The screen object.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)
