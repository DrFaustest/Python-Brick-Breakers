import pygame as pg
from settings import *

class Button:
    def __init__(self, x:int, y:int, width:int = 200, height:int = 100, text:str = "Change ME", color:tuple =(WHITE) , hover_color:tuple = (0, 255, 0), text_color:tuple = (BLACK), action: callable = None) -> None:
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.font = pg.font.SysFont("Arial", 50)
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                if self.action is not None:
                    self.action()