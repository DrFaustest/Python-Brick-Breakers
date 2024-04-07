import pygame as pg
from game.game_state import GameState
from settings import Settings
from ui.button import Button
from ui.preview_window import PreviewWindow


class SettingsMenu(GameState):
    """
    Represents the settings menu state of the game.

    Inherits from the GameState class.

    Attributes:
    - TAB_HEIGHT: The height of the tab buttons.
    - BUTTON_WIDTH: The width of the buttons.
    - BUTTON_HEIGHT: The height of the buttons.
    - PADDING: The padding between elements.
    - MIDDLE_PANEL_HEIGHT: The height of the middle panel.
    - MIDDLE_PANEL_WIDTH: The width of the middle panel.
    - settings: An instance of the Settings class.
    - screen: The game screen.
    - WHITE: The white color.
    - GREEN: The green color.
    - BLACK: The black color.
    - GRAY: The gray color.
    - tab_buttons: A list of tab buttons.
    - current_tab: The currently selected tab.
    - tabs_content: A dictionary mapping tab names to PreviewWindow instances.
    - save_button: The save button.
    - exit_button: The exit button.

    Methods:
    - __init__(self, game): Initializes the SettingsMenu instance.
    - create_tabs(self): Creates the tab buttons.
    - change_tab(self, tab_name): Changes the current tab.
    - handle_events(self, event): Handles events.
    - draw(self): Draws the settings menu.
    - draw_text_with_padding(self, text, button): Draws text with padding.
    - save(self): Saves the settings.
    - update(self, events): Updates the settings menu state.
    - check_current_tab_state(self): Checks the state of the current tab.
    """
    
    TAB_HEIGHT = 40  
    BUTTON_WIDTH = 120  
    BUTTON_HEIGHT = 40  
    PADDING = 5  
    MIDDLE_PANEL_HEIGHT = 300  
    MIDDLE_PANEL_WIDTH = 600  

    def __init__(self, game):
        """
        Initializes the SettingsMenu instance.

        Parameters:
        - game: The game instance.
        """
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
        """
        Creates the tab buttons.
        """
        tab_images = self.settings.get("TAB_IMAGES")
        tab_images = []
        for img in self.settings.get("TAB_IMAGES"):
            tab_images.append(pg.image.load(img))
        for img in tab_images:
            img = pg.transform.scale(img, (self.BUTTON_WIDTH, self.TAB_HEIGHT))
        #"TAB_IMAGES": ["img\\tab_img\\ball_tab_img.png","img\\tab_img\\paddles_tab_img.png","img\\tab_img\\background_tab_img.png","img\\tab_img\\bricks_tab_img.png"]
        tab_names = ['Balls', 'Paddles', 'Background', 'Bricks']
        total_tab_width = self.settings.get("SCREEN_WIDTH") - (len(tab_names) + 1) * self.PADDING
        self.BUTTON_WIDTH = total_tab_width // len(tab_names)
        self.tab_buttons.clear()
        for index, (name,tab_img) in enumerate(zip(tab_names,tab_images)):
            button_x = index * (self.BUTTON_WIDTH + self.PADDING) + self.PADDING
            button_y = self.PADDING
            button_color = self.GREEN if name == self.current_tab else self.GRAY

            button = Button(self.screen, button_x, button_y, self.BUTTON_WIDTH, self.TAB_HEIGHT, '',
                self.WHITE, button_color, self.BLACK,
                lambda n=name: self.change_tab(n), tab_img)
            self.tab_buttons.append(button)

    def change_tab(self, tab_name):
        """
        Changes the current tab.
    
        Parameters:
        - tab_name: The name of the tab to change to.
        """
        for tab in self.tabs_content:
            if tab == tab_name:
                self.tabs_content[tab].selected = True
                self.current_tab = tab_name
            else:
                self.tabs_content[tab].selected = False
    
        self.create_tabs()

    def handle_events(self, event):
        """
        Handles events.

        Parameters:
        - event: The event to handle.
        """
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            for button in self.tab_buttons:
                button.update(event)
            self.tabs_content[self.current_tab].handle_event(event)
            self.save_button.update(event)
            self.exit_button.update(event)

    def draw(self):
        """
        Draws the settings menu.
        """
        self.screen.fill(self.BLACK)
        for button in self.tab_buttons:
            button.draw()
        self.tabs_content[self.current_tab].draw()
        self.save_button.draw()
        self.exit_button.draw()

    def draw_text_with_padding(self, text, button):
        """
        Draws text with padding.

        Parameters:
        - text: The text to draw.
        - button: The button to center the text on.
        """
        font = pg.font.SysFont("Arial", 22)  
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button.rect.center)
        self.screen.blit(text_surface, text_rect)

    def save(self):
        """
        Saves the settings.
        """
        if hasattr(self.tabs_content[self.current_tab], 'get_value'):
            key, value = self.tabs_content[self.current_tab].get_value()
            self.settings.set(key+"_IMG", value)
            self.save_button.error = False

    def update(self, events):
        """
        Updates the settings menu state.

        Parameters:
        - events: The list of events to update.
        """
        self.check_current_tab_state()
        self.save_button.update(events)
        self.exit_button.update(events)
        for event in events:
            self.handle_events(event)

    def check_current_tab_state(self):
        """
        Checks the state of the current tab.
        """
        key, value = self.tabs_content[self.current_tab].get_value()
        set_val = self.settings.get(key+"_IMG")
        if value != set_val:
            self.save_button.error = True
        else:
            self.save_button.error = False

