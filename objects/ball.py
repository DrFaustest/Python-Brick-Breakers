import pygame as pg
from settings import Settings
from objects.paddle import Paddle

class Ball(pg.sprite.Sprite):
    def __init__(self, paddle: Paddle) -> None:
        super().__init__()
        self.settings = Settings()
        self.SCREEN_WIDTH = self.settings.get("SCREEN_WIDTH")
        self.BALL_RADIUS = self.settings.get("BALL_RADIUS")
        self.BALL_SPEED = self.settings.get("BALL_SPEED")
        self.WHITE = self.settings.get("WHITE")
        self.BALL_IMG = self.settings.get("BALL_IMG")
        self.original_image = pg.image.load(self.BALL_IMG)
        self.original_image = pg.transform.scale(self.original_image, (self.BALL_RADIUS * 2, self.BALL_RADIUS * 2))
        self.image = self.original_image.copy()
        self.BALL_RADIUS: int = self.BALL_RADIUS
        self.color: tuple = self.WHITE
        self.paddle: Paddle = paddle
        self.position = pg.math.Vector2(paddle.rect.centerx, paddle.rect.top - self.BALL_RADIUS)
        self.rect = self.image.get_rect(center=self.position)
        self.velocity = pg.math.Vector2(0, 0)
        self.attached_to_paddle = True
        self.spin = 5  # Angular velocity, degrees per update cycle
        self.angular_friction = 0.99  # Slows down spin over time
        self.angle = 0  # Current rotation angle

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
        if self.attached_to_paddle:
            self.position.x = self.paddle.rect.centerx
            self.position.y = self.paddle.rect.top - self.BALL_RADIUS
        self.position += self.velocity
        self.rect.center = self.position
        # Update spin
        self.spin *= self.angular_friction
        # Update angle and rotate image only if there's a significant rotation needed
        if abs(self.spin) > 0.1:
            self.angle += self.spin  # Increment angle by spin value
            self.image = pg.transform.rotate(self.original_image, -self.angle)  # Rotate the original image
            self.rect = self.image.get_rect(center=self.rect.center)  # Reset rect to maintain position
        else:
            self.spin = 0  # Optionally reset spin to zero if too small

    def draw(self, screen) -> None:
        """
        Draw the Ball object on the screen.

        Args:
            screen: The screen object.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)

