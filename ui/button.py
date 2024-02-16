import pygame as pg
from settings import *

class Button:
    def __init__(self, x: int, y: int, width: int = None, height: int = None, text: str = "change me", color: tuple = WHITE, hover_color: tuple = GRAY, text_color: tuple = BLACK, action: callable = None, image: pg.Surface = None) -> None:
        self.image = image
        if self.image is not None:
            # If an image is provided and no width/height are specified, use the image's dimensions
            if width is None or height is None:
                width, height = self.image.get_size()
        else:
            # Default to provided dimensions or a standard size if none are specified
            width = width if width is not None else 200
            height = height if height is not None else 100

        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.font = pg.font.SysFont("Arial", 50)

    def draw(self, screen):
        # Draw the button image if provided, otherwise draw a rectangle
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pg.draw.rect(screen, self.color, self.rect)
        # Draw text in the center of the button/image
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        # Change color or image on hover, depending on your design
        if self.rect.collidepoint(mouse_pos) and not self.image:  # Only change color if no image is used
            self.color = self.hover_color

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos) and self.action:
                self.action()
