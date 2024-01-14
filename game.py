import pygame as pg
from objects import *
import json
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
        self.collision = Collision(self.ball, self.paddle, self.bricks)
        self.input_handler = InputEvent(self.paddle, self.ball)

    def start(self):
        
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
                    self.level = Level(self.current_level_index)
                    self.bricks = self.level.bricks
                except ValueError:
                    # All levels are complete, handle game completion or ending
                    self.state = "Game Over"
                    self.screen.fill((BLACK))
                    self.scoreboard.draw(self.screen)

    def draw(self):
        self.screen.fill(BLACK)
        # Draw game objects
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)




    def game_over(self):
        pass
