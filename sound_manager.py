import os
import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.music_volume = 0.35
        self.sfx_volume = 0.7

        self.sounds = {}

        self.load_sound("hit", "assets/sounds/hit.wav")
        self.load_sound("shield_break", "assets/sounds/shield_break.wav")
        self.load_sound("shoot", "assets/sounds/shoot.wav")
        self.load_sound("win", "assets/sounds/win.wav")
        self.load_sound("lose", "assets/sounds/lose.wav")
        self.load_sound("intro", "assets/sounds/intro.wav")
        self.load_sound("not_enough_coin", "assets/sounds/not_enough_coin.wav")
        self.load_sound("boss_roar", "assets/sounds/boss_roar.wav")
        self.load_sound("coin", "assets/sounds/coin.wav")
    def load_sound(self, name, path):
        if not os.path.exists(path):
            print(f"Khong tim thay file am thanh: {path}")
            self.sounds[name] = None
            return

        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        self.sounds[name] = sound

    def play_music(self, path="assets/sounds/background_music.mp3"):
        if not os.path.exists(path):
            print(f"Khong tim thay nhac nen: {path}")
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play(self, name):
        sound = self.sounds.get(name)

        if sound is not None:
            sound.play()