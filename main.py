import pygame as pg
from game.game import Game
from settings import *

def main() -> None:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Brick Breaker")
    game = Game(screen)
    running = True
    clock = pg.time.Clock()
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        game.update(events)  # Pass the events to the game update method
        game.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()
if __name__ == "__main__":
    main()
