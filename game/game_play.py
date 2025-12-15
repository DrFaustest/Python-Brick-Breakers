import pygame as pg
from settings import Settings
from objects.paddle import Paddle
from objects.ball import Ball
from objects.brick import Brick
from levels.level import Level
from ui.level_banner import LevelBanner
from ui.scoreboard import Scoreboard
from ui.player_lives import PlayerLives
from managers.collision import Collision
from managers.input import InputEvent
from managers.game_reset import GameReset
from game.game_state import GameState

class GamePlay(GameState):
    def __init__(self, game) -> None:
        """
        Initialize the GamePlay class.

        Args:
            game (Game): The game instance.

        Attributes:
            difficulty (float): The game difficulty.
            background_image (Surface): The background image of the game.
            current_level_index (int): The index of the current level.
            level (Level): The current level.
            bricks (list): The list of bricks in the level.
            paddle (Paddle): The game paddle.
            ball (Ball): The game ball.
            scoreboard (Scoreboard): The game scoreboard.
            lives (PlayerLives): The player lives.
            collision (Collision): The collision manager.
            input_handler (InputEvent): The input event manager.
            level_banner (LevelBanner): The level banner UI.
            game_reset (GameReset): The game reset manager.
        """
        super().__init__(game)
        self.difficulty: float = self.settings.get("DIFFICULTY")
        self.background_image: pg.Surface = pg.image.load(self.settings.get("BACKGROUND_IMG")).convert()
        self.background_image = pg.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.current_level_index: int = 0
        self.level: Level = Level(self.current_level_index)
        self.bricks: list[Brick] = self.level.bricks
        self.paddle: Paddle = Paddle()
        self.balls: list[Ball] = [Ball(self.paddle)]  # Changed to list to support multiple balls
        self.scoreboard: Scoreboard = Scoreboard()
        self.lives: PlayerLives = PlayerLives()
        self.collision: Collision = Collision(self.balls, self.paddle, self.level, self.scoreboard, self.lives, self.screen, self)
        self.input_handler: InputEvent = InputEvent(self.paddle, self.balls)
        self.level_banner: LevelBanner = LevelBanner()
        self.game_reset: GameReset = GameReset(self)
        self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)

    def update(self, events: list[pg.event.Event]) -> None:
        """
        Update the game logic in the playing state.

        Args:
            events (list): The list of pygame events.

        Returns:
            None
        """
        self.input_handler.handle_input()
        self.level.update()  # Update bricks (for moving bricks)
        
        # Update all balls
        for ball in self.balls[:]:
            ball.update()
        
        self.collision.update()
        if self.level.is_level_complete():
            self.handle_level_complete()
        if self.lives.lives == 0:
            self.settings.set("DIFFICULTY", 1)
            self.game.player_score = self.scoreboard.score
            self.game.change_state("GameOver")

    def handle_level_complete(self) -> None:
        """
        Handle the completion of a level.

        Returns:
            None
        """
        self.current_level_index += 1
        if self.difficulty < 10:
            new_difficulty: float = self.difficulty + 0.2
            self.settings.set("DIFFICULTY", new_difficulty)
            self.difficulty = self.settings.get("DIFFICULTY")
        self.game_reset.reset()
        self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)

    def draw(self) -> None:
        """
        Draw the game objects on the screen.

        Returns:
            None
        """
        self.screen.blit(self.background_image, (0, 0))
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        
        # Draw all balls
        for ball in self.balls:
            ball.draw(self.screen)
        
        self.lives.draw(self.screen)
