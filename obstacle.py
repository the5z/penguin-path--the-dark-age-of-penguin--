# obstacle.py

import os
import random
import pygame

from settings import RED, HEIGHT
from perspective import get_perspective_position
from settings import SNOW_WALL_W, SNOW_WALL_H, SNOW_WALL_ANIMATION_SPEED

def load_image(path):
    if not os.path.exists(path):
        print(f"Khong tim thay anh: {path}")
        return None
    return pygame.image.load(path).convert_alpha()


class Obstacle:
    normal_image = None
    wall_image = None
    damaged_image_1 = None
    damaged_image_2 = None
    broken_image = None
    wall_frames = []
    
    @classmethod
    def load_assets(cls):
        cls.normal_image = load_image("assets/obstacles/ice_block.png")
        cls.wall_image = load_image("assets/obstacles/snow_wall.png")
        cls.damaged_image_1 = load_image("assets/obstacles/ice_block_damaged_1.png")
        cls.damaged_image_2 = load_image("assets/obstacles/ice_block_damaged_2.png")
        cls.broken_image = load_image("assets/obstacles/ice_block_broken.png")
        cls.wall_frames = []

        cls.wall_frames = []

        for i in range(1, 6):
            image = load_image(f"assets/obstacles/snow_wall_{i}.png")

            if image is not None:
                cls.wall_frames.append(image)
    
    def __init__(self, lane, obstacle_type="normal"):
        self.lane = lane
        self.type = obstacle_type

        self.depth = 1.0
        self.hit_checked = False
        self.hit_player = False

        # Khối băng thường chịu được 3 viên
        self.max_health = 3 if self.type == "normal" else 999
        self.health = self.max_health

        # Trúng đủ 3 viên thì đi xuyên được
        self.passable = False

        self.base_w = 110
        self.base_h = 110

        if self.type == "wall":
            self.lane = 1
            self.base_w = SNOW_WALL_W
            self.base_h = SNOW_WALL_H
        self.animation_timer = 0
        self.animation_index = 0
    def update(self, speed):
        self.depth -= speed
        if self.type == "wall":
            self.animation_timer += 1

            if self.animation_timer >= SNOW_WALL_ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % 5
    def is_out_of_screen(self):
        if self.type == "wall":
            return self.depth < -0.15

        return self.depth < -0.35

    def get_draw_rect(self):
        visible_depth = max(-0.35, min(1.0, self.depth))
        x, y, scale = get_perspective_position(self.lane, visible_depth)

        # Khi vật cản đã vượt qua Piko (depth < 0), vẫn cho nó tiếp tục lớn thêm chút
        if self.depth < 0:
            extra = min(abs(self.depth), 0.35)
            scale *= (1 + extra * 1.8)
            y += extra * 450

        w = max(45, int(self.base_w * scale))
        h = max(45, int(self.base_h * scale))

        return pygame.Rect(
            int(x - w // 2),
            int(y - h // 2),
            w,
            h
        )

    def draw_placeholder(self, screen):
        rect = self.get_draw_rect()

        if self.type == "wall":
            color = (120, 170, 255)
        else:
            color = RED

        pygame.draw.rect(screen, color, rect, border_radius=12)

    def draw(self, screen):
        rect = self.get_draw_rect()

        if self.type == "wall":
            if Obstacle.wall_frames:
                image = Obstacle.wall_frames[self.animation_index]
            else:
                image = Obstacle.wall_image

        else:
            if self.health > self.max_health * 2 // 3:
                image = Obstacle.normal_image

            elif self.health > self.max_health // 3:
                image = Obstacle.damaged_image_1

            elif self.health > 0:
                image = Obstacle.damaged_image_2

            else:
                image = Obstacle.broken_image

        if image is not None:
            scaled_image = pygame.transform.smoothscale(image, (rect.w, rect.h))
            screen.blit(scaled_image, rect)
        else:
            self.draw_placeholder(screen)

    def take_bullet_hit(self):
        # Không cho bắn bão tuyết / snow wall
        if self.type == "wall":
            return False

        if self.passable:
            return False

        self.health -= 1

        if self.health <= 0:
            self.passable = True
            self.hit_checked = True

        return True
class ObstacleManager:
    def __init__(self, level=1):
        Obstacle.load_assets()

        self.level = level
        self.obstacles = []

        self.spawn_timer = 0
        self.spawn_interval = 85

        self.wall_timer = 0

        # Màn 1 bão tuyết đến sớm hơn, màn 2 ít hơn
        if self.level == 1:
            self.wall_interval = 520
        else:
            self.wall_interval = 900

        self.show_wall_warning = False

        # Cảnh báo chỉ dùng cho màn 1
        self.wall_warning_enabled = self.level == 1
        self.wall_warning_triggered = False
        self.wall_warning_timer = 0
        self.wall_warning_duration = 120

        # tốc độ theo chiều sâu
        self.depth_speed = 0.0065

    def spawn_obstacle(self):
        lane = random.randint(0, 2)
        self.obstacles.append(Obstacle(lane, "normal"))

    def spawn_double_obstacle(self):
        lanes = [0, 1, 2]
        safe_lane = random.choice(lanes)

        for lane in lanes:
            if lane != safe_lane:
                self.obstacles.append(Obstacle(lane, "normal"))

    def spawn_wall_obstacle(self):
        self.obstacles.append(Obstacle(1, "wall"))

    def update(self, speed, distance, current_level=1):
        self.spawn_timer += 1
        self.wall_timer += 1

        # =====================
        # CẢNH BÁO BÃO TUYẾT
        # Chỉ hiện ở màn 1, đúng lần đầu
        # =====================
        if self.wall_warning_timer > 0:
            self.wall_warning_timer -= 1
            self.show_wall_warning = True
        else:
            self.show_wall_warning = False

        if (
            self.wall_warning_enabled
            and not self.wall_warning_triggered
            and self.wall_timer >= self.wall_interval - 120
        ):
            self.wall_warning_triggered = True
            self.wall_warning_timer = self.wall_warning_duration
            self.show_wall_warning = True

        # =====================
        # SINH BÃO TUYẾT
        # =====================

        # Màn 2 trở đi: không cho bão tuyết xuất hiện quá sớm đầu màn
        if current_level >= 2 and distance < 2500:
            # Giữ wall_timer chưa chạy quá sớm
            self.wall_timer = 0

        # Nếu đã tới thời điểm bão tuyết, ưu tiên sinh bão tuyết
        if self.wall_timer >= self.wall_interval:
            self.spawn_wall_obstacle()
            self.wall_timer = 0
            self.spawn_timer = 0
            self.show_wall_warning = False

        elif self.spawn_timer >= self.spawn_interval:
            # Nếu gần tới bão tuyết thì không spawn cục băng nữa
            # để bão tuyết xuất hiện riêng
            near_wall_time = self.wall_timer >= self.wall_interval - 130

            if not near_wall_time:
                if distance > 2000 and random.random() < 0.35:
                    self.spawn_double_obstacle()
                else:
                    self.spawn_obstacle()

            self.spawn_timer = 0

        current_depth_speed = self.depth_speed + (speed - 5) * 0.0004

        for obstacle in self.obstacles:
            obstacle.update(current_depth_speed)

        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if not obstacle.is_out_of_screen()
        ]

        self.obstacles.sort(key=lambda obstacle: obstacle.depth, reverse=True)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def check_collision(self, player):
        hit_count = 0

        for obstacle in self.obstacles:
            # Khối băng đã bị bắn vỡ thì đi qua được
            if obstacle.passable:
                continue

            if obstacle.depth <= 0.08 and not obstacle.hit_checked:
                obstacle.hit_checked = True

                if obstacle.type == "wall":
                    obstacle.hit_player = True
                    hit_count += 1

                elif obstacle.lane == player.current_lane:
                    obstacle.hit_player = True
                    hit_count += 1

        return hit_count
    
    def check_bullet_hits(self, projectile_manager):
        for bullet in projectile_manager.bullets[:]:
            for obstacle in self.obstacles[:]:

                # Không cho bắn tường tuyết / bão tuyết
                if obstacle.type == "wall":
                    continue

                # Khối băng đã vỡ thì bỏ qua
                if obstacle.passable:
                    continue

                if bullet.lane == obstacle.lane:
                    if abs(bullet.depth - obstacle.depth) < 0.08:
                        obstacle.take_bullet_hit()
                        bullet.active = False
                        break

    def should_show_wall_warning(self):
        return self.show_wall_warning

    def reset(self):
        self.obstacles = []
        self.spawn_timer = 0
        self.wall_timer = 0
        self.show_wall_warning = False
        self.wall_warning_triggered = False
        self.wall_warning_timer = 0
        
    def clear_visible_obstacles(self):
        # Bom phá toàn bộ vật cản đang nhìn thấy trên màn hình
        destroyed_count = len(self.obstacles)
        self.obstacles = []
        return destroyed_count