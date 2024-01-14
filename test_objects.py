import unittest
from unittest.mock import Mock, MagicMock, patch
from objects import *
from settings import *
import pygame as pg

class TestButton(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.button = Button(100, 100, 200, 100, "Test", (255, 255, 255), (0, 255, 0), (0, 0, 0))

    def test_initialization(self):
        self.assertEqual(self.button.rect.x, 100)
        self.assertEqual(self.button.rect.y, 100)
        self.assertEqual(self.button.rect.width, 200)
        self.assertEqual(self.button.rect.height, 100)
        self.assertEqual(self.button.text, "Test")
        self.assertEqual(self.button.color, (255, 255, 255))
        self.assertEqual(self.button.hover_color, (0, 255, 0))
        self.assertEqual(self.button.text_color, (0, 0, 0))

    def test_draw(self):
        # Since draw method involves pygame graphics, we primarily ensure it runs without error
        self.button.draw(self.screen)
        # More detailed graphical testing is beyond the scope of unit testing

    def test_check_hover(self):
        self.button.check_hover((150, 150))
        self.assertEqual(self.button.color, self.button.hover_color)
        self.button.check_hover((50, 50))
        self.assertEqual(self.button.color, (255, 255, 255))

    def test_handle_event(self):
        # Mocking pygame event and action
        mock_action = Mock()
        self.button.action = mock_action
        mock_event = pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(150, 150))
        self.button.handle_event(mock_event)
        mock_action.assert_called_once()
  

