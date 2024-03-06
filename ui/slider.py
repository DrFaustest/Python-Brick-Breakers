import pygame

class Slider:
    def __init__(self, x, y, screen_width, h, min_val, max_val, initial_val, description=None):
        self.font = pygame.font.Font(None, 20)
        self.description = description if description else ""
        self.x, self.y, self.h = x, y, h

        description_surf = self.font.render(self.description, True, (0, 0, 0)) if self.description else None
        description_width = description_surf.get_width() if description_surf else 0

        adjusted_x = x + description_width + 10
        adjusted_width = screen_width - adjusted_x - 10

        self.rect = pygame.Rect(adjusted_x, y, adjusted_width, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.grabbed = False
        self.handle_rect = pygame.Rect(adjusted_x, y - 10, 20, h + 20)
        self.update_handle_position()

    def update_handle_position(self):
        # Update the handle position based on the current value
        handle_pos = (self.val - self.min_val) / (self.max_val - self.min_val) * (self.rect.width - self.handle_rect.width)
        self.handle_rect.x = self.rect.x + handle_pos

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            self.move_handle(event.pos[0])

    def move_handle(self, mouse_x):
        if self.rect.x <= mouse_x <= self.rect.x + self.rect.width:
            self.handle_rect.x = max(self.rect.x, min(mouse_x, self.rect.right - self.handle_rect.width))
            self.val = self.min_val + (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width) * (self.max_val - self.min_val)

    def draw(self, surface):
        if self.description:
            description_surf = self.font.render(self.description, True, (0, 0, 0))
            surface.blit(description_surf, (self.x, self.y + self.h / 2 - description_surf.get_height() / 2))

        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.handle_rect)

        min_val_surf = self.font.render(str(self.min_val), True, (0, 0, 0))
        max_val_surf = self.font.render(str(self.max_val), True, (0, 0, 0))
        current_val_surf = self.font.render(str(int(self.val)), True, (0, 0, 0))

        surface.blit(min_val_surf, (self.rect.x - min_val_surf.get_width() / 2, self.rect.y + self.rect.height + 5))
        surface.blit(max_val_surf, (self.rect.x + self.rect.width - max_val_surf.get_width() / 2, self.rect.y + self.rect.height + 5))
        surface.blit(current_val_surf, (self.handle_rect.x + self.handle_rect.width / 2 - current_val_surf.get_width() / 2, self.handle_rect.y - current_val_surf.get_height() - 5))

    def get_value(self):
        return self.val