from settings import *
import pygame as pg

class BackgroundMusic:
    def __init__(self) -> None:
        self.enabled: bool = True
        self.enabled_image: pg.Surface = pg.image.load(SOUND_ENABLED_IMAGE)
        self.enabled_image = pg.transform.scale(self.enabled_image, (50, 50))
        self.disabled_image: pg.Surface = pg.image.load(SOUND_DISABLED_IMAGE)
        self.disabled_image = pg.transform.scale(self.disabled_image, (50, 50))
        # Load the initial music track
        pg.mixer.music.load("sound/background_1.mp3")
        pg.mixer.music.set_volume(VOLUME)
        self.current_image: pg.Surface = self.enabled_image
        self.play()

    def change_music_state(self) -> None:
        if self.enabled:
            self.stop()
        else:
            self.play()

    def play(self) -> None:
        pg.mixer.music.play(-1)  # Play indefinitely
        self.enabled = True
        self.current_image = self.enabled_image

    def stop(self) -> None:
        pg.mixer.music.stop()
        self.enabled = False
        self.current_image = self.disabled_image
