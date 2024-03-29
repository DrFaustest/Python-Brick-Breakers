import pygame as pg

class Button:
    def __init__(self, screen,x: int, y: int, width: int = None, height: int = None, text: str = "change me", color: tuple = (255, 255, 255), hover_color: tuple = (128, 128, 128), text_color: tuple = (0, 0, 0), action: callable = None, image: pg.Surface = None) -> None:
        """
        Initializes a Button object.

        Parameters:
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
        """
        self.image = image
        self.screen = screen
        if self.image is not None:
            # If an image is provided and no width/height are specified, use the image's dimensions
            if width is None or height is None:
                width, height = self.image.get_size()
        else:
            # Default to provided dimensions or a standard size if none are specified
            width = width if width is not None else 200
            height = height if height is not None else 100
        
        self.x = x
        self.y = y
        self.error = False
        self.error_color = (255, 0, 0)
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.hitbox = self.rect
        self.font = pg.font.SysFont("Arial", 50)

    def draw(self):
        """
        Draws the button on the screen.

        Parameters:
        - screen: The pygame screen to draw the button on.
        """
        # Draw the button image if provided, otherwise draw a rectangle
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pg.draw.rect(self.screen, self.color, self.rect)
        # Draw text in the center of the button/image
        if self.text:
            text_str = str(self.text)
            text_color = self.text_color if isinstance(self.text_color, tuple) and len(self.text_color) in [3, 4] else (0, 0, 0)
            text_surface = self.font.render(text_str, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.screen.blit(text_surface, text_rect)

    def check_hover(self):
        """
        Checks if the button is being hovered over and changes its appearance accordingly.

        Returns:
            bool: True if the mouse is hovering over the button, False otherwise.
        """
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):  # Check if mouse is over the button
            if not self.image:  # Change color if no image is used
                #check for the error flag and change the color to error color reguardless of the hover color
                if self.error:
                    self.color = self.error_color
                else:
                    self.color = self.hover_color
            return True
        else: # Reset color if not hovered over
            if self.error:
                self.color = self.error_color
            else:
                self.color = self.color
        return False

    def handle_event(self, event):
        """
        Handles events for the button, such as mouse clicks.

        Parameters:
        - event: The pygame event to handle.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos) and self.action:
                self.action()

    def update(self, events):
        """
        Updates the button's appearance and checks for interaction based on the current mouse position.
        This method can handle a single event or a list of events.

        Parameters:
        - events: A single pygame event or a list of pygame events to handle.
        """
        if self.check_hover():
            if isinstance(events, list):
                # If events is a list, iterate over each event
                for event in events:
                    self.handle_event(event)
            else:
                # If events is a single event, just handle that event
                self.handle_event(events)
