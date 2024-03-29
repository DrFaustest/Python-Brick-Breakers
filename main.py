import pygame as pg
from game.game import Game
from settings import Settings
from logo import LogoDisplay

def main() -> None:
    pg.init()
    settings = Settings()
    screen_width = settings.get("SCREEN_WIDTH")
    screen_height = settings.get("SCREEN_HEIGHT")

    FPS = settings.get("FPS")
    screen = pg.display.set_mode((screen_width, screen_height))
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

        # Update the game state and draw every frame, not just when there are events
        if not logo_display.done:
            logo_display.update()  # Assuming there's an update method for logo_display
            logo_display.draw()
        else:
            game.update(events)  # Pass events to the game update for processing
            game.draw()

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
