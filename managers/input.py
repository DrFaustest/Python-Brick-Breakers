import pygame as pg
from settings import Settings
from objects.paddle import Paddle
from objects.ball import Ball
from typing import List

class InputEvent:
    def __init__(self, paddle: Paddle, balls: List[Ball]) -> None:
        """
        Initialize the InputEvent class.

        Args:
            paddle (Paddle): The paddle object.
            balls (List[Ball]): List of ball objects.
        """
        self.paddle = paddle
        self.balls = balls
        self.active_input_type = "mouse"
        self.settings = Settings()
        self.SCREEN_WIDTH: int = self.settings.get("SCREEN_WIDTH")

    def handle_input(self) -> None:
        """
        Handle the input events.

        This method checks for keyboard and mouse inputs and updates the paddle and ball accordingly.
        """
        keys = pg.key.get_pressed()
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_SPACE]:
            self.active_input_type = "keyboard"
        elif mouse_buttons[0]:
            self.active_input_type = "mouse"

        if self.active_input_type == "keyboard":
            if keys[pg.K_LEFT]:
                self.paddle.move("left")
            elif keys[pg.K_RIGHT]:
                self.paddle.move("right")
            if keys[pg.K_SPACE]:
                # Launch all attached balls
                for ball in self.balls:
                    if ball.attached_to_paddle:
                        ball.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE))

        elif self.active_input_type == "mouse":
            self.paddle.rect.centerx = mouse_x
            if self.paddle.rect.left < 0:
                self.paddle.rect.left = 0
            if self.paddle.rect.right > self.SCREEN_WIDTH:
                self.paddle.rect.right = self.SCREEN_WIDTH
            if mouse_buttons[0]:
                # Launch all attached balls
                for ball in self.balls:
                    if ball.attached_to_paddle:
                        ball.handle_event(pg.event.Event(pg.MOUSEBUTTONDOWN, button=1))
