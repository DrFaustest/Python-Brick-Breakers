import pygame
import sys
from slider import Slider
from text_box import TextBox

# Initialize Pygame
pygame.init()

def name_entered(name):
    print(f"Name entered: {name}")

# Set up the display
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
input_box = TextBox(100, 100, 140, 32, name_entered, "Enter your name: ")
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        input_box.handle_event(event)

    screen.fill((0, 0, 0))  # Clear screen with black
    input_box.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