class TestPaddle(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.paddle = Paddle(100, 550, 100, 20, self.screen_width)

    def tearDown(self):
        pg.quit()

    def test_initialization(self):
        self.assertEqual(self.paddle.rect.x, 100)
        self.assertEqual(self.paddle.rect.y, 550)
        self.assertEqual(self.paddle.rect.width, 100)
        self.assertEqual(self.paddle.rect.height, 20)
        self.assertEqual(self.paddle.screen_width, self.screen_width)
        self.assertEqual(self.paddle.position_accumulator, 100)

    def test_move_left_within_bounds(self):
        initial_x = self.paddle.rect.x
        self.paddle.move("left")
        self.assertTrue(self.paddle.rect.x < initial_x)
        self.assertTrue(self.paddle.rect.x >= 0)

    def test_move_right_within_bounds(self):
        initial_x = self.paddle.rect.x
        self.paddle.move("right")
        self.assertTrue(self.paddle.rect.x > initial_x)
        self.assertTrue(self.paddle.rect.right <= self.screen_width)

    def test_move_left_at_boundary(self):
        self.paddle.rect.x = 0
        self.paddle.move("left")
        self.assertEqual(self.paddle.rect.x, 0)

    def test_move_right_at_boundary(self):
        self.paddle.rect.x = self.screen_width - self.paddle.rect.width
        self.paddle.move("right")
        self.assertEqual(self.paddle.rect.right, self.screen_width)

    # Additional tests can be added for drawing functionality, if necessary.

class TestBall(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.screen_height = 600
        self.paddle = Paddle(400, 550, 100, 20, self.screen_width)
        self.ball = Ball(self.paddle)

    def tearDown(self):
        pg.quit()

    def test_initialization(self):
        self.assertEqual(self.ball.radius, 10)  # Assuming default radius of 10
        self.assertEqual(self.ball.color, (255, 255, 255))  # Assuming default color of WHITE
        self.assertEqual(self.ball.paddle, self.paddle)
        self.assertEqual(self.ball.x, self.paddle.rect.centerx)
        self.assertEqual(self.ball.y, self.paddle.rect.top - self.ball.radius)
        self.assertTrue(self.ball.attached_to_paddle)

    def test_handle_event_space_key(self):
        # Mocking pygame event for space key press
        mock_event = pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE)
        self.ball.handle_event(mock_event)
        self.assertFalse(self.ball.attached_to_paddle)
        self.assertNotEqual(self.ball.speed_x, 0)
        self.assertNotEqual(self.ball.speed_y, 0)

    def test_update_attached_to_paddle(self):
        self.ball.attached_to_paddle = True
        paddle_original_x = self.paddle.rect.centerx
        self.paddle.move("right")
        self.ball.update()
        self.assertEqual(self.ball.x, self.paddle.rect.centerx)
        self.assertNotEqual(self.ball.x, paddle_original_x)
        self.assertEqual(self.ball.y, self.paddle.rect.top - self.ball.radius)

    def test_update_not_attached(self):
        self.ball.attached_to_paddle = False
        original_x = self.ball.x
        original_y = self.ball.y
        self.ball.speed_x = 5
        self.ball.speed_y = -5
        self.ball.update()
        self.assertEqual(self.ball.x, original_x + 5)
        self.assertEqual(self.ball.y, original_y - 5)

    # Additional tests can be added for collision detection and drawing functionality.


class TestBrick(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.brick = Brick(100, 50, 50, 20)

    def tearDown(self):
        pg.quit()

    def test_initialization(self):
        self.assertEqual(self.brick.rect.x, 100)
        self.assertEqual(self.brick.rect.y, 50)
        self.assertEqual(self.brick.rect.width, 50)
        self.assertEqual(self.brick.rect.height, 20)
        self.assertEqual(self.brick.color, (255, 0, 0))  # Assuming default red color
        self.assertFalse(self.brick.is_destroyed)

    def test_draw(self):
        # Assuming screen setup
        screen = pg.display.set_mode((800, 600))
        # Since draw method involves pygame graphics, we primarily ensure it runs without error
        self.brick.draw(screen)
        # More detailed graphical testing is beyond the scope of unit testing

    def test_destroy(self):
        self.brick.destroy()
        self.assertTrue(self.brick.is_destroyed)
        self.assertEqual(self.brick.color, (0, 0, 0))  # Assuming the color changes to black




class TestLevel(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.mock_level_data = {
            "levels": [
                {
                    "name": "Level 1",
                    "layout": [[1, 1, 1], [0, 1, 0], [1, 0, 1]]
                }
            ]
        }

    def tearDown(self):
        pg.quit()

    @patch('builtins.open')
    @patch('json.load')
    def test_initialization(self, mock_json_load, mock_open):
        mock_json_load.return_value = self.mock_level_data
        level = Level(0)  # Load the first level
        mock_open.assert_called_with("levels.json", "r")
        mock_json_load.assert_called_once()
        self.assertEqual(level.level_name, "Level 1")
        self.assertEqual(len(level.bricks), 5)  # 5 bricks as per layout

    @patch('builtins.open')
    @patch('json.load')
    def test_invalid_level(self, mock_json_load, mock_open):
        mock_json_load.return_value = self.mock_level_data
        with self.assertRaises(ValueError):
            Level(99)  # An invalid level index

    # Additional tests can be added for methods like draw, is_level_complete, etc.


class TestScoreboard(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.scoreboard = Scoreboard(100, 50)

    def tearDown(self):
        pg.quit()

    def test_initialization(self):
        self.assertEqual(self.scoreboard.score, 0)
        self.assertEqual(self.scoreboard.x, 100)
        self.assertEqual(self.scoreboard.y, 50)
        self.assertIsNotNone(self.scoreboard.font)  # Check if font is set

    def test_increase_score(self):
        initial_score = self.scoreboard.score
        self.scoreboard.increase_score(10)
        self.assertEqual(self.scoreboard.score, initial_score + 10)

    def test_update(self):
        # Assuming update method might be extended in the future
        # For now, just ensure it doesn't raise errors
        self.scoreboard.update()

    def test_draw(self):
        # Since draw method involves pygame graphics, we primarily ensure it runs without error
        screen = pg.display.set_mode((800, 600))
        self.scoreboard.draw(screen)
        # More detailed graphical testing is beyond the scope of unit testing


class TestCollision(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.screen_height = 600
        self.paddle = Paddle(400, 550, 100, 20, self.screen_width)
        self.ball = Ball(self.paddle)
        self.bricks = [Brick(100, 50, 50, 20), Brick(200, 50, 50, 20)]

        self.collision = Collision(self.ball, self.paddle, self.bricks)

    def tearDown(self):
        pg.quit()

    def test_check_wall_collision(self):
        # Simulate collision with the left wall
        self.ball.rect.x = 0
        initial_speed_x = self.ball.speed_x
        self.collision.check_wall_collision()
        self.assertNotEqual(self.ball.speed_x, initial_speed_x)

        # Simulate collision with the right wall
        self.ball.rect.x = self.screen_width
        self.collision.check_wall_collision()
        self.assertNotEqual(self.ball.speed_x, initial_speed_x)

        # Simulate collision with the top wall
        self.ball.rect.y = 0
        initial_speed_y = self.ball.speed_y
        self.collision.check_wall_collision()
        self.assertNotEqual(self.ball.speed_y, initial_speed_y)

        # Note: Bottom wall collision may be game-specific (game over or similar logic)

    def test_check_paddle_collision(self):
        # Place the ball right on the paddle for collision
        self.ball.rect.centerx = self.paddle.rect.centerx
        self.ball.rect.bottom = self.paddle.rect.top
        initial_speed_y = self.ball.speed_y
        self.collision.check_paddle_collision()
        self.assertNotEqual(self.ball.speed_y, initial_speed_y)

    def test_check_brick_collision(self):
        # Position the ball to collide with a brick
        brick = self.bricks[0]
        self.ball.rect.centerx = brick.rect.centerx
        self.ball.rect.centery = brick.rect.centery
        initial_speed_y = self.ball.speed_y
        self.collision.check_brick_collision()
        self.assertNotEqual(self.ball.speed_y, initial_speed_y)
        self.assertTrue(brick.is_destroyed)

    # Additional tests can include specific edge cases or combinations of collisions.

class TestInputEvent(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.paddle = Paddle(400, 550, 100, 20, self.screen_width)
        self.ball = Ball(self.paddle)
        self.input_event = InputEvent(self.paddle, self.ball)

    def tearDown(self):
        pg.quit()

    @patch('pygame.key.get_pressed')
    def test_handle_input_move_left(self, mock_get_pressed):
        mock_get_pressed.return_value = {KEY_MOVE_LEFT: 1, KEY_MOVE_RIGHT: 0, pg.K_SPACE: 0}
        initial_x = self.paddle.rect.x
        self.input_event.handle_input()
        self.assertTrue(self.paddle.rect.x < initial_x)

    @patch('pygame.key.get_pressed')
    def test_handle_input_move_right(self, mock_get_pressed):
        mock_get_pressed.return_value = {KEY_MOVE_LEFT: 0, KEY_MOVE_RIGHT: 1, pg.K_SPACE: 0}
        initial_x = self.paddle.rect.x
        self.input_event.handle_input()
        self.assertTrue(self.paddle.rect.x > initial_x)

    @patch('pygame.event.Event')
    @patch('pygame.key.get_pressed')
    def test_handle_input_space_key(self, mock_get_pressed, mock_event):
        mock_get_pressed.return_value = {KEY_MOVE_LEFT: 0, KEY_MOVE_RIGHT: 0, pg.K_SPACE: 1}
        mock_event.return_value = pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE)
        self.input_event.handle_input()
        mock_event.assert_called_with(pg.KEYDOWN, key=pg.K_SPACE)
        self.ball.handle_event(mock_event.return_value)
        self.assertFalse(self.ball.attached_to_paddle)

    # Additional tests can be added for other key inputs or combinations.
        
class TestLevelBanner(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        self.level_banner = LevelBanner()

    def tearDown(self):
        pg.quit()

    def test_display(self):
        level_number = 1
        # Since display method involves pygame graphics and time delay, we primarily ensure it runs without error
        with patch('pygame.time.wait') as mock_wait:
            self.level_banner.display(self.screen, level_number, self.screen_width, self.screen_height)
            mock_wait.assert_called_with(2000)
            # More detailed graphical testing is beyond the scope of unit testing

class TestGameReset(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.screen_width = 800
        self.screen_height = 600
        self.current_level_index = 0
        self.level = Level(self.current_level_index)
        self.paddle = Paddle(400, 550, 100, 20, self.screen_width)
        self.ball = Ball(self.paddle)
        self.game = Mock()  # Mocking the game object
        self.game.level = self.level
        self.game.bricks = self.level.bricks
        self.game.paddle = self.paddle
        self.game.ball = self.ball
        self.game.collision = Collision(self.ball, self.paddle, self.game.bricks)
        self.game.screen_width = self.screen_width
        self.game.screen_height = self.screen_height
        self.game.current_level_index = self.current_level_index

        self.game_reset = GameReset(self.game)

    def tearDown(self):
        pg.quit()

    def test_reset(self):
        # Modify game state to simulate mid-game conditions
        self.game.paddle.rect.x = 300
        self.game.ball.attached_to_paddle = False
        self.game.ball.speed_x = 5
        self.game.ball.speed_y = -5

        self.game_reset.reset()

        # Check if level, paddle, and ball are reset
        self.assertEqual(self.game.level, self.level)
        self.assertEqual(self.game.bricks, self.level.bricks)
        self.assertEqual(self.game.paddle.rect.centerx, self.screen_width // 2)
        self.assertEqual(self.game.paddle.rect.y, 550)
        self.assertEqual(self.game.ball.x, self.game.paddle.rect.centerx)
        self.assertEqual(self.game.ball.y, self.game.paddle.rect.top - self.game.ball.radius)
        self.assertTrue(self.game.ball.attached_to_paddle)
        self.assertEqual(self.game.ball.speed_x, 0)
        self.assertEqual(self.game.ball.speed_y, 0)

        # Verify collision detection is reset with new bricks
        self.assertIsInstance(self.game.collision, Collision)
        self.assertEqual(self.game.collision.bricks, self.level.bricks)



if __name__ == '__main__':
    unittest.main()
