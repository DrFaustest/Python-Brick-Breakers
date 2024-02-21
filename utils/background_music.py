from settings import SOUND_ENABLED_IMAGE, SOUND_DISABLED_IMAGE, VOLUME
import pygame as pg

class BackgroundMusic:
    def __init__(self) -> None:
        self.enabled: bool = True
        self.enabled_image: pg.Surface = pg.image.load(SOUND_ENABLED_IMAGE)
        self.enabled_image = pg.transform.scale(self.enabled_image, (50, 50))
        self.disabled_image: pg.Surface = pg.image.load(SOUND_DISABLED_IMAGE)
        self.disabled_image = pg.transform.scale(self.disabled_image, (50, 50))
        self.current_image = self.enabled_image
        self.playlist = ["sound/background_1.mp3", "sound/background_2.mp3", "sound/background_1.mid", "sound/background_2.mid"]
        self.current_track_index = 0
        pg.mixer.music.set_volume(VOLUME)
        pg.mixer.music.set_endevent(pg.USEREVENT)
        self.play()

    def change_music_state(self) -> None:
        if self.enabled:
            self.stop()
        else:
            self.play()

    def play(self) -> None:
        if not self.enabled:
            self.enabled = True
            self.current_image = self.enabled_image
        pg.mixer.music.load(self.playlist[self.current_track_index])
        pg.mixer.music.play(0)

    def play_next_track(self) -> None:
        if not self.enabled:
            return
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        pg.mixer.music.load(self.playlist[self.current_track_index])
        pg.mixer.music.play(0)

    def stop(self) -> None:
        pg.mixer.music.stop()
        self.enabled = False
        self.current_image = self.disabled_image
