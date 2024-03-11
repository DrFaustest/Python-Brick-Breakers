import pygame

class Slider:
    def __init__(self, screen, x, y, width, height, min_value, max_value, current_value, description=""):
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
    
        # Slider track dimensions
        self.track_rect = pygame.Rect(x, y, width, height // 2)
        # Slider handle dimensions
        self.handle_rect = pygame.Rect(x, y, self.get_handle_width(), height // 2)
        # Slider hitbox dimensions
        self.hitbox = pygame.Rect(x, y, width, height)

        self.grabbed = False  # Initialize the grabbed attribute
        self.update_handle_position()

    def get_handle_width(self):
        # Calculate the width of the handle to fill the track proportionally to the value range
        range_width_ratio = 20 / (self.max_value - self.min_value)
        return max(self.width * range_width_ratio, 20)

    def update_handle_position(self):
        # Calculate the handle's position along the track based on the current value
        value_ratio = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        handle_x_position = self.x + (self.width - self.get_handle_width()) * value_ratio
        self.handle_rect.x = handle_x_position

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hitbox.collidepoint(event.pos):  # Use hitbox for initial click detection
                self.grabbed = True
                self.unsaved_changes = True
                # Optionally, you can add logic to detect if the click is on the handle specifically
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            # For movement, consider limiting the interaction to when the mouse is over the track or handle
            self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        # Update the handle position and value based on mouse position
        if self.x <= mouse_x <= self.x + self.width:
            self.handle_rect.x = max(self.x, min(mouse_x, self.x + self.width - self.handle_rect.width))
            value_range = (self.handle_rect.x - self.x) / (self.width - self.handle_rect.width)
            self.current_value = self.min_value + value_range * (self.max_value - self.min_value)

    def draw(self):
        # Draw the container with a white background
        container_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_color, container_rect)

        # Draw the slider track
        pygame.draw.rect(self.screen, self.track_color, self.track_rect)

        # Draw the slider handle with a black border
        pygame.draw.rect(self.screen, self.handle_color, self.handle_rect)
        pygame.draw.rect(self.screen, self.border_color, self.handle_rect, 1)  # 1 is the thickness of the border

        # Render the current value inside the slider handle
        val_text = self.font.render(str(int(self.current_value)), True, self.border_color)
        val_text_rect = val_text.get_rect(center=self.handle_rect.center)
        self.screen.blit(val_text, val_text_rect)

        # Draw the description and min/max values
        desc_text = self.font.render(self.description, True, self.border_color)
        min_val_text = self.font.render(str(self.min_value), True, self.border_color)
        max_val_text = self.font.render(str(self.max_value), True, self.border_color)

        # Position the texts in the lower half of the height
        base_y = self.y + self.height // 2
        self.screen.blit(min_val_text, (self.x, base_y))
        self.screen.blit(desc_text, (self.x + self.width // 2 - desc_text.get_width() // 2, base_y))
        self.screen.blit(max_val_text, (self.x + self.width - max_val_text.get_width(), base_y))

    def get_value(self):
        return (self.description, self.current_value)

    def update(self, new_value):
        # Update the current value and handle position
        self.current_value = new_value
        self.update_handle_position()
