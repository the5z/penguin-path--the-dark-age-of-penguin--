import pygame
import random
import sys

pygame.init()

# ======================
# CÀI ĐẶT CƠ BẢN
# ======================

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dark age of penguins - Prototype")

clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLUE = (120, 200, 255)
DARK_BLUE = (30, 80, 120)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
YELLOW = (255, 220, 80)
GREEN = (80, 220, 120)

# 3 làn đường
LANES = [250, 400, 550]
current_lane = 1

# Nhân vật
player_width = 50
player_height = 60
player_y = HEIGHT - 120
player_x = LANES[current_lane] - player_width // 2

# Trạng thái người chơi
health = 3
score = 0
distance = 0
finish_distance = 12000

# Khiên
shield_active = False
shield_timer = 0
shield_duration = 120  # 2 giây nếu FPS = 60
shield_cooldown = 0
shield_cooldown_max = 180  # 3 giây

# Vật cản
obstacles = []
obstacle_speed = 5
spawn_timer = 0
spawn_interval = 70

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)


# ======================
# HÀM HỖ TRỢ
# ======================

def draw_text(text, x, y, color=BLACK, size="normal"):
    used_font = big_font if size == "big" else font
    img = used_font.render(text, True, color)
    screen.blit(img, (x, y))


def spawn_obstacle():
    lane = random.randint(0, 2)
    obstacle = {
        "lane": lane,
        "x": LANES[lane] - 25,
        "y": -80,
        "w": 50,
        "h": 50
    }
    obstacles.append(obstacle)


def draw_player(x, y):
    # Thân chim cánh cụt
    pygame.draw.ellipse(screen, BLACK, (x, y, player_width, player_height))
    pygame.draw.ellipse(screen, WHITE, (x + 10, y + 15, 30, 35))

    # Mắt
    pygame.draw.circle(screen, WHITE, (x + 18, y + 15), 5)
    pygame.draw.circle(screen, WHITE, (x + 32, y + 15), 5)
    pygame.draw.circle(screen, BLACK, (x + 18, y + 15), 2)
    pygame.draw.circle(screen, BLACK, (x + 32, y + 15), 2)

    # Mỏ
    pygame.draw.polygon(screen, YELLOW, [
        (x + 25, y + 23),
        (x + 15, y + 30),
        (x + 35, y + 30)
    ])

    # Khiên
    if shield_active:
        pygame.draw.circle(
            screen,
            BLUE,
            (x + player_width // 2, y + player_height // 2),
            45,
            4
        )


def draw_road():
    screen.fill((220, 245, 255))

    # Nền đường tuyết
    pygame.draw.rect(screen, WHITE, (180, 0, 440, HEIGHT))

    # Vẽ vạch chia làn
    pygame.draw.line(screen, BLUE, (325, 0), (325, HEIGHT), 4)
    pygame.draw.line(screen, BLUE, (475, 0), (475, HEIGHT), 4)

    # Viền đường
    pygame.draw.line(screen, DARK_BLUE, (180, 0), (180, HEIGHT), 5)
    pygame.draw.line(screen, DARK_BLUE, (620, 0), (620, HEIGHT), 5)


def check_collision(player_rect, obstacle_rect):
    return player_rect.colliderect(obstacle_rect)


def reset_game():
    global current_lane, player_x, health, score, distance
    global shield_active, shield_timer, shield_cooldown
    global obstacles, obstacle_speed, spawn_timer

    current_lane = 1
    player_x = LANES[current_lane] - player_width // 2

    health = 3
    score = 0
    distance = 0

    shield_active = False
    shield_timer = 0
    shield_cooldown = 0

    obstacles = []
    obstacle_speed = 5
    spawn_timer = 0


# ======================
# GAME LOOP
# ======================

hand_command = "CENTER"
hand_gesture = "NONE"

game_state = "playing"
while True:
    clock.tick(FPS)

    # ======================
    # XỬ LÝ SỰ KIỆN
    # ======================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    current_lane = max(0, current_lane - 1)

                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    current_lane = min(2, current_lane + 1)

                if event.key == pygame.K_SPACE:
                    if shield_cooldown <= 0:
                        shield_active = True
                        shield_timer = shield_duration
                        shield_cooldown = shield_cooldown_max

            if game_state in ["win", "lose"]:
                if hand_command == "LEFT":
                    current_lane = 0
                elif hand_command == "CENTER":
                    current_lane = 1
                elif hand_command == "RIGHT":
                    current_lane = 2

                if hand_gesture == "FIST":
                    if shield_cooldown <= 0:
                        shield_active = True
                        shield_timer = shield_duration
                        shield_cooldown = shield_cooldown_max                
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"

    # ======================
    # CẬP NHẬT GAME
    # ======================

    if game_state == "playing":
        # Cập nhật vị trí nhân vật theo lane
        target_x = LANES[current_lane] - player_width // 2
        player_x += (target_x - player_x) * 0.25

        # Cập nhật khiên
        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        if shield_cooldown > 0:
            shield_cooldown -= 1

        # Sinh vật cản
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_obstacle()
            spawn_timer = 0

        # Di chuyển vật cản
        for obs in obstacles:
            obs["y"] += obstacle_speed

        # Xóa vật cản đã đi qua
        obstacles = [obs for obs in obstacles if obs["y"] < HEIGHT + 100]

        # Va chạm
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        for obs in obstacles[:]:
            obstacle_rect = pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"])

            if check_collision(player_rect, obstacle_rect):
                obstacles.remove(obs)

                if shield_active:
                    shield_active = False
                else:
                    health -= 1

                    if health <= 0:
                        game_state = "lose"

        # Điểm và khoảng cách
        score += 1
        distance += obstacle_speed

        # Tăng độ khó nhẹ
        if distance % 500 < obstacle_speed:
            obstacle_speed += 0.3

        # Thắng
        if distance >= finish_distance:
            game_state = "win"

    # ======================
    # VẼ GAME
    # ======================

    draw_road()

    # Vẽ vật cản
    for obs in obstacles:
        pygame.draw.rect(
            screen,
            RED,
            (obs["x"], obs["y"], obs["w"], obs["h"]),
            border_radius=10
        )

    # Vẽ người chơi
    draw_player(int(player_x), player_y)

    # HUD
    draw_text(f"HP: {health}", 20, 20)
    draw_text(f"Score: {score}", 20, 60)
    draw_text(f"Distance: {int(distance)}/{finish_distance}", 20, 100)

    if shield_cooldown <= 0:
        draw_text("Shield: READY", 20, 140, GREEN)
    else:
        draw_text(f"Shield: {shield_cooldown // 60 + 1}s", 20, 140, RED)

    draw_text("A/D or ←/→: Move | Space: Shield", 180, HEIGHT - 40, DARK_BLUE)

    # Màn thắng/thua
    if game_state == "win":
        pygame.draw.rect(screen, WHITE, (150, 180, 500, 220), border_radius=20)
        draw_text("YOU WIN!", 290, 230, GREEN, "big")
        draw_text("Piko da ve dich an toan!", 230, 300)
        draw_text("Nhan R de choi lai", 270, 350)

    if game_state == "lose":
        pygame.draw.rect(screen, WHITE, (150, 180, 500, 220), border_radius=20)
        draw_text("GAME OVER", 250, 230, RED, "big")
        draw_text("Piko da va cham qua nhieu!", 220, 300)
        draw_text("Nhan R de choi lai", 270, 350)

    pygame.display.flip()