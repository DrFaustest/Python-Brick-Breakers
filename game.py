import pygame as pg
from objects import *
from settings import * 

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.state = "Start"
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT



        self.current_level_index = 0
        self.level = Level(self.current_level_index)
        self.bricks = self.level.bricks


        self.paddle = Paddle(350, 550, 100, 20, self.screen_width)  # Example dimensions
        self.ball = Ball(self.paddle)
        self.scoreboard = Scoreboard(10, 10)  # Position of the scoreboard
        self.collision = Collision(self.ball, self.paddle, self.bricks, self.scoreboard)
        self.input_handler = InputEvent(self.paddle, self.ball)
        self.level_banner = LevelBanner()
        self.game_reset = GameReset(self)

    def start(self):
        self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)
        
        def change_to_playing():
            self.state = "Playing"
            self.screen.fill((0, 0, 0))

        play_button = Button(300, 150, 200, 100, "Play", (255, 255, 255), (0, 255, 0), (0, 0, 0), change_to_playing)
        play_button.draw(self.screen)
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                play_button.handle_event(event)

    def update(self):
        if self.state == "Playing":
            self.input_handler.handle_input()
            self.ball.update()
            self.collision.update()
            if self.level.is_level_complete():
                self.current_level_index += 1
                try:
                    self.game_reset.reset()
                    self.level_banner.display(self.screen, self.current_level_index + 1, self.screen_width, self.screen_height)
                except ValueError:
                    self.state = "Game Over"
                    self.screen.fill(WHITE)

    def draw(self):
        self.screen.fill(BLACK)
        # Draw game objects
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)




    def game_over(self):
        pass
