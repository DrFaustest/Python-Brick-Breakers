import json
import os
from typing import Dict, List, Union

class Settings:
    """
    A class that manages the game settings.
    """

    _instance = None # Singleton instance of the Settings class
    defaults: Dict[str, Union[int, str, List[str], List[int]]] = {
        "SCALE": 1,
        "SCREEN_WIDTH": 800,
        "SCREEN_HEIGHT": 600,
        "BRICK_SIZE": [100, 20],
        "BACKGROUND_IMAGES": [
            "img/background.webp",
            "img/background_2.webp",
            "img/background_3.webp",
            "img/background_4.webp"
        ],
        "MUSIC_PLAYLIST": [
            "sound\\background_1.mp3",
            "sound\\background_2.mp3",
            "sound\\background_1.mid",
            "sound\\background_2.mid"
        ],
        "BRICK_IMAGES": [
            "img/brick_img.png",
            "img/brick_img1.png"
        ],
        "BALL_IMAGES": [
            "img/future_ball.png",
            "img/retro_snow_ball.png",
            "img/ring_ball.png"
        ],
        "PADDLE_IMAGES": ["img/paddle.png"],
        "PLAYER_SCORE": 0,
        "FPS": 240,
        "PADDLE_SPEED": 25,
        "PADDLE_SIZE": [100, 20],
        "BALL_SPEED": 2,
        "DIFFICULTY": 1,
        "VOLUME": 0.5,
        "WHITE": [255, 255, 255],
        "GRAY": [128, 128, 128],
        "RED": [255, 0, 0],
        "GREEN": [0, 255, 0],
        "BLUE": [0, 0, 255],
        "BLACK": [0, 0, 0],
        "MAX_REFLECTION_ANGLE": 90,
        "MIN_Y_VELOCITY": -1.5,
        "BALL_RADIUS": 15,
        "BALL_IMG": "img/future_ball.png",
        "PADDLE_IMG": "img/paddle.png",
        "BRICK_IMG": "img/brick_img.png",
        "BACKGROUND_IMG": "img/background.webp",
        "SOUND_ENABLED_IMAGE": "img/sound_image.png",
        "SOUND_DISABLED_IMAGE": "img/sound_muted.png",
        "PLAY_BUTTON_IMG": "img/StartButton.png",
        "SETTINGS_BUTTON_IMG": "img/SettingsButton.png",
        "HIGH_SCORES_BUTTON_IMG": "img/LeaderboardButton.png"
    }

    def __new__(cls, filename: str = "settings.json") -> "Settings":
        """
        Create a new instance of the Settings class.

        Args:
            filename (str): The name of the settings file.

        Returns:
            Settings: The Settings instance.
        """
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.filename = filename
            cls._instance.settings = cls._instance.load()
            cls._instance.populate_image_lists()
        return cls._instance

    def load(self) -> Dict[str, Union[int, str, List[str], List[int]]]:
        """
        Load the settings from the settings file.

        Returns:
            dict: The loaded settings.
        """
        try:
            with open(self.filename, "r") as file:
                loaded_settings = json.load(file)
                for key, value in self.defaults.items():
                    if key not in loaded_settings:
                        loaded_settings[key] = value
                return loaded_settings
        except FileNotFoundError:
            return self.defaults

    def save(self) -> None:
        """
        Save the settings to the settings file.
        """
        with open(self.filename, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key: str) -> Union[int, str, List[str], List[int]]:
        """
        Get the value of a specific setting.

        Args:
            key (str): The key of the setting.

        Returns:
            Union[int, str, List[str], List[int]]: The value of the setting.
        """
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key: str, value: Union[int, str, List[str], List[int]]) -> None:
        """
        Set the value of a specific setting.

        Args:
            key (str): The key of the setting.
            value (Union[int, str, List[str], List[int]]): The value to set.
        """
        self.settings[key] = value
        self.save()
        self.settings = self.load()

    def populate_image_lists(self) -> Dict[str, Union[int, str, List[str], List[int]]]:
        """
        Populate the image lists with the files in the 'img' directory.

        Returns:
            dict: The updated settings.
        """
        self.settings["BALL_IMAGES"] = []
        self.settings["PADDLE_IMAGES"] = []
        self.settings["BACKGROUND_IMAGES"] = []
        self.settings["BRICK_IMAGES"] = []
        for root, dirs, files in os.walk("img"):
            for file in files:
                if "ball" in root:
                    self.settings["BALL_IMAGES"].append(os.path.join(root, file))
                elif "paddle" in root:
                    self.settings["PADDLE_IMAGES"].append(os.path.join(root, file))
                elif "background" in root:
                    self.settings["BACKGROUND_IMAGES"].append(os.path.join(root, file))
                elif "brick" in root:
                    self.settings["BRICK_IMAGES"].append(os.path.join(root, file))
        self.save()
        return self.settings