import json
import os

class Settings:
    _instance = None
    defaults = {
    "SCALE": 1,
    "SCREEN_WIDTH": 800,
    "SCREEN_HEIGHT": 600,
    "BRICK_SIZE": [100, 20],
    "BACKGROUND_IMAGES": ["img/background.webp", "img/background_2.webp", "img/background_3.webp", "img/background_4.webp"],
    "BRICK_IMAGES": ["img/brick_img.png", "img/brick_img1.png"],
    "BALL_IMAGES": ["img/future_ball.png", "img/retro_snow_ball.png", "img/ring_ball.png"],
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

    def __new__(cls, filename="settings.json"):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.filename = filename
            cls._instance.settings = cls._instance.load()
            cls._instance.populate_image_lists()
        return cls._instance

    def load(self):
        try:
            with open(self.filename, "r") as file:
                loaded_settings = json.load(file)
                for key, value in self.defaults.items():
                    if key not in loaded_settings:
                        loaded_settings[key] = value
                return loaded_settings
        except FileNotFoundError:
            return self.defaults

    def save(self):
        with open(self.filename, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()
        self.settings = self.load()

    def populate_image_lists(self):
        self.settings["BALL_IMAGES"] = []
        self.settings["PADDLE_IMAGES"] = []
        self.settings["BACKGROUND_IMAGES"] = []
        self.settings["BRICK_IMAGES"] = []
        for root, dirs, files in os.walk("img"):
            for file in files:
                if "ball" in root :
                    self.settings["BALL_IMAGES"].append(os.path.join(root, file))
                elif "paddle" in root:
                    self.settings["PADDLE_IMAGES"].append(os.path.join(root, file))
                elif "background" in root:
                    self.settings["BACKGROUND_IMAGES"].append(os.path.join(root, file))
                elif "brick" in root:
                    self.settings["BRICK_IMAGES"].append(os.path.join(root, file))
        self.save()
        return self.settings