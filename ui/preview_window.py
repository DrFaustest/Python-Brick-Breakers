import pygame
from pygame.locals import *

class PreviewWindow:
    def __init__(self,screen, image_list,image_description, x, y, display_width, display_height):
        self.window = screen
        self.image_list = image_list
        self.image_description = image_description
        self.index = 0
        self.x = x
        self.y = y
        self.display_width = display_width
        self.display_height = display_height
        self.button_width = 50
        self.button_height = 50
        self.load_images()
        self.create_buttons()

    def draw(self):
        self.draw_image()
        self.draw_buttons()

    def draw_text(self, text, position, font_size=20, text_color=(255, 255, 255), background_color=None):
        font = pygame.font.Font(None, font_size)  # None uses the default font
        text_surface = font.render(text, True, text_color, background_color)
        text_rect = text_surface.get_rect(center=position)
        self.window.blit(text_surface, text_rect)


    def load_images(self):
        self.images = []
        for img in self.image_list:
            image = pygame.image.load(img)
            img_width, img_height = image.get_size()
            scale_factor = min((self.display_width - 2 * self.button_width) / img_width, self.display_height / img_height)
            new_size = (int(img_width * scale_factor), int(img_height * scale_factor))
            self.images.append(pygame.transform.scale(image, new_size))

    def create_buttons(self):
        mid_y = self.y + (self.display_height - self.button_height) // 2
        self.left_button = pygame.Rect(self.x - self.button_width, mid_y, self.button_width, self.button_height)
        self.right_button = pygame.Rect(self.x + self.display_width, mid_y, self.button_width, self.button_height)

    def draw_buttons(self):
        pygame.draw.rect(self.window, (100, 100, 100), self.left_button)
        pygame.draw.rect(self.window, (100, 100, 100), self.right_button)
        font = pygame.font.Font(None, 40)
        left_arrow = font.render("<", True, (255, 255, 255))
        right_arrow = font.render(">", True, (255, 255, 255))
        left_arrow_pos = left_arrow.get_rect(center=self.left_button.center)
        right_arrow_pos = right_arrow.get_rect(center=self.right_button.center)
        self.window.blit(left_arrow, left_arrow_pos)
        self.window.blit(right_arrow, right_arrow_pos)

    def draw_image(self):
        self.window.fill((255, 255, 255), (self.x, self.y, self.display_width, self.display_height))
        descriptive_text = self.image_description
        self.draw_text(descriptive_text, (self.x + self.display_width // 2, self.y + self.display_height + 20))
        current_image = self.images[self.index]
        image_width, image_height = current_image.get_size()
        scale_factor_w = self.display_width / image_width
        scale_factor_h = self.display_height / image_height
        scale_factor = min(scale_factor_w, scale_factor_h)
        new_image_width = int(image_width * scale_factor)
        new_image_height = int(image_height * scale_factor)
        image_x = self.x + (self.display_width - new_image_width) // 2
        image_y = self.y + (self.display_height - new_image_height) // 2
        self.window.blit(pygame.transform.scale(current_image, (new_image_width, new_image_height)), (image_x, image_y))
        self.draw_buttons()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_button.collidepoint(event.pos):
                self.index = (self.index - 1) % len(self.images)
                self.draw_image()
            elif self.right_button.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.images)
                self.draw_image()

    def get_image(self):
        return self.images[self.index]