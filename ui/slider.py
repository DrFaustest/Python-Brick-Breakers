import pygame

class Slider:
    def __init__(self, screen, x, y, width, height, min_value, max_value, current_value, description=""):
        """
        Initialize a Slider object.

        Args:
            screen (pygame.Surface): The surface to draw the slider on.
            x (int): The x-coordinate of the top-left corner of the slider.
            y (int): The y-coordinate of the top-left corner of the slider.
            width (int): The width of the slider.
            height (int): The height of the slider.
            min_value (float): The minimum value of the slider.
            max_value (float): The maximum value of the slider.
            current_value (float): The current value of the slider.
            description (str, optional): The description of the slider. Defaults to "".
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value
        self.description = description
        self.unsaved_changes = False
        self.font = pygame.font.Font(None, 20)
        self.bg_color = (255, 255, 255)
        self.track_color = (180, 180, 180)
        self.handle_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.track_rect = pygame.Rect(x, y, width, height // 2)
        self.handle_rect = pygame.Rect(x, y, self.get_handle_width(), height // 2)
        self.hitbox = pygame.Rect(x, y, width, height)
        self.grabbed = False
        self.update_handle_position()

    def get_handle_width(self):
        """
        Calculate the width of the slider handle based on the range of values.

        Returns:
            int: The width of the slider handle.
        """
        range_width_ratio = 20 / (self.max_value - self.min_value)
        return max(self.width * range_width_ratio, 20)

    def update_handle_position(self):
        """
        Update the position of the slider handle based on the current value.
        """
        value_ratio = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        handle_x_position = self.x + (self.width - self.get_handle_width()) * value_ratio
        self.handle_rect.x = handle_x_position

    def handle_event(self, event):
        """
        Handle events related to the slider.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hitbox.collidepoint(event.pos):
                self.grabbed = True
                self.unsaved_changes = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        """
        Move the slider handle based on the mouse position.

        Args:
            mouse_x (int): The x-coordinate of the mouse position.
        """
        if self.x <= mouse_x <= self.x + self.width:
            self.handle_rect.x = max(self.x, min(mouse_x, self.x + self.width - self.handle_rect.width))
            value_range = (self.handle_rect.x - self.x) / (self.width - self.handle_rect.width)
            self.current_value = self.min_value + value_range * (self.max_value - self.min_value)

    def draw(self):
        """
        Draw the slider on the screen.
        """
        container_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, container_rect)
        pygame.draw.rect(self.screen, self.track_color, self.track_rect)
        pygame.draw.rect(self.screen, self.handle_color, self.handle_rect)
        pygame.draw.rect(self.screen, self.border_color, self.handle_rect, 1)
        val_text = self.font.render(str(int(self.current_value)), True, self.border_color)
        val_text_rect = val_text.get_rect(center=self.handle_rect.center)
        self.screen.blit(val_text, val_text_rect)

        desc_text = self.font.render(self.description, True, self.border_color)
        min_val_text = self.font.render(str(self.min_value), True, self.border_color)
        max_val_text = self.font.render(str(self.max_value), True, self.border_color)

        base_y = self.y + self.height // 2
        self.screen.blit(min_val_text, (self.x, base_y))
        self.screen.blit(desc_text, (self.x + self.width // 2 - desc_text.get_width() // 2, base_y))
        self.screen.blit(max_val_text, (self.x + self.width - max_val_text.get_width(), base_y))

    def get_value(self):
        """
        Get the current value of the slider.

        Returns:
            tuple: A tuple containing the description and current value of the slider.
        """
        return (self.description, self.current_value)

    def update(self, new_value):
        """
        Update the current value of the slider.

        Args:
            new_value (float): The new value of the slider.
        """
        self.current_value = new_value
        self.update_handle_position()