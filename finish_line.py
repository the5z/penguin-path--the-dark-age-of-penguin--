# finish_line.py

import pygame

from settings import WIDTH
from perspective import get_perspective_position


class FinishLine:
    def __init__(self):
        self.active = False
        self.depth = 1.0
        self.reached = False

    def start(self):
        if not self.active and not self.reached:
            self.active = True
            self.depth = 1.0

    def update(self, speed):
        if not self.active:
            return

        depth_speed = 0.006 + (speed - 5) * 0.0004
        self.depth -= depth_speed

        if self.depth <= 0.05:
            self.reached = True
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        left_x, y, scale = get_perspective_position(0, self.depth)
        mid_x, _, _ = get_perspective_position(1, self.depth)
        right_x, _, _ = get_perspective_position(2, self.depth)

        tile_w = int(34 * scale)
        tile_h = int(18 * scale)

        colors = [(30, 30, 30), (240, 240, 240)]

        start_x = int(left_x - tile_w)
        end_x = int(right_x + tile_w)

        count = 0
        x = start_x

        while x < end_x:
            color = colors[count % 2]
            pygame.draw.rect(
                screen,
                color,
                (x, int(y), tile_w, tile_h)
            )
            x += tile_w
            count += 1

        # 2 cột cờ nhỏ
        pole_h = int(80 * scale)

        pygame.draw.line(screen, (70, 70, 70), (left_x, y), (left_x, y - pole_h), max(2, int(4 * scale)))
        pygame.draw.line(screen, (70, 70, 70), (right_x, y), (right_x, y - pole_h), max(2, int(4 * scale)))

        pygame.draw.polygon(screen, (80, 180, 255), [
            (left_x, y - pole_h),
            (left_x + 35 * scale, y - pole_h + 10 * scale),
            (left_x, y - pole_h + 22 * scale),
        ])

        pygame.draw.polygon(screen, (80, 180, 255), [
            (right_x, y - pole_h),
            (right_x - 35 * scale, y - pole_h + 10 * scale),
            (right_x, y - pole_h + 22 * scale),
        ])
        