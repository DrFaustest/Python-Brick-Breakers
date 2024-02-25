import pygame

class Slider:
    def __init__(self, x, y, screen_width, h, min_val, max_val, initial_val, description, font_size=20):
        """
        Initializes a Slider object.

        Args:
            x (int): The x-coordinate of the slider.
            y (int): The y-coordinate of the slider.
            screen_width (int): The width of the screen.
            h (int): The height of the slider.
            min_val (float): The minimum value of the slider.
            max_val (float): The maximum value of the slider.
            initial_val (float): The initial value of the slider.
            description (str): The description of the slider.
            font_size (int, optional): The font size of the description. Defaults to 20.
        """
        self.font = pygame.font.Font(None, font_size)
        self.description = description
        description_surf = self.font.render(description, True, (0, 0, 0))
        description_width = description_surf.get_width()

        # Adjust starting x position based on the description width
        adjusted_x = x + description_width + 10  # Add some padding after the description
        adjusted_width = screen_width - adjusted_x - 10  # Leave some space on the right as well

        self.rect = pygame.Rect(adjusted_x, y, adjusted_width, h)  # Adjusted slider rectangle
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val  # Current value
        self.grabbed = False  # Is the slider being dragged?
        # Calculate initial handle position
        self.handle_rect = pygame.Rect(adjusted_x, y - 10, 20, h + 20)  # Handle rectangle, slightly larger for easier grabbing
        self.update_handle_position()

    def draw(self, surface):
        """
        Draws the slider on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the slider on.
        """
        # Draw the description
        description_surf = self.font.render(self.description, True, (0, 0, 0))
        surface.blit(description_surf, (self.rect.x - description_surf.get_width() - 10, self.rect.y + self.rect.height / 2 - description_surf.get_height() / 2))

        # Draw the slider
        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.handle_rect)

        # Value display
        min_val_surf = self.font.render(str(self.min_val), True, (0, 0, 0))
        max_val_surf = self.font.render(str(self.max_val), True, (0, 0, 0))
        current_val_surf = self.font.render(str(int(self.val)), True, (0, 0, 0))

        surface.blit(min_val_surf, (self.rect.x - min_val_surf.get_width() / 2, self.rect.y + self.rect.height + 5))
        surface.blit(max_val_surf, (self.rect.x + self.rect.width - max_val_surf.get_width() / 2, self.rect.y + self.rect.height + 5))
        surface.blit(current_val_surf, (self.handle_rect.x + self.handle_rect.width / 2 - current_val_surf.get_width() / 2, self.handle_rect.y - current_val_surf.get_height() - 5))

    def handle_event(self, event):
        """
        Handles the given event.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        """
        Moves the handle of the slider based on the mouse position.

        Args:
            mouse_x (int): The x-coordinate of the mouse position.
        """
        # Move the handle within the slider bounds
        self.handle_rect.x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.handle_rect.width))
        self.val = self.min_val + ((self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)) * (self.max_val - self.min_val)
        self.update_handle_position()

    def update_handle_position(self):
        """
        Updates the position of the handle based on the current value.
        """
        self.handle_rect.x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * (self.rect.width - self.handle_rect.width)
