import unittest
from unittest.mock import patch, Mock
import pygame as pg
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from objects.paddle import Paddle

# Mock settings before importing Paddle
WHITE = (255, 255, 255)
PADDLE_SPEED = 0.5
SCREEN_WIDTH = 800

@patch('settings.WHITE', WHITE)
@patch('settings.PADDLE_SPEED', PADDLE_SPEED)
@patch('settings.SCREEN_WIDTH', SCREEN_WIDTH)
class TestPaddle(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame to avoid "pygame not initialized" errors during tests
        pg.init()
        self.paddle = Paddle()

    def test_init(self):
        self.assertEqual(self.paddle.rect.x, 350)
        self.assertEqual(self.paddle.rect.y, 550)
        self.assertEqual(self.paddle.rect.width, 100)
        self.assertEqual(self.paddle.rect.height, 20)
        self.assertEqual(self.paddle.speed, PADDLE_SPEED)
        self.assertEqual(self.paddle.screen_width, SCREEN_WIDTH)
        self.assertEqual(self.paddle.position_accumulator, 350)

    def test_move_left_within_bounds(self):
        self.paddle.move("left")
        self.assertTrue(self.paddle.rect.x < 350)
        self.assertTrue(self.paddle.position_accumulator < 350)

    def test_move_right_within_bounds(self):
    # Call move right multiple times to ensure a noticeable change
        for _ in range(10):  # Move right multiple times to ensure accumulation
            self.paddle.move("right")
        self.assertTrue(self.paddle.rect.x > 350, "Paddle did not move right from its original position.")
        self.assertTrue(self.paddle.position_accumulator > 350, "Position accumulator did not increase as expected.")

    def test_move_left_boundary_check(self):
        self.paddle.position_accumulator = -5
        self.paddle.move("left")
        self.assertEqual(self.paddle.rect.x, 0)
        self.assertEqual(self.paddle.position_accumulator, 0)

    def test_move_right_boundary_check(self):
        self.paddle.position_accumulator = SCREEN_WIDTH + 5  # beyond the right boundary
        self.paddle.move("right")
        self.assertEqual(self.paddle.rect.right, SCREEN_WIDTH)
        self.assertEqual(self.paddle.position_accumulator, SCREEN_WIDTH - self.paddle.rect.width)

    @patch('pygame.draw.rect')
    def test_draw(self, mock_draw):
        screen_mock = Mock()
        self.paddle.draw(screen_mock)
        mock_draw.assert_called_once_with(screen_mock, self.paddle.rect)

if __name__ == '__main__':
    unittest.main()