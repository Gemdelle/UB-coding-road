import os

import pygame


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.mixer.init()
            cls._instance.sounds = {}
        return cls._instance

    def load_sound(self, name, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        self.sounds[name] = pygame.mixer.Sound(file_path)

    def play_sound(self, name, loops=0):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        self.sounds[name].play(loops=loops)

    def stop_sound(self, name):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        self.sounds[name].stop()

    def stop_all_sounds(self):
        for sound in self.sounds.values():
            sound.stop()

    def set_volume(self, name, volume):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        self.sounds[name].set_volume(volume)

    def get_volume(self, name):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        return self.sounds[name].get_volume()

    def fadeout(self, name, time):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        self.sounds[name].fadeout(time)

    def is_playing(self, name):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        return self.sounds[name].get_busy()