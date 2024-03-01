import pygame as pg
from settings import *
from ui.button import Button
from ui.slider import Slider
from ui.preview_window import PreviewWindow

class SettingsMenu:
    def __init__(self):
        self.unsaved_changes = False
        # Initialize buttons
        self.back_button = Button(0, 0, 100, 50, "BACK", WHITE, self.back_button_color, self.back_button_action)
        self.save_button = Button(SCREEN_WIDTH - 100, 0, 100, 50, "SAVE", WHITE, GRAY, BLACK, self.save_settings)
        
        # Initialize preview windows
        self.ball_preview = PreviewWindow(BALL_IMAGES, 100, 100, (200, 200))
        self.paddle_preview = PreviewWindow(PADDLE_IMAGES, 100, 300, (200, 200))
        self.background_preview = PreviewWindow(BACKGROUND_IMAGES, 100, 500, (200, 200))
        
        # Initialize slider
        self.volume_slider = Slider(SCREEN_WIDTH // 2 - 100, 650, 200, 20, 0, 100, VOLUME * 100, "Volume")

    def update(self):
        # Here you would check for input, update UI elements, etc.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Update button states based on user interaction
            self.back_button.update(pg.mouse.get_pos(), event)
            self.save_button.update(pg.mouse.get_pos(), event)
            # Update sliders
            self.volume_slider.handle_event(event)
            # Update preview windows
            self.ball_preview.handle_event(event)
            self.paddle_preview.handle_event(event)
            self.background_preview.handle_event(event)

            if self.unsaved_changes:
                self.back_button.color = self.back_button_color

    def draw(self, screen):
        # Draw the back and save buttons
        self.back_button.draw(screen)
        self.save_button.draw(screen)
        # Draw the preview windows
        self.ball_preview.draw(screen)
        self.paddle_preview.draw(screen)
        self.background_preview.draw(screen)
        # Draw the slider
        self.volume_slider.draw(screen)

    def back_button_action(self):
        # Define the action for the back button
        # This might involve changing the scene or updating a state
        pass

    def save_settings(self):
        # Save the settings and reset the unsaved_changes flag
        self.unsaved_changes = False

    def update_volume(self, value):
        # Update the volume based on the slider value
        # This would typically involve setting the volume in the game's settings or audio system
        pass

    @property
    def back_button_color(self):
        # Dynamic property to get the current color for the back button
        return RED if self.unsaved_changes else GRAY