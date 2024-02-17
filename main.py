import pygame as pg
from game.game import Game
from settings import *
from logo import LogoDisplay

def main() -> None:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Brick Breaker")
    game = Game(screen)
    logo_display = LogoDisplay(screen)
    running = True
    clock = pg.time.Clock()
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.USEREVENT:
                game.background_music.play_next_track()
            if event.type == pg.QUIT:
                running = False
        if not logo_display.done:
            logo_display.update()
            logo_display.draw()
            pg.display.flip()
            continue
        else:
            game.update(events)
            game.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()
if __name__ == "__main__":
    main()
