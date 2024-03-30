

class GameState:
    """
    Represents the state of the game.

    Attributes:
        game (Game): The game object associated with this state.
    """

    def __init__(self, game):
        """
        Initializes a new instance of the GameState class.

        Args:
            game (Game): The game object associated with this state.
        """
        self.game = game

    def update(self, events):
        """
        Updates the state of the game.

        Args:
            events (list): A list of events that occurred since the last update.
        """
        raise NotImplementedError

    def draw(self, screen):
        """
        Draws the state of the game on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        raise NotImplementedError
