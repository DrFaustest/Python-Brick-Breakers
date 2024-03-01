import pygame
from pygame.locals import *

class PreviewWindow:
    def __init__(self, image_list, x, y, window_size):
        self.image_list = image_list
        self.index = 0
        self.x = x
        self.y = y
        self.window_size = window_size
        self.window = pygame.display.set_mode(window_size)
        self.button_width = 50  # Width of the left/right buttons
        self.button_height = 50  # Height of the left/right buttons
        self.load_images()
        self.create_buttons()

    def draw(self, screen):
        self.draw_image()
        self.draw_buttons()
        

    def load_images(self):
        # Load and scale images to fit the window, maintaining aspect ratio
        self.images = []
        for img in self.image_list:
            image = pygame.image.load(img)
            self.images.append(pygame.transform.scale(image, (self.window_size[0] - 2 * self.button_width, self.window_size[1])))

    def create_buttons(self):
        # Create left and right buttons
        self.left_button = pygame.Rect(0, (self.window_size[1] - self.button_height) // 2, self.button_width, self.button_height)
        self.right_button = pygame.Rect(self.window_size[0] - self.button_width, (self.window_size[1] - self.button_height) // 2, self.button_width, self.button_height)

    def draw_buttons(self):
        # Draw left and right buttons
        pygame.draw.rect(self.window, (100, 100, 100), self.left_button)  # Draw left button
        pygame.draw.rect(self.window, (100, 100, 100), self.right_button)  # Draw right button

        # You can add text or arrows to the buttons here

    def draw_image(self):
        # Clear the window
        self.window.fill((255, 255, 255))
        # Draw the current image
        self.window.blit(self.images[self.index], (self.x + self.button_width, self.y))
        # Draw navigation buttons
        self.draw_buttons()
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_button.collidepoint(event.pos):
                self.index = (self.index - 1) % len(self.images)
                self.draw_image()
            elif self.right_button.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.images)
                self.draw_image()





