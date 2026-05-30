# player.py

import os
import pygame
from settings import (
    LANES,
    HEIGHT,
    BLACK,
    WHITE,
    YELLOW,
    BLUE,
    PLAYER_W,
    PLAYER_H,
    PLAYER_BASE_Y,
    PLAYER_VISUAL_LANE_OFFSET_X,
    SHIELD_SIZE,
    SHIELD_OFFSET_X,
    SHIELD_OFFSET_Y,
)

def load_image(path, size=None):
    if not os.path.exists(path):
        print(f"Khong tim thay anh: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()

    if size is not None:
        size = (int(size[0]), int(size[1]))

        if size[0] <= 0 or size[1] <= 0:
            print(f"Size anh khong hop le: {path} - {size}")
            return image

        image = pygame.transform.smoothscale(image, size)

    return image

class Player:
    def __init__(self):
        self.width = PLAYER_W
        self.height = PLAYER_H

        self.celebrating = False
        self.celebrate_timer = 0
        self.celebrate_offset_y = 0
        self.celebrate_finished = False

        self.current_lane = 1
        self.visual_lane_offset_x = PLAYER_VISUAL_LANE_OFFSET_X
        self.x = LANES[self.current_lane] - self.width // 2 + self.visual_lane_offset_x

        self.base_y = PLAYER_BASE_Y
        self.camera_offset_y = 0
        self.y = self.base_y

        self.max_health = 5
        self.health = self.max_health
        self.max_energy = 50
        self.energy = self.max_energy
        # Ảnh nhân vật
        self.idle_image = load_image(
            "assets/characters/piko_idle.png",
            (PLAYER_W, PLAYER_H)
        )

        self.run_images = [
            load_image("assets/characters/piko_run_back_1.png", (PLAYER_W, PLAYER_H)),
            load_image("assets/characters/piko_run_back_2.png", (PLAYER_W, PLAYER_H)),
        ]
        self.celebrate_images = [
            load_image("assets/characters/celebrate/celebrate_1.png", (PLAYER_W, PLAYER_H)),
            load_image("assets/characters/celebrate/celebrate_2.png", (PLAYER_W, PLAYER_H)),
            load_image("assets/characters/celebrate/celebrate_3.png", (PLAYER_W, PLAYER_H)),
            load_image("assets/characters/celebrate/celebrate_4.png", (PLAYER_W, PLAYER_H)),
            load_image("assets/characters/celebrate/celebrate_5.png", (PLAYER_W, PLAYER_H)),
        ]

        self.celebrate_animation_timer = 0

        # 60 FPS / 5 frame mỗi giây = đổi ảnh mỗi 12 frame
        self.celebrate_animation_timer = 0
        self.celebrate_animation_speed = 12
        self.celebrate_animation_index = 0

        # Nhảy ăn mừng đúng 1 giây
        self.celebrate_jump_duration = 60
        self.celebrate_jump_height = 50
        


        self.shield_effect_image = load_image(
            "assets/effects/shield.png",
            (SHIELD_SIZE, SHIELD_SIZE)
        )

        # Animation chạy
        self.animation_timer = 0
        self.animation_speed = 12
        self.animation_index = 0

        # Khiên
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 120

        self.shield_cooldown = 0
        self.shield_cooldown_max = 180

    def move_left(self):
        self.current_lane = max(0, self.current_lane - 1)

    def move_right(self):
        self.current_lane = min(2, self.current_lane + 1)

    def activate_shield(self):
        shield_energy_cost = 5

        if self.shield_cooldown <= 0 and self.energy >= shield_energy_cost:
            self.energy -= shield_energy_cost

            self.shield_active = True
            self.shield_timer = self.shield_duration
            self.shield_cooldown = self.shield_cooldown_max

            return True

        return False

    def update_animation(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.run_images)

    def update(self):
        self.y = self.base_y - self.camera_offset_y
        target_x = LANES[self.current_lane] - self.width // 2 + self.visual_lane_offset_x
        self.x += (target_x - self.x) * 0.25

        self.update_animation()
        if self.celebrating:
            self.update_celebration()
            return
        if self.shield_active:
            self.shield_timer -= 1

            if self.shield_timer <= 0:
                self.shield_active = False

        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

    def absorb_hit(self):
        if self.shield_active:
            self.shield_active = False
            self.shield_timer = 0
            return True

        return False


    def take_hit(self):
        # Nếu đang có khiên: đỡ đúng 1 hit rồi mất khiên
        if self.shield_active:
            self.shield_active = False
            self.shield_timer = 0
            return False

        # Không có khiên thì mới mất máu
        self.health -= 1
        return True

    def is_dead(self):
        return self.health <= 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_center(self):
        return (
            int(self.x + self.width // 2),
            int(self.y + self.height // 2 + self.celebrate_offset_y)
    )

    def draw_placeholder(self, screen, x, y):
        pygame.draw.ellipse(screen, BLACK, (x, y, self.width, self.height))
        pygame.draw.ellipse(screen, WHITE, (x + 12, y + 18, 40, 45))

        pygame.draw.polygon(screen, YELLOW, [
            (x + 32, y + 25),
            (x + 22, y + 35),
            (x + 42, y + 35)
        ])

    def draw(self, screen):
        x = int(self.x)
        y = int(self.y + self.celebrate_offset_y)

        # Khiên hiệu ứng nằm sau nhân vật
        if self.shield_active and self.shield_effect_image is not None:
            shield_x = (
                x
                + self.width // 2
                - self.shield_effect_image.get_width() // 2
                + SHIELD_OFFSET_X
            )

            shield_y = (
                y
                + self.height // 2
                - self.shield_effect_image.get_height() // 2
                + SHIELD_OFFSET_Y
            )

            screen.blit(self.shield_effect_image, (shield_x, shield_y))

        if self.celebrating:
            image = self.celebrate_images[self.celebrate_animation_index]

            if image is not None:
                image_x = x + self.width // 2 - image.get_width() // 2
                image_y = y + self.height // 2 - image.get_height() // 2
                screen.blit(image, (image_x, image_y))
            elif self.idle_image is not None:
                image_x = x + self.width // 2 - self.idle_image.get_width() // 2
                image_y = y + self.height // 2 - self.idle_image.get_height() // 2
                screen.blit(self.idle_image, (image_x, image_y))
            else:
                self.draw_placeholder(screen, x, y)

            return
        
        # Dùng animation chạy
        image = self.run_images[self.animation_index]

        if image is not None:
            image_x = x + self.width // 2 - image.get_width() // 2
            image_y = y + self.height // 2 - image.get_height() // 2
            screen.blit(image, (image_x, image_y))
        elif self.idle_image is not None:
            image_x = x + self.width // 2 - self.idle_image.get_width() // 2
            image_y = y + self.height // 2 - self.idle_image.get_height() // 2
            screen.blit(self.idle_image, (image_x, image_y))
        else:
            self.draw_placeholder(screen, x, y)
    
    def start_celebration(self):
        self.celebrating = True
        self.celebrate_finished = False

        self.celebrate_timer = 0
        self.celebrate_offset_y = 0

        self.celebrate_animation_timer = 0
        self.celebrate_animation_index = 0

    def update_celebration(self):
        if not self.celebrating:
            return

        # Nếu đã nhảy xong thì giữ nguyên tư thế cuối, không nhảy nữa
        if self.celebrate_finished:
            self.celebrate_offset_y = 0
            self.celebrate_animation_index = len(self.celebrate_images) - 1
            return

        self.celebrate_timer += 1

        # Animation 5 frame/s
        self.celebrate_animation_timer += 1

        if self.celebrate_animation_timer >= self.celebrate_animation_speed:
            self.celebrate_animation_timer = 0
            self.celebrate_animation_index = min(
                self.celebrate_animation_index + 1,
                len(self.celebrate_images) - 1
            )

        # Nhảy đúng 1 giây: lên nửa giây, xuống nửa giây
        progress = self.celebrate_timer / self.celebrate_jump_duration

        if progress >= 1:
            self.celebrate_offset_y = 0
            self.celebrate_finished = True
            self.celebrate_animation_index = len(self.celebrate_images) - 1
            return

        # Công thức parabol: 0 -> cao nhất -> 0
        jump_curve = 4 * progress * (1 - progress)
        self.celebrate_offset_y = -int(self.celebrate_jump_height * jump_curve)
    def force_activate_shield(self):
        # Khiên cấp tốc: bật ngay, không phụ thuộc cooldown gốc
        self.shield_active = True
        self.shield_timer = self.shield_duration
    def add_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)