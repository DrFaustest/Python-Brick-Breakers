import unittest
from unittest.mock import MagicMock, patch
import pygame as pg
from pygame.locals import *
from settings import *
from objects.paddle import Paddle
from objects.ball import Ball

# Mock settings before importing Ball
WHITE = (255, 255, 255)
BALL_SPEED = 5

with patch.dict('sys.modules', {'settings': MagicMock(WHITE=WHITE, BALL_SPEED=BALL_SPEED),
                                'objects.paddle': MagicMock(),
                                'managers.vector': MagicMock()}):
    from objects.ball import Ball  # Replace 'your_module.ball' with the actual module path

class TestBall(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.paddle_mock = MagicMock()
        self.paddle_mock.rect = pg.Rect(100, 550, 100, 20)
        self.ball = Ball(self.paddle_mock)

    def test_init(self):
        self.assertEqual(self.ball.radius, 10)
        self.assertEqual(self.ball.color, WHITE)
        self.assertTrue(self.ball.attached_to_paddle)
        self.assertEqual(self.ball.velocity.x, 0)
        self.assertEqual(self.ball.velocity.y, 0)

    def test_handle_event_space_keydown(self):
        event = pg.event.Event(KEYDOWN, {'key': K_SPACE})
        self.ball.handle_event(event)
        self.assertFalse(self.ball.attached_to_paddle)
        self.assertNotEqual(self.ball.velocity.x, 0)
        self.assertNotEqual(self.ball.velocity.y, 0)

    def test_handle_event_mouse_button_down(self):
        event = pg.event.Event(MOUSEBUTTONDOWN)
        self.ball.handle_event(event)
        self.assertFalse(self.ball.attached_to_paddle)
        self.assertNotEqual(self.ball.velocity.x, 0)
        self.assertNotEqual(self.ball.velocity.y, 0)

    def test_update_attached(self):
        self.ball.attached_to_paddle = True
        self.ball.update()
        self.assertEqual(self.ball.position.x, self.paddle_mock.rect.centerx)
        self.assertEqual(self.ball.position.y, self.paddle_mock.rect.top - self.ball.radius)

    def test_update_not_attached(self):
        self.ball.attached_to_paddle = False
        self.ball.velocity.x = BALL_SPEED
        self.ball.velocity.y = -BALL_SPEED
        initial_x, initial_y = self.ball.position.x, self.ball.position.y
        self.ball.update()
        self.assertNotEqual(self.ball.position.x, initial_x)
        self.assertNotEqual(self.ball.position.y, initial_y)

    @patch('pygame.draw.circle')
    def test_draw(self, mock_draw):
        self.ball.draw(self.screen)
        mock_draw.assert_called_once_with(self.screen, self.ball.color, (int(self.ball.position.x), int(self.ball.position.y)), self.ball.radius)

if __name__ == '__main__':
    unittest.main()
