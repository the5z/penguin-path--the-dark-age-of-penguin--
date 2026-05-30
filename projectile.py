# projectile.py

import pygame

from perspective import get_perspective_position


class SnowBullet:
    def __init__(self, lane):
        self.lane = lane

        # Đạn bắt đầu gần Piko rồi bay ra xa
        self.depth = 0.05
        self.speed = 0.035

        self.active = True

    def update(self):
        # Bullet bay ra phía trước nên depth tăng dần
        self.depth += self.speed

        if self.depth >= 1.05:
            self.active = False

    def get_rect(self):
        x, y, scale = get_perspective_position(self.lane, self.depth)

        size = max(8, int(24 * scale))

        return pygame.Rect(
            int(x - size // 2),
            int(y - size // 2),
            size,
            size
        )

    def draw(self, screen):
        rect = self.get_rect()

        pygame.draw.circle(
            screen,
            (230, 250, 255),
            rect.center,
            rect.w // 2
        )

        pygame.draw.circle(
            screen,
            (80, 190, 255),
            rect.center,
            rect.w // 2,
            3
        )


class ProjectileManager:
    def __init__(self):
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 18

    def shoot(self, lane):
        if self.shoot_cooldown <= 0:
            self.bullets.append(SnowBullet(lane))
            self.shoot_cooldown = self.shoot_cooldown_max
            return True

        return False

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.active
        ]

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def reset(self):
        self.bullets = []
        self.shoot_cooldown = 0