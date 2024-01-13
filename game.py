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
        with open("levels.json", "r") as file:
            self.levels = json.load(file)
        self.current_level = 0

        current_level_data = self.levels['levels'][self.current_level]
        self.level_name = current_level_data['name']
        self.level_map = current_level_data['layout']

        self.level_complete = False
        self.paddle = Paddle(350, 550, 100, 20, self.screen_width)  # Example dimensions
        self.ball = Ball(self.paddle)
        self.scoreboard = Scoreboard(10, 10)  # Position of the scoreboard
        self.collision = Collision(self.ball, self.paddle, [], self.screen_width, self.screen_height)

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
            keys = pg.key.get_pressed()
            if keys[KEY_MOVE_LEFT]:
                self.paddle.move("left")
            elif keys[KEY_MOVE_RIGHT]:
                self.paddle.move("right")
            if keys[pg.K_SPACE]:
                self.ball.handle_event(pg.event.Event(pg.KEYDOWN, key=pg.K_SPACE))
            self.collision.update()
            self.ball.update()

            self.level = Level(self.level_map)
            if self.level.is_level_complete():
                self.current_level += 1
                if self.current_level < len(self.levels['levels']):
                    self.level_map = self.levels['levels'][self.current_level]
                else:
                    # All levels are complete, handle game completion or ending
                    self.state = "Game Over"

    def draw(self):
        self.screen.fill(BLACK)
        # Draw game objects
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.level.draw(self.screen)
        self.scoreboard.draw(self.screen)




    def game_over(self):
        pass
