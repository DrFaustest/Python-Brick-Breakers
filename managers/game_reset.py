# This file contains the GameReset class, which is responsible for resetting the game state when the player loses all life or completes a level.
from levels.level import Level
from managers.collision import Collision
from typing import *
from settings import Settings

class GameReset:
    def __init__(self, game):
        """
        Initializes a new instance of the GameReset class.

        Parameters:
        - game: The game object.

        Returns:
        None
        """
        self.game = game
        self.settings = Settings()
        self.SCREEN_HEIGHT = self.settings.get("SCREEN_HEIGHT")
        self.BALL_RADIUS = self.settings.get("BALL_RADIUS")

    def reset(self) -> None:
        """
        Resets the game state.

        Parameters:
        None

        Returns:
        None
        """
        # Load the new level
        self.game.level = Level(self.game.current_level_index)
        self.game.bricks = self.game.level.bricks

        # Reset paddle position
        self.game.paddle.rect.centerx = self.game.screen_width // 2
        self.game.paddle.rect.y = self.SCREEN_HEIGHT - 60

        # Reset ball position and state
        self.game.ball.x = self.game.paddle.rect.centerx
        self.game.ball.y = self.game.paddle.rect.top - self.BALL_RADIUS
        self.game.ball.speed_x = 0
        self.game.ball.speed_y = 0
        self.game.ball.attached_to_paddle = True

        # Reset collision detection with the new bricks
        self.game.collision = Collision(self.game.ball, self.game.paddle, self.game.bricks, self.game.scoreboard, self.game.lives)

    def full_reset(self) -> None:
        self.game.current_level_index = 0
        self.game.scoreboard.score = 0
        self.game.lives.lives = 3
        self.reset()




