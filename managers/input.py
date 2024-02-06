import pygame as pg
from settings import *

class InputEvent:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[KEY_MOVE_LEFT]:
            self.paddle.move("left")
        elif keys[KEY_MOVE_RIGHT]:
            self.paddle.move("right")
        if keys[pg.K_SPACE]:
            self.ball.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE))
