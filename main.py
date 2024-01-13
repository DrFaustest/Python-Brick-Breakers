import pygame as pg
from game import Game

def main():
    pg.init()
    screen = pg.display.set_mode((800,600))
    pg.display.set_caption("brick breaker")
    clock = pg.time.Clock()
    clock.tick(60)
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

    