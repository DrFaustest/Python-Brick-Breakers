from settings import *
from ui.button import Button
from ui.slider import Slider
import pygame as pg
import game
'''
this is going to update and save the settings, first we need a back button and a save button, I want the back button to turn red if changes have been made and not saved as a visual indicator to the user

I want to have a preview window window that shows the ball, paddle, and background, a left and right arrow for each will sysle between each image in the corrosponding list

I want a volume slider that adjusts the volume of the game

This class is its own scene, so it will have its own update and draw methods
'''

class SettingsMenu:
    def __init__(self):
        self.unsaved_changes = False
        # Initialize buttons, slider, and preview window here
        self.back_button = Button(0, 0, 100, 100, "BACK", WHITE, GRAY, self.back_button_color, self.change_to_start)
        self.save_button = Button(SCREEN_WIDTH - 100, 0, 100, 100, "SAVE", WHITE, GRAY, BLACK, self.save_settings)
        self.volume_slider = Slider(...)  # Define slider properties and handler
        # Initialize preview window and its elements

    def update(self):
        # Update logic, including handling arrow buttons for preview cycling
        # and volume slider adjustments
        pass

    def draw(self, screen):
        # Draw settings elements, including changing the back button's color if unsaved changes exist
        if self.unsaved_changes:
            self.back_button.color = RED  # Assuming your Button class can handle color changes
        else:
            self.back_button.color = GRAY
        # Draw other elements (buttons, sliders, preview window)

    def save_settings(self):
        # Save the settings and reset unsaved_changes flag
        self.unsaved_changes = False

    def change_preview(self, category, direction):
        # Change the preview images based on arrow button input
        pass

    @property
    def back_button_color(self):
        return RED if self.unsaved_changes else GRAY

    # Additional methods as needed for functionality