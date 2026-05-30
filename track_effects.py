# track_effects.py

import os
import random
import pygame

from settings import WIDTH, HEIGHT
from perspective import get_perspective_position


# =====================
# CHỈNH NHANH Ở ĐÂY
# =====================

TREE_IMAGE_PATH = "assets/decor/tree.png"
ROCK_IMAGE_PATH = "assets/decor/rock.png"
ICE_SPIKE_IMAGE_PATH = "assets/decor/ice_spike.png"

# Cây bên đường
TREE_COUNT_PER_SIDE = 6
TREE_BASE_SIZE_MIN = 90
TREE_BASE_SIZE_MAX = 130
TREE_MIN_SIZE = 45
TREE_MAX_SIZE = 190
TREE_SPEED_MULTIPLIER = 0.75

# Đá bên đường
ROCK_COUNT_PER_SIDE = 5
ROCK_BASE_SIZE_MIN = 65
ROCK_BASE_SIZE_MAX = 105
ROCK_MIN_SIZE = 35
ROCK_MAX_SIZE = 150
ROCK_SPEED_MULTIPLIER = 0.80

ICE_SPIKE_COUNT_PER_SIDE = 5
ICE_SPIKE_BASE_SIZE_MIN = 70
ICE_SPIKE_BASE_SIZE_MAX = 115
ICE_SPIKE_MIN_SIZE = 40
ICE_SPIKE_MAX_SIZE = 165
ICE_SPIKE_SPEED_MULTIPLIER = 0.78
# Vị trí 2 hàng vật thể ngoài đường
# Tăng/giảm mấy số này nếu muốn kéo cây/đá gần đường hoặc xa đường hơn
LEFT_FAR_X_RATIO = 0.36
LEFT_NEAR_X_RATIO = 0.06

RIGHT_FAR_X_RATIO = 0.64
RIGHT_NEAR_X_RATIO = 0.94

SIDE_FAR_Y_RATIO = 0.22
SIDE_NEAR_Y_RATIO = 1.05


def load_image(path):
    if not os.path.exists(path):
        print(f"Khong tim thay anh trang tri: {path}")
        return None

    return pygame.image.load(path).convert_alpha()


def get_side_position(side, depth):
    """
    side = "left" hoặc "right"
    depth = 1 xa, 0 gần
    """

    depth = max(-0.25, min(1.0, depth))
    t = 1 - depth

    far_y = int(HEIGHT * SIDE_FAR_Y_RATIO)
    near_y = int(HEIGHT * SIDE_NEAR_Y_RATIO)

    y = far_y + t * (near_y - far_y)

    if side == "left":
        far_x = int(WIDTH * LEFT_FAR_X_RATIO)
        near_x = int(WIDTH * LEFT_NEAR_X_RATIO)
    else:
        far_x = int(WIDTH * RIGHT_FAR_X_RATIO)
        near_x = int(WIDTH * RIGHT_NEAR_X_RATIO)

    x = far_x + t * (near_x - far_x)

    # Xa bé, gần to
    scale = 0.35 + t * 1.65

    return x, y, scale


class SnowStreak:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.depth = random.uniform(0.2, 1.0)
        self.length = random.randint(20, 60)

    def update(self, speed):
        self.depth -= speed

        if self.depth < 0:
            self.depth = 1.0
            self.lane = random.randint(0, 2)
            self.length = random.randint(20, 60)

    def draw(self, screen):
        x, y, scale = get_perspective_position(self.lane, self.depth)

        line_length = int(self.length * scale)
        line_width = max(1, int(3 * scale))

        pygame.draw.line(
            screen,
            (180, 230, 255),
            (x, y),
            (x, y + line_length),
            line_width
        )


