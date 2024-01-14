import pygame as pg
from game import Game
from settings import *

'''
This module is the main function to run Brick Breaker. It initializes the game and runs the game loop, sets up the game window, and controls the game loop. the game has three states: start, playing, and game over. The game starts in the start state, where the player can click the play button to start the game. The game then moves to the playing state, where the player can move the paddle and hit the ball to break the bricks. The game ends when the player clears all the bricks or the ball hits the bottom of the screen. The game then moves to the game over state, where the player can click the play button to restart the game.

Classes: 
    Game: Handles the game logic, and updates, and rendering.

Constants:
    SCREEN_WIDTH: The width of the game window as determined in the settings module.
    SCREEN_HEIGHT: The height of the game window as determined in the settings module.
    FPS: The frame rate of the game as determined in the settings module.

Functions:
    main(): Initializes the game and runs the game loop and processes user input.
'''

def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("brick breaker")
    clock = pg.time.Clock()
    clock.tick(FPS)
    game = Game(screen)
    running = True
    while running:
        if game.state == "Start":
            game.start()
        elif game.state == "Playing":
            game.update()
            game.draw()
        elif game.state == "Game Over":
            game.game_over()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.flip()
    pg.quit()

if __name__ == "__main__":
    main()

    