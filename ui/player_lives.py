import pygame as pg
from settings import Settings

class PlayerLives:
    def __init__(self):
        """
        Initializes the PlayerLives object.

        Attributes:
        - lives (int): The number of lives the player has.
        - x (int): The x-coordinate of the player lives display.
        - y (int): The y-coordinate of the player lives display.
        - ball_image (Surface): The image of the ball representing a life.
        """
        self.settings = Settings()
        self.SCREEN_HEIGHT = self.settings.get("SCREEN_HEIGHT")
        self.BALL_IMG = self.settings.get("BALL_IMG")
        self.lives = 3
        self.x = 10
        self.y = self.SCREEN_HEIGHT - 40  # Adjusted for better visibility
        
        # Load and scale the ball image
        self.ball_image = pg.image.load(self.BALL_IMG).convert_alpha()  # Assuming BALL_IMG_PATH is defined in settings
        self.ball_image = pg.transform.scale(self.ball_image, (20, 20))  # Scale the image to 20x20 pixels

    def decrease_lives(self):
        """
        Decreases the number of lives by 1.
        """
        self.lives -= 1

    def update(self):
        """
        Updates the player lives display.
        This method can be used to update any other information on the scoreboard if needed.
        """
        pass

    def draw(self, screen):
        """
        Draws the player lives display on the screen.

        Parameters:
        - screen (Surface): The surface to draw on.
        """
        # Draw an oval-shaped box with a white border and black fill
        rect_width = self.lives * 25 + 10  # Adjust based on the size of the ball image and desired spacing
        pg.draw.ellipse(screen, (0, 0, 0), (self.x, self.y, rect_width, 30), 0)  # Black fill
        pg.draw.ellipse(screen, (255, 255, 255), (self.x, self.y, rect_width, 30), 2)  # White border
        
        # Display ball images for the number of lives remaining
        for i in range(self.lives):
            ball_x = self.x + 10 + i * 25  # Adjust spacing based on the size of the ball image
            ball_y = self.y + 5  # A little padding from the top of the oval
            screen.blit(self.ball_image, (ball_x, ball_y))

