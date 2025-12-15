import pygame as pg
import sys
import os
from game.game import Game
from settings import Settings
from logo import LogoDisplay

def setup_bundled_paths() -> None:
    """
    Adjust paths for PyInstaller bundled executable.
    When running as an exe, os.path.abspath('.') points to the temp extraction dir.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        os.chdir(sys._MEIPASS)

def main() -> None:
    """
    The main function that initializes the game and runs the game loop.

    Returns:
        None
    """
    setup_bundled_paths()
    pg.init()
    settings = Settings()
    screen_width: int = settings.get("SCREEN_WIDTH")
    screen_height: int = settings.get("SCREEN_HEIGHT")

    FPS: int = settings.get("FPS")
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Brick Breaker")
    game = Game(screen)
    logo_display = LogoDisplay(screen)
    running: bool = True
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
        else:
            game.update(events)
            game.draw()

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
