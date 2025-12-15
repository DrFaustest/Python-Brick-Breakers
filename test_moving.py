import pygame as pg
from levels.level import Level

pg.init()
screen = pg.display.set_mode((800, 600))

l = Level(0)
moving_bricks = [b for b in l.bricks if hasattr(b, 'velocity')]

if moving_bricks:
    mb = moving_bricks[0]
    print(f'Start X: {mb.rect.x}, Velocity: {mb.velocity}')
    
    for i in range(10):
        l.update()
        print(f'Frame {i+1} X: {mb.rect.x}')
else:
    print("No moving bricks found!")

pg.quit()
