import pygame as pg
from game.game_state import GameState
from settings import Settings
from ui.button import Button
from ui.slider import Slider
from ui.preview_window import PreviewWindow

class SettingsMenu(GameState):
    TAB_HEIGHT = 40  # Adjusted for better fit
    BUTTON_WIDTH = 120  # Adjusted for better fit
    BUTTON_HEIGHT = 40  # Adjusted for better fit
    PADDING = 5  # Reduced padding for a tighter fit
    MIDDLE_PANEL_HEIGHT = 300  # Height for the PreviewWindow and Slider
    MIDDLE_PANEL_WIDTH = 600  # Width for the PreviewWindow and Slider

    def __init__(self, game):
        super().__init__(game)
        self.settings = Settings()
        self.screen = game.screen
        self.WHITE = self.settings.get("WHITE")
        self.GREEN = self.settings.get("GREEN")
        self.BLACK = self.settings.get("BLACK")
        self.GRAY = self.settings.get("GRAY")
        self.tab_buttons = []
        self.current_tab = 'Balls'
        middle_panel_x = (self.settings.get("SCREEN_WIDTH") - self.MIDDLE_PANEL_WIDTH) // 2
        middle_panel_y = (self.settings.get("SCREEN_HEIGHT") - self.MIDDLE_PANEL_HEIGHT) // 2
        self.tabs_content = {
            'Balls': PreviewWindow(self.screen, self.settings.get("BALL_IMAGES"), "BALL", middle_panel_x, middle_panel_y, self.MIDDLE_PANEL_WIDTH, self.MIDDLE_PANEL_HEIGHT) ,
            'Paddles': PreviewWindow(self.screen, self.settings.get("PADDLE_IMAGES"), "PADDLE", middle_panel_x, middle_panel_y, self.MIDDLE_PANEL_WIDTH, self.MIDDLE_PANEL_HEIGHT),
            'Background': PreviewWindow(self.screen, self.settings.get("BACKGROUND_IMAGES"), "BACKGROUND", middle_panel_x, middle_panel_y, self.MIDDLE_PANEL_WIDTH, self.MIDDLE_PANEL_HEIGHT),
            'Bricks': PreviewWindow(self.screen, self.settings.get("BRICK_IMAGES"), "BRICK", middle_panel_x, middle_panel_y, self.MIDDLE_PANEL_WIDTH, self.MIDDLE_PANEL_HEIGHT),
        }
        save_button_x = self.PADDING
        save_button_y = self.settings.get("SCREEN_HEIGHT") - self.BUTTON_HEIGHT - self.PADDING
        exit_button_x = self.settings.get("SCREEN_WIDTH") - self.BUTTON_WIDTH - self.PADDING
        exit_button_y = save_button_y
        self.save_button = Button(self.screen, save_button_x, save_button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Save", self.WHITE, self.GREEN, self.BLACK, self.save)
        self.exit_button = Button(self.screen, exit_button_x, exit_button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, "Exit", self.WHITE, self.GREEN, self.BLACK, lambda: self.game.change_state("MainMenu"))
        self.create_tabs()

    def create_tabs(self):
        tab_names = ['Balls', 'Paddles', 'Background', 'Bricks']
        total_tab_width = self.settings.get("SCREEN_WIDTH") - (len(tab_names) + 1) * self.PADDING
        self.BUTTON_WIDTH = total_tab_width // len(tab_names)
        self.tab_buttons.clear()
        for index, name in enumerate(tab_names):
            button_x = index * (self.BUTTON_WIDTH + self.PADDING) + self.PADDING
            button_y = self.PADDING
            button_color = self.GREEN if name == self.current_tab else self.GRAY

            button = Button(self.screen, button_x, button_y, self.BUTTON_WIDTH, self.TAB_HEIGHT, name,
                            self.WHITE, button_color, self.BLACK,
                            action=lambda n=name: self.change_tab(n))
            self.tab_buttons.append(button)



    def change_tab(self, tab_name):
        if tab_name in self.tabs_content:
            self.current_tab = tab_name
            self.create_tabs()

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            for button in self.tab_buttons:
                button.update(event.pos, event)
            self.tabs_content[self.current_tab].handle_event(event)
            self.save_button.update(event.pos, event)
            self.exit_button.update(event.pos, event)

    def draw(self):
        self.screen.fill(self.BLACK)
        for button in self.tab_buttons:
            button.draw()
        # Draw the currently selected tab's content
        self.tabs_content[self.current_tab].draw()
        # Ensure padding around the text in buttons
        self.draw_text_with_padding("Save", self.save_button)
        self.draw_text_with_padding("Exit", self.exit_button)

    def draw_text_with_padding(self, text, button):
        font = pg.font.SysFont("Arial", 22)  # Smaller font size for button text
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button.rect.center)
        self.screen.blit(text_surface, text_rect)

    def save(self):
        # Save the current settings
        if hasattr(self.tabs_content[self.current_tab], 'get_value'):
            key, value = self.tabs_content[self.current_tab].get_value()
            self.settings.set(key+"_IMG", value)

    def update(self, events):
        for event in events:
            self.handle_events(event)

