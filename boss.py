import os
import math
import random
import pygame

from settings import WIDTH, HEIGHT, LANES, WHITE, BLACK, RED, FPS
from perspective import get_perspective_position


def load_image(path, size=None):
    if not os.path.exists(path):
        print(f"Khong tim thay anh boss: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()

    if size is not None:
        image = pygame.transform.scale(image, size)

    return image


def load_animation(prefix, count, size=None):
    frames = []

    for i in range(1, count + 1):
        path = f"{prefix}_{i}.png"
        frames.append(load_image(path, size))

    return frames

class BearThrowObject:
    def __init__(self, start_x, start_y, lane, kind):
        self.start_x = start_x
        self.start_y = start_y

        self.lane = lane
        self.kind = kind  # "ice" hoặc "tree"

        self.x = start_x
        self.y = start_y

        # Vật được ném tới điểm xa trên đường trước
        self.land_depth = 0.85
        target_x, target_y, _ = get_perspective_position(lane, self.land_depth)

        self.target_x = target_x
        self.target_y = target_y

        # Giai đoạn 1: bay từ tay gấu ra lane
        self.phase = "fly_from_bear"
        self.fly_timer = 0
        self.fly_duration = 25

        # Giai đoạn 2: trôi về phía Piko như vật cản
        self.depth = self.land_depth
        self.speed = 0.010

        self.active = True
        self.hit_checked = False

        self.base_size = 125
        self.min_size = 45

    def update(self):
        if self.phase == "fly_from_bear":
            self.fly_timer += 1
            progress = min(1, self.fly_timer / self.fly_duration)

            # Bay từ tay gấu ra vị trí rơi
            self.x = self.start_x + (self.target_x - self.start_x) * progress

            # Bay cong nhẹ lên rồi rơi xuống
            arc = 4 * progress * (1 - progress)
            self.y = self.start_y + (self.target_y - self.start_y) * progress - int(80 * arc)

            if progress >= 1:
                self.phase = "roll_to_piko"
                self.depth = self.land_depth

        elif self.phase == "roll_to_piko":
            self.depth -= self.speed

            if self.depth < -0.25:
                self.active = False

    def get_rect(self):
        if self.phase == "fly_from_bear":
            size = 55

            return pygame.Rect(
                int(self.x - size // 2),
                int(self.y - size // 2),
                size,
                size
            )

        visible_depth = max(-0.25, min(1.0, self.depth))
        x, y, scale = get_perspective_position(self.lane, visible_depth)

        if self.depth < 0:
            extra = min(abs(self.depth), 0.25)
            y += extra * 420
            scale *= 1 + extra * 1.5

        size = max(self.min_size, int(self.base_size * scale))

        return pygame.Rect(
            int(x - size // 2),
            int(y - size // 2),
            size,
            size
        )

    def draw(self, screen, ice_image=None, tree_image=None):
        rect = self.get_rect()
        image = ice_image if self.kind == "ice" else tree_image

        if image is not None:
            scaled_image = pygame.transform.smoothscale(image, (rect.w, rect.h))
            screen.blit(scaled_image, rect)
            return

        # fallback nếu thiếu ảnh
        if self.kind == "ice":
            pygame.draw.circle(screen, (120, 220, 255), rect.center, rect.w // 2)
            pygame.draw.circle(screen, WHITE, rect.center, rect.w // 2, 3)
        else:
            pygame.draw.rect(screen, (120, 75, 35), rect, border_radius=8)

class BearLaneAttack:
    def __init__(self, attack_lanes):
        self.attack_lanes = attack_lanes

        self.depth = 1.0
        self.speed = 0.012

        self.active = True
        self.hit_checked = False

        self.timer = 0
        self.warning_duration = 50

    def update(self):
        self.timer += 1

        if self.timer > self.warning_duration:
            self.depth -= self.speed

        if self.depth < -0.25:
            self.active = False

    def is_dangerous(self):
        return self.depth <= 0.08

    def draw(self, screen):
        for lane in self.attack_lanes:
            visible_depth = max(-0.25, min(1.0, self.depth))
            x, y, scale = get_perspective_position(lane, visible_depth)

            if self.depth < 0:
                extra = min(abs(self.depth), 0.25)
                y += extra * 420
                scale *= 1 + extra * 1.5

            w = max(40, int(95 * scale))
            h = max(60, int(170 * scale))

            rect = pygame.Rect(
                int(x - w // 2),
                int(y - h // 2),
                w,
                h
            )

            if self.timer <= self.warning_duration:
                color = (255, 210, 60)
            else:
                color = (230, 60, 60)

            pygame.draw.rect(screen, color, rect, 5, border_radius=12)
            pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 4)
            pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 4)


class PolarBearBoss:
    def __init__(self):
        from settings import BOSS_W, BOSS_H
        self.active = False
        self.state = "hidden"

        self.timer = 0
        self.scene_timer = 0

        self.width = BOSS_W
        self.height = BOSS_H

        # Ảnh boss
        self.image = load_image("assets/boss/polar_bear.png", (self.width, self.height))

        self.intro_frames = load_animation(
            "assets/boss/bear_intro",
            5,
            (self.width, self.height)
        )

        self.run_frames = load_animation(
            "assets/boss/bear_run",
            5,
            (self.width, self.height)
        )

        self.throw_image = load_image(
            "assets/boss/bear_throw.png",
            (self.width, self.height)
        )

        self.jump_attack_image = load_image(
            "assets/boss/bear_jump_attack.png",
            (self.width + 10, self.height + 10)
        )

        self.ice_image = load_image("assets/boss/boss_ice.png")
        self.tree_image = load_image("assets/boss/boss_tree.png")

        # Vị trí xuất hiện từ trái
        self.start_x = -280
        self.start_y = HEIGHT - 170

        # Vị trí boss chạy sau Piko
        self.chase_x = WIDTH // 2 - self.width // 2
        self.chase_y = HEIGHT - 165

        self.x = self.start_x
        self.y = self.start_y

        # Camera lùi để thấy boss
        self.camera_pullback = 0
        self.target_camera_pullback = 100

        # Animation 5 frame/s
        self.animation_timer = 0
        self.animation_speed = 12
        self.animation_index = 0

        # Skill
        self.attack_timer = 0
        self.attack_interval = 130

        self.projectiles = []
        self.lane_attacks = []

        # Nhảy đánh 2 lane
        self.leap_lane = None
        self.leap_start_x = 0
        self.leap_start_y = 0
        self.leap_target_x = 0
        self.leap_target_y = 0

        # Final block sau 60s
        self.final_started = False
        self.final_hit_checked = False
        self.final_warning_duration = 28
        self.final_duration = 52

        self.final_start_x = 0
        self.final_start_y = 0
        self.final_target_x = LANES[1] - self.width // 2
        self.final_target_y = HEIGHT - 210

        self.stun_timer = 0
        
    def start(self):
        if self.active:
            return

        self.active = True
        self.state = "intro"

        self.timer = 0
        self.scene_timer = 0
        self.attack_timer = 0

        self.x = self.start_x
        self.y = self.start_y

        self.camera_pullback = 0
        self.animation_index = 0
        self.animation_timer = 0

    def update_animation(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % 5

    def update(self):
        if not self.active:
            return
        
        if self.stun_timer > 0:
            self.stun_timer -= 1

            # Khi bị choáng thì vẫn cho vật thể cũ trôi tiếp
            for projectile in self.projectiles:
                projectile.update()

            for lane_attack in self.lane_attacks:
                lane_attack.update()

            self.projectiles = [
                projectile for projectile in self.projectiles
                if projectile.active
            ]

            self.lane_attacks = [
                lane_attack for lane_attack in self.lane_attacks
                if lane_attack.active
            ]

            return
        
        self.timer += 1
        self.scene_timer += 1

        self.update_animation()

        if self.state == "intro":
            self.update_intro()

        elif self.state == "chase":
            self.update_chase()

        elif self.state == "throw":
            self.update_throw()

        elif self.state == "leap_attack":
            self.update_leap_attack()

        elif self.state == "final_warning":
            self.update_final_warning()

        elif self.state == "final_block":
            self.update_final_block()

        for projectile in self.projectiles:
            projectile.update()

        for lane_attack in self.lane_attacks:
            lane_attack.update()

        self.projectiles = [
            projectile for projectile in self.projectiles
            if projectile.active
        ]

        self.lane_attacks = [
            lane_attack for lane_attack in self.lane_attacks
            if lane_attack.active
        ]

    def update_intro(self):
        progress = min(1, self.timer / 80)

        self.x = self.start_x + (self.chase_x - self.start_x) * progress

        drift_y = self.start_y + (self.chase_y - self.start_y) * progress
        jump_curve = 4 * progress * (1 - progress)
        self.y = drift_y - int(110 * jump_curve)

        self.camera_pullback = int(self.target_camera_pullback * progress)

        if progress >= 1:
            self.state = "chase"
            self.timer = 0

    def update_chase(self):
        self.x = self.chase_x + int(8 * math.sin(self.timer * 0.08))
        self.y = self.chase_y + int(5 * math.sin(self.timer * 0.12))

        if self.camera_pullback < self.target_camera_pullback:
            self.camera_pullback += 1

        if self.scene_timer >= FPS * 60 and not self.final_started:
            self.final_started = True
            self.state = "final_warning"
            self.timer = 0
            self.final_hit_checked = False
            return

        self.attack_timer += 1

        if self.attack_timer >= self.attack_interval:
            # Tạm tăng tỉ lệ ném để bạn dễ thấy skill
            if random.random() < 0.7:
                self.throw_from_behind()
            else:
                self.start_side_leap()

            self.attack_timer = 0
            self.attack_interval = random.randint(110, 170)

    def throw_from_behind(self):
        lane = random.randint(0, 2)
        kind = random.choice(["ice", "tree"])

        # Vị trí tay gấu
        hand_x = self.x + self.width * 0.62
        hand_y = self.y + self.height * 0.38

        self.projectiles.append(
            BearThrowObject(hand_x, hand_y, lane, kind)
        )

        self.state = "throw"
        self.timer = 0

    def update_throw(self):
        # Đứng ném trong nửa giây rồi quay lại chase
        if self.timer >= 30:
            self.state = "chase"
            self.timer = 0

    def start_side_leap(self):
        side_lane = random.choice([0, 2])

        if side_lane == 0:
            attack_lanes = [0, 1]
        else:
            attack_lanes = [1, 2]

        self.lane_attacks.append(
            BearLaneAttack(attack_lanes)
        )

        self.state = "leap_attack"
        self.timer = 0

        self.leap_lane = side_lane
        self.leap_start_x = self.x
        self.leap_start_y = self.y

        self.leap_target_x = LANES[side_lane] - self.width // 2
        self.leap_target_y = self.chase_y - 20

    def update_leap_attack(self):
        progress = min(1, self.timer / 45)

        self.x = self.leap_start_x + (self.leap_target_x - self.leap_start_x) * progress

        jump_curve = 4 * progress * (1 - progress)
        self.y = self.leap_start_y - int(120 * jump_curve)

        if progress >= 1:
            self.state = "chase"
            self.timer = 0
            self.x = self.chase_x
            self.y = self.chase_y

    def update_final_warning(self):
        if self.timer >= self.final_warning_duration:
            self.state = "final_block"
            self.timer = 0

            self.final_start_x = self.x
            self.final_start_y = self.y

    def update_final_block(self):
        progress = min(1, self.timer / self.final_duration)

        self.x = self.final_start_x + (self.final_target_x - self.final_start_x) * progress

        drift_y = self.final_start_y + (self.final_target_y - self.final_start_y) * progress
        jump_curve = 4 * progress * (1 - progress)
        self.y = drift_y - int(130 * jump_curve)

        if progress >= 1:
            self.x = self.final_target_x
            self.y = self.final_target_y

    def check_hits_player(self, player):
        hit_count = 0

        # Vật thể boss ném
        for projectile in self.projectiles:
            if projectile.active and not projectile.hit_checked:
                if projectile.phase == "roll_to_piko" and projectile.depth <= 0.08:
                    projectile.hit_checked = True

                    if projectile.lane == player.current_lane:
                        projectile.active = False
                        hit_count += 1

        # Đòn boss đánh 2 lane
        for lane_attack in self.lane_attacks:
            if lane_attack.active and not lane_attack.hit_checked:
                if lane_attack.is_dangerous():
                    lane_attack.hit_checked = True

                    if player.current_lane in lane_attack.attack_lanes:
                        hit_count += 1

        # Final block giữa
        if self.state == "final_block":
            if self.timer >= self.final_duration - 4 and not self.final_hit_checked:
                self.final_hit_checked = True

                if player.current_lane == 1:
                    hit_count += 1

        return hit_count

    def get_current_image(self):
        if self.state == "intro":
            image = self.intro_frames[self.animation_index]
            if image is not None:
                return image

        if self.state == "throw":
            if self.throw_image is not None:
                return self.throw_image

        if self.state == "leap_attack":
            if self.jump_attack_image is not None:
                return self.jump_attack_image

        if self.state in ["chase", "final_warning", "final_block"]:
            image = self.run_frames[self.animation_index]
            if image is not None:
                return image

        if self.image is not None:
            return self.image

        return None

    def draw(self, screen):
        if not self.active:
            return

        # Vùng đánh 2 lane
        for lane_attack in self.lane_attacks:
            lane_attack.draw(screen)

        # Vật thể boss ném
        for projectile in self.projectiles:
            projectile.draw(screen, self.ice_image, self.tree_image)

        # Boss
        image = self.get_current_image()

        if image is not None:
            screen.blit(image, (int(self.x), int(self.y)))
        else:
            rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
            pygame.draw.ellipse(screen, WHITE, rect)
            pygame.draw.ellipse(screen, BLACK, rect, 4)

            pygame.draw.circle(screen, BLACK, (rect.centerx - 35, rect.centery - 20), 8)
            pygame.draw.circle(screen, BLACK, (rect.centerx + 35, rect.centery - 20), 8)

            pygame.draw.polygon(screen, RED, [
                (rect.centerx, rect.centery),
                (rect.centerx - 15, rect.centery + 20),
                (rect.centerx + 15, rect.centery + 20),
            ])

    def get_camera_pullback(self):
        return self.camera_pullback

    def reset(self):
        self.__init__()

    def stun(self, duration=180):
        # 180 frame = 3 giây nếu FPS = 60
        self.stun_timer = duration

        # Xóa luôn các đòn boss đang tung ra
        self.projectiles = []
        self.lane_attacks = []