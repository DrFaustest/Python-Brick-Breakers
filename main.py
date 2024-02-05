import pygame as pg
from game.game import Game
from settings import *
from typing import *


def main() -> None:
    pg.init()
    screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("brick breaker")
    clock: pg.time.Clock = pg.time.Clock()
    clock.tick(FPS)
    game: Game = Game(screen)
    running: bool = True
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

    