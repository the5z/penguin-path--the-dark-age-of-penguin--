# enemy.py

import random
import pygame

from settings import HEIGHT
from perspective import get_perspective_position


class Arrow:
    def __init__(self, lane, start_depth):
        self.lane = lane
        self.depth = start_depth

        # Mũi tên bay từ xa về phía Piko
        self.speed = 0.025

        self.active = True
        self.hit_checked = False

    def update(self):
        self.depth -= self.speed

        if self.depth < -0.25:
            self.active = False

    def get_rect(self):
        visible_depth = max(-0.25, min(1.0, self.depth))
        x, y, scale = get_perspective_position(self.lane, visible_depth)

        if self.depth < 0:
            extra = min(abs(self.depth), 0.25)
            y += extra * 420
            scale *= 1 + extra * 1.5

        w = max(12, int(34 * scale))
        h = max(5, int(10 * scale))

        return pygame.Rect(
            int(x - w // 2),
            int(y - h // 2),
            w,
            h
        )

    def draw(self, screen):
        rect = self.get_rect()

        # Thân tên
        pygame.draw.rect(
            screen,
            (120, 70, 35),
            rect,
            border_radius=4
        )

        # Đầu tên
        pygame.draw.polygon(screen, (70, 70, 70), [
            (rect.right, rect.centery),
            (rect.right + max(6, rect.w // 3), rect.centery - rect.h),
            (rect.right + max(6, rect.w // 3), rect.centery + rect.h),
        ])


class HedgehogArcher:
    def __init__(self, lane):
        self.lane = lane
        self.depth = 1.0

        self.speed = 0.0035

        self.active = True
        self.health = 1

        self.shoot_timer = random.randint(50, 90)
        self.shoot_interval = 100

        self.base_w = 70
        self.base_h = 70

    def update(self):
        # Nhím tiến lại gần chậm hơn vật cản
        self.depth -= self.speed

        self.shoot_timer -= 1

        if self.depth < -0.2:
            self.active = False

    def should_shoot(self):
        # Chỉ bắn khi còn ở khoảng xa/trung bình
        if self.depth <= 0.15:
            return False

        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_interval
            return True

        return False

    def take_hit(self):
        self.health -= 1

        if self.health <= 0:
            self.active = False

    def get_rect(self):
        x, y, scale = get_perspective_position(self.lane, self.depth)

        w = max(12, int(self.base_w * scale))
        h = max(12, int(self.base_h * scale))

        return pygame.Rect(
            int(x - w // 2),
            int(y - h // 2),
            w,
            h
        )

    def draw(self, screen):
        rect = self.get_rect()

        # Placeholder nhím cầm cung
        # Thân nhím
        pygame.draw.ellipse(screen, (120, 80, 55), rect)

        # Gai nhím
        for i in range(5):
            spike_x = rect.left + i * rect.w // 4
            pygame.draw.polygon(screen, (80, 55, 40), [
                (spike_x, rect.top + rect.h // 3),
                (spike_x + rect.w // 8, rect.top - rect.h // 5),
                (spike_x + rect.w // 4, rect.top + rect.h // 3),
            ])

        # Mắt
        eye_size = max(2, rect.w // 12)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx - rect.w // 6, rect.centery - rect.h // 8), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (rect.centerx + rect.w // 6, rect.centery - rect.h // 8), eye_size)

        # Cung
        pygame.draw.arc(
            screen,
            (100, 50, 20),
            (rect.right - rect.w // 3, rect.top, rect.w // 2, rect.h),
            -1.3,
            1.3,
            max(2, rect.w // 16)
        )


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.arrows = []

        self.spawn_timer = 0
        self.spawn_interval = 240

    def spawn_hedgehog(self):
        lane = random.randint(0, 2)
        self.enemies.append(HedgehogArcher(lane))

    def update(self, obstacle_speed):
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_hedgehog()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()

            if enemy.should_shoot():
                self.arrows.append(Arrow(enemy.lane, enemy.depth))

        for arrow in self.arrows:
            arrow.update()

        self.enemies = [
            enemy for enemy in self.enemies
            if enemy.active
        ]

        self.arrows = [
            arrow for arrow in self.arrows
            if arrow.active
        ]

        # Xa vẽ trước, gần vẽ sau
        self.enemies.sort(key=lambda enemy: enemy.depth, reverse=True)
        self.arrows.sort(key=lambda arrow: arrow.depth, reverse=True)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

        for arrow in self.arrows:
            arrow.draw(screen)

    def check_bullet_hits(self, projectile_manager):
        for bullet in projectile_manager.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.lane == enemy.lane:
                    if abs(bullet.depth - enemy.depth) < 0.08:
                        enemy.take_hit()
                        bullet.active = False
                        break

    def check_arrow_hits_player(self, player):
        hit_count = 0

        for arrow in self.arrows:
            if arrow.depth <= 0.08 and not arrow.hit_checked:
                arrow.hit_checked = True

                if arrow.lane == player.current_lane:
                    hit_count += 1

        return hit_count

    def reset(self):
        self.enemies = []
        self.arrows = []
        self.spawn_timer = 0