import pygame as pg
from settings import *

class InputEvent:
    def __init__(self, paddle, ball):
        """
        Initialize the InputEvent class.

        Args:
            paddle (Paddle): The paddle object.
            ball (Ball): The ball object.
        """
        self.paddle = paddle
        self.ball = ball
        self.active_input_type = "keyboard"  # Default to keyboard at the start

    def handle_input(self):
        """
        Handle the input events.

        This method checks for keyboard and mouse inputs and updates the paddle and ball accordingly.
        """
        keys = pg.key.get_pressed()
        mouse_x, mouse_y = pg.mouse.get_pos()  # Get the current mouse position
        mouse_buttons = pg.mouse.get_pressed()  # Check if any mouse buttons are pressed

        # Determine active input type based on input received
        if keys[KEY_MOVE_LEFT] or keys[KEY_MOVE_RIGHT] or keys[pg.K_SPACE]:
            self.active_input_type = "keyboard"
        elif mouse_buttons[0]:  # Left mouse button click activates mouse mode
            self.active_input_type = "mouse"

        # Handle keyboard inputs
        if self.active_input_type == "keyboard":
            if keys[KEY_MOVE_LEFT]:
                self.paddle.move("left")
            elif keys[KEY_MOVE_RIGHT]:
                self.paddle.move("right")
            if keys[pg.K_SPACE] and self.ball.attached_to_paddle:
                # Release the ball
                self.ball.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE))

        # Handle mouse inputs
        elif self.active_input_type == "mouse":
            # Move paddle based on mouse position
            self.paddle.rect.centerx = mouse_x
            # Restrict paddle movement to screen bounds
            if self.paddle.rect.left < 0:
                self.paddle.rect.left = 0
            if self.paddle.rect.right > SCREEN_WIDTH:
                self.paddle.rect.right = SCREEN_WIDTH
            # Mouse input to release the ball
            if mouse_buttons[0]:  # Left mouse button
                self.ball.handle_event(pg.event.Event(pg.MOUSEBUTTONDOWN, button=1))

