import pygame as pg

class Button:
    def __init__(self, screen: pg.Surface, x: int, y: int, width: int = None, 
                 height: int = None, text: str = "change me", 
                 color: tuple = (255, 255, 255), hover_color: tuple = (128, 128, 128), 
                 text_color: tuple = (0, 0, 0), action: callable = None, 
                 image: pg.Surface = None, hover_image: pg.Surface = None, selected_image: pg.Surface = None) -> None:
        """
        Initializes a Button object.

        Parameters:
        - screen (pg.Surface): The pygame screen to draw the button on.
        - x (int): The x-coordinate of the button's top-left corner.
        - y (int): The y-coordinate of the button's top-left corner.
        - width (int, optional): The width of the button. If not provided, defaults to 200.
        - height (int, optional): The height of the button. If not provided, defaults to 100.
        - text (str, optional): The text displayed on the button. Defaults to "change me".
        - color (tuple, optional): The color of the button. Defaults to (255, 255, 255) (white).
        - hover_color (tuple, optional): The color of the button when hovered over. Defaults to (128, 128, 128) (gray).
        - text_color (tuple, optional): The color of the button's text. Defaults to (0, 0, 0) (black).
        - action (callable, optional): The function to be executed when the button is clicked. Defaults to None.
        - image (pg.Surface, optional): The image to be displayed on the button. Defaults to None.
        - hover_image (pg.Surface, optional): The image to be displayed on the button when hovered over. Defaults to None.
        - selected_image (pg.Surface, optional): The image to be displayed on the button when selected. Defaults to None.
        """
        self.image: pg.Surface = image
        self.screen: pg.Surface = screen
        if self.image is not None:
            if width is None or height is None:
                width, height = self.image.get_size()
        else:
            width = width if width is not None else 200
            height = height if height is not None else 100
        
        self.x: int = x
        self.y: int = y
        self.error: bool = False
        self.hover: bool = False
        self.selected: bool = False
        self.error_color: tuple = (255, 0, 0)
        self.rect: pg.Rect = pg.Rect(x, y, width, height)
        self.default_color: tuple = color
        self.color: tuple = color
        self.hover_color: tuple = hover_color
        self.text: str = text
        self.text_color: tuple = text_color
        self.action: callable = action
        self.hitbox: pg.Rect = self.rect
        self.font: pg.font.Font = pg.font.SysFont("Arial", 50)
        self.default_image: pg.Surface = image
        self.hover_image: pg.Surface = hover_image
        self.selected_image: pg.Surface = selected_image


    def draw(self) -> None:
        """
        Draws the button on the screen.
        """
        self.check_hover()

        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pg.draw.rect(self.screen, self.color, self.rect)

        if self.text:
            text_str = str(self.text)
            text_color = self.text_color if isinstance(self.text_color, tuple) and len(self.text_color) in [3, 4] else (0, 0, 0)
            text_surface = self.font.render(text_str, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.screen.blit(text_surface, text_rect)

    def check_hover(self) -> bool:
        """
        Checks if the button is being hovered over and changes its appearance accordingly.
    
        Returns:
            bool: True if the mouse is hovering over the button, False otherwise.
        """
        mouse_pos = pg.mouse.get_pos()
        is_hovering = self.rect.collidepoint(mouse_pos)
    
        if not is_hovering:
            self.handle_not_hovering()
            return False
    
        if not self.image:
            self.handle_no_image_hover()
        elif self.hover_image and not self.selected:
            self.image = self.hover_image
    
        return True
    
    def handle_not_hovering(self) -> None:
        if self.error:
            self.set_button_color(self.error_color)
        elif self.selected:
            self.image = self.selected_image
        else:
            self.set_button_color(self.default_color)
            self.image = self.default_image
    
    def handle_no_image_hover(self) -> None:
        if self.error:
            self.set_button_color(self.error_color)
        else:
            self.set_button_color(self.hover_color)

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Handles events for the button, such as mouse clicks.

        Parameters:
        - event (pg.event.Event): The pygame event to handle.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos) and self.action:
                self.action()

    def update(self, events) -> None:
        """
        Updates the button's appearance and checks for interaction based on the current mouse position.
        This method can handle a single event or a list of events.

        Parameters:
        - events: A single pygame event or a list of pygame events to handle.
        """
        self.check_hover()
        if self.check_hover():
            if isinstance(events, list):
                for event in events:
                    self.handle_event(event)
            else:
                self.handle_event(events)

    def set_button_color(self, color: tuple) -> None:
        """
        Sets the color of the button.

        Parameters:
        - color (tuple): The color to set the button to.
        """
        self.color = color
