import pygame as pg

class LevelBanner:
    def __init__(self, font_size=50, color=(255, 255, 255)):
        """
        Initialize the LevelBanner object.

        Args:
            font_size (int): The font size for the level text. Default is 50.
            color (tuple): The color of the level text in RGB format. Default is (255, 255, 255).
        """
        self.font = pg.font.SysFont("Arial", font_size)
        self.color = color

    def display(self, screen, level_number, screen_width, screen_height):
        """
        Display the level banner on the screen.

        Args:
            screen (pygame.Surface): The surface to display the level banner on.
            level_number (int): The level number to be displayed.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        bg_color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])
        level_text = self.font.render(f"Level {level_number}", True, self.color, bg_color)
        text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(level_text, text_rect)
        pg.display.flip()
        pg.time.wait(2000)

    def display_ball_lost_message(self, screen, screen_width, screen_height):
        """
        Display the "YOU LOST A BALL!" message on the screen.
    
        Args:
            screen (pygame.Surface): The surface to display the message on.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        bg_color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])
        message_text = self.font.render("YOU LOST A BALL!", True, (255, 0, 0), bg_color)
        text_rect = message_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(message_text, text_rect)
        pg.display.flip()
        pg.time.wait(2000)