class TreeProp:
    def __init__(self, side, image=None):
        self.side = side
        self.image = image
        self.depth = random.uniform(0.1, 1.0)
        self.base_size = random.randint(TREE_BASE_SIZE_MIN, TREE_BASE_SIZE_MAX)

    def reset(self):
        self.depth = 1.0
        self.base_size = random.randint(TREE_BASE_SIZE_MIN, TREE_BASE_SIZE_MAX)

    def update(self, speed):
        self.depth -= speed

        if self.depth < -0.25:
            self.reset()

    def draw(self, screen):
        x, y, scale = get_side_position(self.side, self.depth)

        size = max(TREE_MIN_SIZE, int(self.base_size * scale))
        size = min(size, TREE_MAX_SIZE)

        if self.image is not None:
            scaled_image = pygame.transform.smoothscale(
                self.image,
                (size, size)
            )

            # y - size để gốc cây nằm gần mặt đất
            screen.blit(
                scaled_image,
                (int(x - size // 2), int(y - size))
            )
            return

        # Fallback nếu thiếu ảnh cây
        trunk_color = (120, 80, 50)
        leaf_color = (80, 160, 120)

        trunk_w = max(6, int(size * 0.12))
        trunk_h = max(16, int(size * 0.28))

        pygame.draw.rect(
            screen,
            trunk_color,
            (
                int(x - trunk_w // 2),
                int(y - trunk_h),
                trunk_w,
                trunk_h
            )
        )

        pygame.draw.polygon(
            screen,
            leaf_color,
            [
                (int(x), int(y - size)),
                (int(x + size * 0.48), int(y - trunk_h)),
                (int(x - size * 0.48), int(y - trunk_h)),
            ]
        )


class RockProp:
    def __init__(self, side, image=None):
        self.side = side
        self.image = image
        self.depth = random.uniform(0.1, 1.0)
        self.base_size = random.randint(ROCK_BASE_SIZE_MIN, ROCK_BASE_SIZE_MAX)

    def reset(self):
        self.depth = 1.0
        self.base_size = random.randint(ROCK_BASE_SIZE_MIN, ROCK_BASE_SIZE_MAX)

    def update(self, speed):
        self.depth -= speed

        if self.depth < -0.25:
            self.reset()

    def draw(self, screen):
        x, y, scale = get_side_position(self.side, self.depth)

        size = max(ROCK_MIN_SIZE, int(self.base_size * scale))
        size = min(size, ROCK_MAX_SIZE)

        if self.image is not None:
            scaled_image = pygame.transform.smoothscale(
                self.image,
                (size, size)
            )

            # Đá nằm thấp hơn cây một chút
            screen.blit(
                scaled_image,
                (int(x - size // 2), int(y - size * 0.75))
            )
            return

        # Fallback nếu thiếu ảnh đá
        pygame.draw.ellipse(
            screen,
            (120, 170, 190),
            (
                int(x - size // 2),
                int(y - size // 2),
                int(size),
                int(size * 0.65)
            )
        )

class IceSpikeProp:
    def __init__(self, side, image=None):
        self.side = side
        self.image = image
        self.depth = random.uniform(0.1, 1.0)
        self.base_size = random.randint(
            ICE_SPIKE_BASE_SIZE_MIN,
            ICE_SPIKE_BASE_SIZE_MAX
        )

    def reset(self):
        self.depth = 1.0
        self.base_size = random.randint(
            ICE_SPIKE_BASE_SIZE_MIN,
            ICE_SPIKE_BASE_SIZE_MAX
        )

    def update(self, speed):
        self.depth -= speed

        if self.depth < -0.25:
            self.reset()

    def draw(self, screen):
        x, y, scale = get_side_position(self.side, self.depth)

        size = max(ICE_SPIKE_MIN_SIZE, int(self.base_size * scale))
        size = min(size, ICE_SPIKE_MAX_SIZE)

        if self.image is not None:
            scaled_image = pygame.transform.smoothscale(
                self.image,
                (size, size)
            )

            screen.blit(
                scaled_image,
                (int(x - size // 2), int(y - size * 0.95))
            )
            return

        # fallback nếu thiếu ảnh băng nhọn
        points = [
            (int(x), int(y - size)),
            (int(x + size * 0.38), int(y)),
            (int(x - size * 0.38), int(y)),
        ]

        pygame.draw.polygon(screen, (130, 220, 255), points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 3)
        
class TrackEffects:
    def __init__(self):
        self.snow_streaks = [SnowStreak() for _ in range(18)]

        self.tree_image = load_image(TREE_IMAGE_PATH)
        self.rock_image = load_image(ROCK_IMAGE_PATH)
        self.ice_spike_image = load_image(ICE_SPIKE_IMAGE_PATH)
        self.ice_spikes = []
        self.trees = []
        self.rocks = []

        for _ in range(TREE_COUNT_PER_SIDE):
            self.trees.append(TreeProp("left", self.tree_image))
            self.trees.append(TreeProp("right", self.tree_image))

        for _ in range(ROCK_COUNT_PER_SIDE):
            self.rocks.append(RockProp("left", self.rock_image))
            self.rocks.append(RockProp("right", self.rock_image))

        for _ in range(ICE_SPIKE_COUNT_PER_SIDE):
            self.ice_spikes.append(IceSpikeProp("left", self.ice_spike_image))
            self.ice_spikes.append(IceSpikeProp("right", self.ice_spike_image))
    def update(self, speed):
        effect_speed = 0.01 + (speed - 5) * 0.0005

        for streak in self.snow_streaks:
            streak.update(effect_speed)

        for tree in self.trees:
            tree.update(effect_speed * TREE_SPEED_MULTIPLIER)

        for rock in self.rocks:
            rock.update(effect_speed * ROCK_SPEED_MULTIPLIER)

        for ice_spike in self.ice_spikes:
            ice_spike.update(effect_speed * ICE_SPIKE_SPEED_MULTIPLIER)
    def draw_side_props(self, screen):
        all_props = self.trees + self.rocks + self.ice_spikes

        # Xa trước, gần sau
        all_props.sort(key=lambda prop: prop.depth, reverse=True)

        for prop in all_props:
            prop.draw(screen)

    def draw_snow_streaks(self, screen):
        for streak in self.snow_streaks:
            streak.draw(screen)