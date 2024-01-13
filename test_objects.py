import unittest
from unittest.mock import Mock, MagicMock
from objects import *
from settings import *
import pygame as pg

class TestButton(unittest.TestCase):

    def setUp(self):
        # Mocking Pygame functionalities
        self.mock_screen = Mock()
        self.mock_event = Mock()
        self.mock_font = Mock()
        pg.font.SysFont = Mock(return_value=self.mock_font)
        pg.Rect = Mock(return_value=Mock())
        pg.draw.rect = Mock()
        pg.mouse = Mock()

        # Initialize a Button object
        self.button = Button(50, 50)

    def test_initialization(self):
        # Test the initialization of the Button
        self.assertEqual(self.button.rect, pg.Rect.return_value)
        self.assertEqual(self.button.color, (255, 255, 255))
        # Add more assertions as necessary

    def test_draw(self):
        # Test the drawing functionality
        self.button.draw(self.mock_screen)
        pg.draw.rect.assert_called_with(self.mock_screen, self.button.color, self.button.rect)
        # Add more assertions as necessary

    def test_check_hover(self):
        # Test the hover functionality
        self.button.check_hover((60, 60))
        self.assertEqual(self.button.color, self.button.hover_color)
        # Add more assertions as necessary

    def test_handle_event(self):
        # Test the event handling functionality
        self.mock_event.type = pg.MOUSEBUTTONDOWN
        self.mock_event.button = 1
        self.mock_event.pos = (60, 60)
        self.button.handle_event(self.mock_event)
        # Assertions depend on the action callback
        # Add more assertions as necessary

class TestPaddle(unittest.TestCase):
    def setUp(self):
        self.mock_screen = Mock()
        pg.draw.rect = Mock()

        # Initialize a Paddle object
        self.paddle = Paddle(100, 50, 100, 20, 800)  # Example dimensions and screen width

        # Assign a real pygame.Rect to paddle.rect
        self.paddle.rect = pg.Rect(100, 50, 100, 20)

    def test_move_left(self):
        # Move the paddle left and test its new position
        original_x = self.paddle.rect.x
        self.paddle.move("left")
        self.assertTrue(self.paddle.rect.x < original_x or self.paddle.rect.x == 0)

    def test_move_right(self):
        # Move the paddle right and test its new position
        original_x = self.paddle.rect.x
        self.paddle.move("right")
        self.assertTrue(self.paddle.rect.x > original_x or self.paddle.rect.right == self.paddle.screen_width)

    def test_initialization(self):
        # Test initialization
        self.assertEqual(self.paddle.rect, pg.Rect.return_value)
        self.assertEqual(self.paddle.color, (255, 255, 255))
        self.assertEqual(self.paddle.speed, PADDLE_SPEED)
        self.assertEqual(self.paddle.screen_width, 800)

    def test_draw(self):
        # Test the drawing functionality
        self.paddle.draw(self.mock_screen)
        pg.draw.rect.assert_called_with(self.mock_screen, self.paddle.color, self.paddle.rect)

class TestBall(unittest.TestCase):
    def setUp(self):
        self.mock_screen = Mock()
        self.mock_paddle = Mock()

        # Mock the paddle's rect with specific return values for properties
        self.mock_paddle.rect = Mock()
        self.mock_paddle.rect.top = 100
        self.mock_paddle.rect.centerx = 150

        pg.draw.circle = Mock()

        # Initialize a Ball object
        self.ball = Ball(self.mock_paddle)


    def test_initialization(self):
        # Test initialization
        self.assertEqual(self.ball.radius, 10)
        self.assertEqual(self.ball.color, (255, 255, 255))
        self.assertEqual(self.ball.paddle, self.mock_paddle)
        self.assertTrue(self.ball.attached_to_paddle)

    def test_handle_event(self):
        # Test handling an event
        mock_event = MagicMock()
        mock_event.type = pg.KEYDOWN
        mock_event.key = pg.K_SPACE
        self.ball.handle_event(mock_event)
        self.assertFalse(self.ball.attached_to_paddle)
        self.assertNotEqual(self.ball.speed_x, 0)
        self.assertNotEqual(self.ball.speed_y, 0)

    def test_update_attached(self):
        # Test update method when ball is attached to the paddle
        self.ball.attached_to_paddle = True
        self.ball.update()
        self.assertEqual(self.ball.x, self.mock_paddle.rect.centerx)
        self.assertEqual(self.ball.y, self.mock_paddle.rect.top - self.ball.radius)

    def test_update_detached(self):
        # Test update method when ball is not attached to the paddle
        self.ball.attached_to_paddle = False
        original_x, original_y = self.ball.x, self.ball.y
        self.ball.update()
        self.assertNotEqual(self.ball.x, original_x)
        self.assertNotEqual(self.ball.y, original_y)

    def test_draw(self):
        # Test the drawing functionality
        self.ball.draw(self.mock_screen)
        pg.draw.circle.assert_called_with(self.mock_screen, self.ball.color, (self.ball.x, self.ball.y), self.ball.radius)

