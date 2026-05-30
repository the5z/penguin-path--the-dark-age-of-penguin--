import os
import pygame


def load_image(path, size=None):
    if not os.path.exists(path):
        print(f"Khong tim thay anh hieu ung: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()

    if size is not None:
        image = pygame.transform.scale(image, size)

    return image


class ImageEffect:
    def __init__(self, x, y, image, duration=20, start_size=70, end_size=120):
        self.x = x
        self.y = y
        self.image = image

        self.timer = 0
        self.duration = duration
        self.active = True

        self.start_size = start_size
        self.end_size = end_size

    def update(self):
        self.timer += 1

        if self.timer >= self.duration:
            self.active = False

    def draw(self, screen):
        if self.image is None:
            return

        progress = self.timer / self.duration

        current_size = int(
            self.start_size + (self.end_size - self.start_size) * progress
        )

        alpha = int(255 * (1 - progress))

        effect_image = pygame.transform.smoothscale(
            self.image,
            (current_size, current_size)
        )

        effect_image.set_alpha(alpha)

        rect = effect_image.get_rect(center=(self.x, self.y))
        screen.blit(effect_image, rect)


class EffectManager:
    def __init__(self):
        self.effects = []

        self.hit_image = load_image("assets/effects/hit_effect.png")
        self.shield_break_image = load_image("assets/effects/shield_break_effect.png")

    def spawn_damage_hit(self, position):
        x, y = position

        self.effects.append(
            ImageEffect(
                x,
                y,
                self.hit_image,
                duration=18,
                start_size=60,
                end_size=110
            )
        )

    def spawn_shield_break(self, position):
        x, y = position

        image = self.shield_break_image

        if image is None:
            image = self.hit_image

        self.effects.append(
            ImageEffect(
                x,
                y,
                image,
                duration=22,
                start_size=80,
                end_size=140
            )
        )

    def update(self):
        for effect in self.effects:
            effect.update()

        self.effects = [
            effect for effect in self.effects
            if effect.active
        ]

    def draw(self, screen):
        for effect in self.effects:
            effect.draw(screen)

    def reset(self):
        self.effects = []