import pygame
import sys
from slider import Slider
from text_box import TextBox
from preview_window import PreviewWindow
from preview_window import PreviewWindow

BACKGROUND_IMAGES = ["img/background.webp", "img/background_2.webp", "img/background_3.webp", "img/background_4.webp"]
BALL_IMAGES = ["img/future_ball.png","img/retro_snow_ball.png","img/ring_ball.png"]
PADDLE_IMAGES = ["img/paddle.png"]

# Initialize Pygame
pygame.init()

def name_entered(name):
    print(f"Name entered: {name}")

# Set up the display
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
preview_window_background=PreviewWindow(screen, BACKGROUND_IMAGES,"Backgound" , 60, 10, 200,200)
preview_window_ball=PreviewWindow(screen, BALL_IMAGES,"Ball", 60, 250, 200,200)
preview_window_paddle=PreviewWindow(screen, PADDLE_IMAGES,"Paddle",60, 500, 200,100)
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            preview_window_background.handle_event(event)
            preview_window_ball.handle_event(event)
            preview_window_paddle.handle_event(event)
            
    preview_window_background.draw()
    preview_window_ball.draw()
    preview_window_paddle.draw()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
