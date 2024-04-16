import os

import pygame


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            pygame.mixer.init()
            cls._instance.sounds = {}
            cls._instance.channel_assignments = {}
        return cls._instance

    def load_sound(self, name, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        self.sounds[name] = pygame.mixer.Sound(file_path)

    def play_sound(self, name, loops=0):
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' not loaded.")
        channel = pygame.mixer.find_channel()
        self.channel_assignments[name] = channel
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
        return name in self.channel_assignments and self.channel_assignments[name].get_busy()


def play_button_sound():
    sound_manager = SoundManager()
    sound_manager.set_volume("button", 0.3)
    sound_manager.play_sound("button")
def play_correct_sound():
    sound_manager = SoundManager()
    sound_manager.set_volume("correct", 0.3)
    sound_manager.play_sound("correct")

def play_wrong_sound():
    sound_manager = SoundManager()
    sound_manager.set_volume("wrong", 0.3)
    sound_manager.play_sound("wrong")

def play_background_music():
    sound_manager = SoundManager()
    if not sound_manager.is_playing("background_music"):
        sound_manager.set_volume("background_music", 0.2)
        sound_manager.play_sound("background_music")