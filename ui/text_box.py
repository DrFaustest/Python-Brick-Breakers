import pygame

class TextBox:
    def __init__(self, x, y, width, height, callback_function, prompt=''):
        """
        Initializes a TextBox object.

        Args:
            x (int): The x-coordinate of the top-left corner of the text box.
            y (int): The y-coordinate of the top-left corner of the text box.
            width (int): The width of the text box.
            height (int): The height of the text box.
            callback_function (function): The function to be called when the user presses Enter.
            prompt (str, optional): The prompt text to be displayed above the text box. Defaults to an empty string.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = (255, 0, 0)
        self.color_inactive = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.text = ""
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.callback_function = callback_function
        self.prompt = prompt

    def handle_event(self, event):
        """
        Handles the given event.

        Args:
            event (pygame.event.Event): The event to be handled.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if callable(self.callback_function):
                        self.callback_function()
                    self.text = ''
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        """
        Updates the state of the text box.
        """
        pass

    def draw(self, screen):
        """
        Draws the text box on the given screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        prompt_surface = self.font.render(self.prompt, True, self.text_color)
        screen.blit(prompt_surface, (self.rect.x, self.rect.y - 30))
        
        screen.fill(self.background_color, self.rect)

        txt_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))

        border_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, border_color, self.rect, 2)