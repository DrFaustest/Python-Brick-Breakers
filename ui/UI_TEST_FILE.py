import pygame
import sys
from slider import Slider
from text_box import TextBox
from button import Button
from preview_window import PreviewWindow
from preview_window import PreviewWindow

BACKGROUND_IMAGES = ["img/backgrounds/background_2.webp","img/backgrounds/background_3.webp","img/backgrounds/background_4.webp"]
BALL_IMAGES = ["img/balls/future_ball.png","img/balls/retro_snow_ball.png","img/balls/ring_ball.png"]
PADDLE_IMAGES = ["img/paddles/paddle.png"]
BRICK_IMAGES = ["img/bricks/brick_img.png","img/bricks/brick_img1.png","img/bricks/pattern_brick.png"]

# Initialize Pygame
pygame.init()

def name_entered(name):
    print(f"Name entered: {name}")

def print_volume():
    value = volume_slider.get_value()
    print(f"Volume: {value}")

# Set up the display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
preview_window_background=PreviewWindow(screen, BACKGROUND_IMAGES,"Backgound" , 60, 100, 200,200)
preview_window_ball=PreviewWindow(screen, BALL_IMAGES,"Ball", 400, 100, 200,200)
preview_window_paddle=PreviewWindow(screen, PADDLE_IMAGES,"Paddle",60, 375, 200,100)
volume_slider = Slider(screen, 350, 375, 300, 100, 0, 100, 50, "Volume")
save_button = Button(screen, 350, 500, 300, 100, "Save", (255, 255, 255), (0, 255, 0), (0, 0, 0), lambda: print_volume())
done = False



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            preview_window_background.handle_event(event)
            preview_window_ball.handle_event(event)
            preview_window_paddle.handle_event(event)
            volume_slider.handle_event(event)
            save_button.handle_event(event)
            
    preview_window_background.draw()
    preview_window_ball.draw()
    preview_window_paddle.draw()
    volume_slider.draw()
    save_button.draw()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
