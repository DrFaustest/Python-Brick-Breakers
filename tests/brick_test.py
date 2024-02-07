import unittest
from unittest.mock import patch, Mock
import pygame as pg
import sys
import os

# Append the directory above the 'tests' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from objects.brick import Brick

# Initialize Pygame to avoid "pygame not initialized" errors during tests
pg.init()

# Use class-level patches for Pygame functionalities
@patch('pygame.image.load', Mock(return_value=Mock()))
@patch('pygame.transform.scale', Mock(return_value=Mock()))
class TestBrick(unittest.TestCase):
    # Mock BRICK_WIDTH and BRICK_HEIGHT directly in the setup
    @patch.dict('settings.__dict__', {'BRICK_WIDTH': 50, 'BRICK_HEIGHT': 20})
    def setUp(self):
        self.brick = Brick(100, 150)

    def test_init(self):
        self.assertEqual(self.brick.rect.x, 100)
        self.assertEqual(self.brick.rect.y, 150)
        self.assertFalse(self.brick.is_destroyed)

    # Use method-level patch for `pygame.Surface.blit`

    def test_draw(self):
        screen_mock = Mock()
        self.brick.draw(screen_mock)
        screen_mock.blit.assert_called_once_with(self.brick.image, self.brick.rect)

    def test_destroy(self):
        self.brick.destroy()
        self.assertTrue(self.brick.is_destroyed)

if __name__ == '__main__':
    unittest.main()
