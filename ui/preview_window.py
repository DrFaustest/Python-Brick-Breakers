import pygame

class PreviewWindow:
    def __init__(self, screen, image_list, image_description, x, y, display_width, display_height):
        self.window = screen
        self.image_list = image_list
        self.image_description = image_description
        self.x = x
        self.y = y
        self.display_width = display_width
        self.display_height = display_height
        self.button_width = 50
        self.button_height = 50
        self.images = {}  # Cache for loaded images
        self.current_image = None
        self.index = 0
        self.unsaved_changes = False
        self.create_buttons()
        self.load_current_image()  # Load only the current image initially

    def load_current_image(self):
        # Load and scale the current image if it's not already in the cache
        img_path = self.image_list[self.index]
        if img_path not in self.images:
            image = pygame.image.load(img_path).convert_alpha()
            img_width, img_height = image.get_size()
            scale_factor = min((self.display_width - 2 * self.button_width) / img_width, self.display_height / img_height)
            new_size = (int(img_width * scale_factor), int(img_height * scale_factor))
            self.images[img_path] = pygame.transform.scale(image, new_size)
        self.current_image = self.images[img_path]

    def create_buttons(self):
        mid_y = self.y + (self.display_height - self.button_height) // 2
        self.left_button = pygame.Rect(self.x - self.button_width, mid_y, self.button_width, self.button_height)
        self.right_button = pygame.Rect(self.x + self.display_width, mid_y, self.button_width, self.button_height)

    def draw_buttons(self):
        pygame.draw.rect(self.window, (100, 100, 100), self.left_button)
        pygame.draw.rect(self.window, (100, 100, 100), self.right_button)
        font = pygame.font.Font(None, 40)
        left_arrow = font.render("<", True, (255, 255, 255))
        right_arrow = font.render(">", True, (255, 255, 255))
        left_arrow_pos = left_arrow.get_rect(center=self.left_button.center)
        right_arrow_pos = right_arrow.get_rect(center=self.right_button.center)
        self.window.blit(left_arrow, left_arrow_pos)
        self.window.blit(right_arrow, right_arrow_pos)

    def draw_image(self):
        if self.current_image:
            self.window.fill((0, 0, 0), (self.x, self.y, self.display_width, self.display_height))
            image_width, image_height = self.current_image.get_size()
            image_x = self.x + (self.display_width - image_width) // 2
            image_y = self.y + (self.display_height - image_height) // 2
            self.window.blit(self.current_image, (image_x, image_y))
            self.draw_text(self.image_description, (self.x + self.display_width // 2, self.y + self.display_height + 20))

    def draw_text(self, text, position, font_size=20, text_color=(255, 255, 255), background_color=None):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, text_color, background_color)
        text_rect = text_surface.get_rect(center=position)
        self.window.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_button.collidepoint(event.pos):
                self.index = (self.index - 1) % len(self.image_list)
                self.load_current_image()
                self.draw_image()
                self.unsaved_changes = True
            elif self.right_button.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.image_list)
                self.load_current_image()
                self.draw_image()
                self.unsaved_changes = True

    def get_value(self):
        return (self.image_description, self.image_list[self.index])

    def draw(self):
        self.draw_image()
        self.draw_buttons()
