import pygame

class TextBox:
    def __init__(self, x, y, width, height, callback_function, prompt=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = (255, 0, 0)  # Red (active color for text and border)
        self.color_inactive = (255, 255, 255)  # White (inactive color for text and border)
        self.background_color = (0, 0, 0)  # Black background
        self.text_color = (255, 255, 255)  # White text
        self.text = ""
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.callback_function = callback_function
        self.prompt = prompt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.callback_function(self.text)
                    self.text = ''
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        # Draw prompt
        prompt_surface = self.font.render(self.prompt, True, self.text_color)
        screen.blit(prompt_surface, (self.rect.x, self.rect.y - 30))  # Adjust as necessary for prompt placement
        
        # Draw text box background
        screen.fill(self.background_color, self.rect)
        
        # Draw text
        txt_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        
        # Draw border with active/inactive color
        border_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, border_color, self.rect, 2)  # 2 pixels for the border thickness
