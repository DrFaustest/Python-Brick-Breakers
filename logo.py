import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class LogoDisplay:
    def __init__(self, screen, duration=4000):
        self.screen = screen
        original_logo = pg.image.load("img\logo.png.webp").convert_alpha()
                 # Calculate the new size to maintain aspect ratio within screen bounds
        logo_width, logo_height = original_logo.get_size()
        aspect_ratio = logo_width / logo_height
        
        # Use screen width and height as max size
        max_width, max_height = SCREEN_WIDTH, SCREEN_HEIGHT
        
        # Calculate new dimensions maintaining aspect ratio
        if logo_width > max_width or logo_height > max_height:
            if (max_width / logo_width) < (max_height / logo_height):
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
        else:
            # If the logo is smaller than the screen size, no need to resize
            new_width, new_height = logo_width, logo_height
        
        # Resize the logo
        self.logo = pg.transform.scale(original_logo, (new_width, new_height))
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.duration = duration
        self.start_ticks = pg.time.get_ticks()
        self.done = False

    def update(self):
        # Calculate the elapsed time
        elapsed_time = pg.time.get_ticks() - self.start_ticks
        if elapsed_time > self.duration:
            self.done = True
            return

        # Calculate the alpha value for fade-in and fade-out
        half_duration = self.duration // 2
        if elapsed_time < half_duration:
            # Fade in
            alpha = (elapsed_time / half_duration) * 255
        else:
            # Fade out
            alpha = ((self.duration - elapsed_time) / half_duration) * 255

        self.alpha = max(min(alpha, 255), 0)  # Ensure alpha stays in the 0-255 range

    def draw(self):
        if not self.done:
            self.screen.fill((0, 0, 0))  # Optional: Fill screen with black
            logo_copy = self.logo.copy()
            logo_copy.fill((255, 255, 255, int(self.alpha)), None, pg.BLEND_RGBA_MULT)
            self.screen.blit(logo_copy, self.logo_rect)