class TestBrick(unittest.TestCase):
    def setUp(self):
        self.mock_screen = Mock()
        pg.Rect = Mock(return_value=Mock())
        pg.draw.rect = Mock()
        self.brick = Brick(100, 100, 50, 20)  # Example brick

    def test_initialization(self):
        self.assertEqual(self.brick.rect, pg.Rect.return_value)
        self.assertEqual(self.brick.color, (255, 0, 0))
        self.assertFalse(self.brick.is_destroyed)

    def test_draw(self):
        self.brick.draw(self.mock_screen)
        pg.draw.rect.assert_called_with(self.mock_screen, self.brick.color, self.brick.rect)

    def test_destroy(self):
        self.brick.destroy()
        self.assertTrue(self.brick.is_destroyed)


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level_data = [[1, 1, 0, 0, 0], [0, 1, 1, 0, 0]]  # Example level data
        self.level = Level(self.level_data)

    def test_load_level(self):
        self.assertEqual(len(self.level.bricks), 4)  # 4 bricks based on the level data

    def test_draw(self):
        self.mock_screen = Mock()
        self.level.draw(self.mock_screen)
        # Assert that draw is called the correct number of times
        self.assertEqual(pg.draw.rect.call_count, 4)

    def test_is_level_complete(self):
        for brick in self.level.bricks:
            brick.destroy()
        self.assertTrue(self.level.is_level_complete())

class TestScoreboard(unittest.TestCase):
    def setUp(self):
        self.mock_screen = Mock()
        pg.font.SysFont = Mock(return_value=Mock(render=Mock(return_value=Mock())))
        self.scoreboard = Scoreboard(100, 50)  # Example position

    def test_initialization(self):
        self.assertEqual(self.scoreboard.score, 0)
        self.assertEqual(self.scoreboard.x, 100)
        self.assertEqual(self.scoreboard.y, 50)

    def test_increase_score(self):
        original_score = self.scoreboard.score
        self.scoreboard.increase_score(10)
        self.assertEqual(self.scoreboard.score, original_score + 10)

    def test_draw(self):
        self.scoreboard.draw(self.mock_screen)
        # Test if the draw method calls the render and blit methods
        self.assertTrue(pg.font.SysFont.return_value.render.called)
        self.assertTrue(self.mock_screen.blit.called)

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.mock_ball = Mock()
        self.mock_ball.speed_x = 0
        self.mock_ball.speed_y = 0
        self.mock_paddle = Mock()
        self.mock_bricks = [Mock(is_destroyed=False, rect=Mock()) for _ in range(5)]
        self.screen_width = 800
        self.screen_height = 600
        self.collision = Collision(self.mock_ball, self.mock_paddle, self.mock_bricks, self.screen_width, self.screen_height)

    def test_check_wall_collision(self):
        # Test collision with left wall
        self.mock_ball.rect.left = -10
        self.collision.check_wall_collision()
        self.assertNotEqual(self.mock_ball.speed_x, 0)

        # Test collision with right wall
        self.mock_ball.rect.right = self.screen_width + 10
        self.collision.check_wall_collision()
        self.assertNotEqual(self.mock_ball.speed_x, 0)

        # Test collision with top wall
        self.mock_ball.rect.top = -10
        self.collision.check_wall_collision()
        self.assertNotEqual(self.mock_ball.speed_y, 0)

    def test_check_paddle_collision(self):
        # Test collision with paddle
        self.mock_ball.rect.colliderect.return_value = True
        self.collision.check_paddle_collision()
        self.assertNotEqual(self.mock_ball.speed_y, 0)

    def test_check_brick_collision(self):
        # Test collision with a brick
        self.mock_bricks[0].rect.colliderect.return_value = True
        self.collision.check_brick_collision()
        self.assertTrue(self.mock_bricks[0].is_destroyed)

        # No collision with other bricks
        for brick in self.mock_bricks[1:]:
            self.assertFalse(brick.is_destroyed)

if __name__ == '__main__':
    unittest.main()
