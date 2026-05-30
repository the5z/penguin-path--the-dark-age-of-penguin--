import random
import pygame

from perspective import get_perspective_position


class Coin:
    def __init__(self, lane, depth):
        self.lane = lane
        self.depth = depth
        self.active = True
        self.collected = False

    def update(self, speed):
        depth_speed = 0.0065 + (speed - 5) * 0.0004
        self.depth -= depth_speed

        if self.depth < -0.25:
            self.active = False

    def get_rect(self):
        visible_depth = max(-0.25, min(1.0, self.depth))
        x, y, scale = get_perspective_position(self.lane, visible_depth)

        if self.depth < 0:
            extra = min(abs(self.depth), 0.25)
            y += extra * 420
            scale *= 1 + extra * 1.5

        size = max(10, int(26 * scale))

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
            (255, 210, 50),
            rect.center,
            rect.w // 2
        )

        pygame.draw.circle(
            screen,
            (255, 245, 150),
            rect.center,
            max(2, rect.w // 4)
        )

        pygame.draw.circle(
            screen,
            (180, 120, 20),
            rect.center,
            rect.w // 2,
            max(1, rect.w // 10)
        )


class CoinManager:
    def __init__(self):
        self.coins = []

        self.spawn_timer = 0
        self.spawn_interval = 110

    def spawn_coin_line(self):
        lane = random.randint(0, 2)

        # 5 xu trên cùng 1 đường thẳng
        depths = [1.00, 0.90, 0.80, 0.70, 0.60]

        for depth in depths:
            self.coins.append(Coin(lane, depth))

    def update(self, speed):
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_coin_line()
            self.spawn_timer = 0

        for coin in self.coins:
            coin.update(speed)

        self.coins = [
            coin for coin in self.coins
            if coin.active
        ]

        # Xa vẽ trước, gần vẽ sau
        self.coins.sort(key=lambda coin: coin.depth, reverse=True)

    def draw(self, screen):
        for coin in self.coins:
            coin.draw(screen)

    def check_collision(self, player):
        collected = 0

        for coin in self.coins:
            if not coin.active:
                continue

            if coin.lane == player.current_lane and coin.depth <= 0.08:
                coin.active = False
                collected += 1

        self.coins = [
            coin for coin in self.coins
            if coin.active
        ]

        return collected

    def reset(self):
        self.coins = []
        self.spawn_timer = 0