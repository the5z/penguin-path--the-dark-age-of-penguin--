# main.py

import os
import pygame
import sys
import ctypes

from intro_cutscene import IntroCutscene
from projectile import ProjectileManager
from enemy import EnemyManager
from track_effects import TrackEffects
from finish_line import FinishLine
from settings import (
    WIDTH,
    HEIGHT,
    FPS,

    WHITE,
    BLACK,
    BLUE,
    DARK_BLUE,
    RED,
    GREEN,
    SNOW_BG,

    ROAD_TOP_Y,
    ROAD_BOTTOM_Y,
    ROAD_TOP_LEFT_X,
    ROAD_TOP_RIGHT_X,
    ROAD_BOTTOM_LEFT_X,
    ROAD_BOTTOM_RIGHT_X,

    HUD_X,
    HP_Y,
    COIN_Y,
    SHIELD_Y,
    ENERGY_Y,

    LEVEL_FINISH_DISTANCE
)
from ui import UI
from player import Player
from obstacle import ObstacleManager
from camera_preview import CameraPreview
from hand_tracking import HandTracker
from start_screen import StartScreen
from effects import EffectManager
from sound_manager import SoundManager
from coin import CoinManager
from boss import PolarBearBoss

pygame.init()

sound_manager = SoundManager()
sound_manager.play_music()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The dark age of penguin - Prototype")

#def maximize_window():
    #try:
        #hwnd = pygame.display.get_wm_info()["window"]
        #ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 = SW_MAXIMIZE
    #except Exception as error:
        #print(f"Khong phong to duoc cua so: {error}")


   #maximize_window()
clock = pygame.time.Clock()

ui = UI()
player = Player()
current_level = 1
next_level_after_shop = None

obstacle_manager = ObstacleManager(current_level)

hand_tracker = HandTracker()
camera_preview = CameraPreview(hand_tracker=hand_tracker)
track_effects = TrackEffects()
finish_line = FinishLine()
start_screen = StartScreen()
runner_background = None
road_image = None
projectile_manager = ProjectileManager()
enemy_manager = EnemyManager()
win_sound_played = False
lose_panel_image = None
level_complete_panel_image = None
win_panel_image = None

effect_manager = EffectManager()
projectile_manager = ProjectileManager()
enemy_manager = EnemyManager()
boss = PolarBearBoss()
level3_timer = 0
coin_manager = CoinManager()
result_sound_played = False
item_gesture_cooldown = 0
level_hint_text = ""
level_hint_timer = 0
intro_cutscene = IntroCutscene(ui, sound_manager)
intro_cutscene.start()
shop_message = ""
shop_message_timer = 0
coin_sound_cooldown = 0
SHOP_ITEMS = {
    "heal": {
        "name": "Hoi mau +1 HP",
        "price": 5
    },
    "energy": {
        "name": "Nang luong +10",
        "price": 5
    },
    "slow": {
        "name": "Thuoc giam toc 10s",
        "price": 20
    },
    "bomb": {
        "name": "Bom pha vat can",
        "price": 50
    }
}
snowflake_hp_image = None
coin_icon_image = None
shield_icon_image = None
item_energy_icon = None
item_slow_icon = None
item_bomb_icon = None
if os.path.exists("assets/ui/snowflake_hp.png"):
    snowflake_hp_image = pygame.image.load(
        "assets/ui/snowflake_hp.png"
    ).convert_alpha()
    snowflake_hp_image = pygame.transform.smoothscale(
        snowflake_hp_image,
        (42, 42)
    )       
if os.path.exists("assets/ui/coin_icon.png"):
    coin_icon_image = pygame.image.load(
        "assets/ui/coin_icon.png"
    ).convert_alpha()
    coin_icon_image = pygame.transform.smoothscale(
        coin_icon_image,
        (40, 40)
    )

if os.path.exists("assets/ui/shield_icon.png"):
    shield_icon_image = pygame.image.load(
        "assets/ui/shield_icon.png"
    ).convert_alpha()
    shield_icon_image = pygame.transform.smoothscale(
        shield_icon_image,
        (42, 42)
    )
def load_ui_panel(path, size):
    if not os.path.exists(path):
        print(f"Khong tim thay anh UI: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image

if os.path.exists("assets/backgrounds/snow_runner_bg.png"):
    runner_background = pygame.image.load(
        "assets/backgrounds/snow_runner_bg.png"
    ).convert()
    runner_background = pygame.transform.smoothscale(
        runner_background,
        (WIDTH, HEIGHT)
    )
lose_panel_image = load_ui_panel(
    "assets/ui/lose_panel.png",
    (520, 260)
)

level_complete_panel_image = load_ui_panel(
    "assets/ui/level_complete_panel.png",
    (460, 220)
)

win_panel_image = load_ui_panel(
    "assets/ui/win_panel.png",
    (420, 180)
)
if os.path.exists("assets/backgrounds/road.png"):
    road_image = pygame.image.load(
        "assets/backgrounds/road.png"
    ).convert_alpha()
    road_image = pygame.transform.smoothscale(
        road_image,
        (WIDTH, HEIGHT)
    )
if os.path.exists("assets/ui/item_energy.png"):
    item_energy_icon = pygame.image.load(
        "assets/ui/item_energy.png"
    ).convert_alpha()
    item_energy_icon = pygame.transform.smoothscale(item_energy_icon, (34, 34))

if os.path.exists("assets/ui/item_slow.png"):
    item_slow_icon = pygame.image.load(
        "assets/ui/item_slow.png"
    ).convert_alpha()
    item_slow_icon = pygame.transform.smoothscale(item_slow_icon, (34, 34))

if os.path.exists("assets/ui/item_bomb.png"):
    item_bomb_icon = pygame.image.load(
        "assets/ui/item_bomb.png"
    ).convert_alpha()
    item_bomb_icon = pygame.transform.smoothscale(item_bomb_icon, (34, 34))
score = 0
distance = 0
coins = 0
obstacle_speed = 5
game_state = "intro"

saved_health = 5
MAX_PLAYER_HEALTH = 5

inventory = {
    "energy": 0,
    "slow": 0,
    "bomb": 0
}

slow_timer = 0

def draw_road():
    if runner_background is not None:
        screen.blit(runner_background, (0, 0))
    else:
        screen.fill(SNOW_BG)

    # Mat duong
    pygame.draw.polygon(screen, WHITE, [
        (ROAD_TOP_LEFT_X, ROAD_TOP_Y),
        (ROAD_TOP_RIGHT_X, ROAD_TOP_Y),
        (ROAD_BOTTOM_RIGHT_X, ROAD_BOTTOM_Y),
        (ROAD_BOTTOM_LEFT_X, ROAD_BOTTOM_Y),
    ])

    # Vien duong
    pygame.draw.line(
        screen,
        DARK_BLUE,
        (ROAD_TOP_LEFT_X, ROAD_TOP_Y),
        (ROAD_BOTTOM_LEFT_X, ROAD_BOTTOM_Y),
        5
    )

    pygame.draw.line(
        screen,
        DARK_BLUE,
        (ROAD_TOP_RIGHT_X, ROAD_TOP_Y),
        (ROAD_BOTTOM_RIGHT_X, ROAD_BOTTOM_Y),
        5
    )

    # Vach chia 3 lane
    lane1_top_x = int(ROAD_TOP_LEFT_X + (ROAD_TOP_RIGHT_X - ROAD_TOP_LEFT_X) / 3)
    lane2_top_x = int(ROAD_TOP_LEFT_X + 2 * (ROAD_TOP_RIGHT_X - ROAD_TOP_LEFT_X) / 3)

    lane1_bottom_x = int(ROAD_BOTTOM_LEFT_X + (ROAD_BOTTOM_RIGHT_X - ROAD_BOTTOM_LEFT_X) / 3)
    lane2_bottom_x = int(ROAD_BOTTOM_LEFT_X + 2 * (ROAD_BOTTOM_RIGHT_X - ROAD_BOTTOM_LEFT_X) / 3)

    pygame.draw.line(
        screen,
        BLUE,
        (lane1_top_x, ROAD_TOP_Y),
        (lane1_bottom_x, ROAD_BOTTOM_Y),
        4
    )

    pygame.draw.line(
        screen,
        BLUE,
        (lane2_top_x, ROAD_TOP_Y),
        (lane2_bottom_x, ROAD_BOTTOM_Y),
        4
    )
def draw_hp_snowflakes():
    start_x = HUD_X
    y = HP_Y
    spacing = 46

    for i in range(player.health):
        x = start_x + i * spacing

        if snowflake_hp_image is not None:
            screen.blit(snowflake_hp_image, (x, y))
        else:
            # fallback nếu chưa có ảnh
            center_x = x + 17
            center_y = y + 17

            pygame.draw.circle(screen, (220, 245, 255), (center_x, center_y), 12)
            pygame.draw.circle(screen, (120, 200, 255), (center_x, center_y), 12, 2)

            pygame.draw.line(screen, WHITE, (center_x - 10, center_y), (center_x + 10, center_y), 2)
            pygame.draw.line(screen, WHITE, (center_x, center_y - 10), (center_x, center_y + 10), 2)
            pygame.draw.line(screen, WHITE, (center_x - 7, center_y - 7), (center_x + 7, center_y + 7), 2)
            pygame.draw.line(screen, WHITE, (center_x - 7, center_y + 7), (center_x + 7, center_y - 7), 2)
def draw_hp_snowflakes():
    start_x = HUD_X + 20
    y = HP_Y + 18
    spacing = 40

    for i in range(player.health):
        x = start_x + i * spacing

        if snowflake_hp_image is not None:
            screen.blit(snowflake_hp_image, (x, y))
        else:
            center_x = x + 17
            center_y = y + 17

            pygame.draw.circle(screen, (220, 245, 255), (center_x, center_y), 12)
            pygame.draw.circle(screen, (120, 200, 255), (center_x, center_y), 12, 2)

            pygame.draw.line(screen, WHITE, (center_x - 10, center_y), (center_x + 10, center_y), 2)
            pygame.draw.line(screen, WHITE, (center_x, center_y - 10), (center_x, center_y + 10), 2)
            pygame.draw.line(screen, WHITE, (center_x - 7, center_y - 7), (center_x + 7, center_y + 7), 2)
            pygame.draw.line(screen, WHITE, (center_x - 7, center_y + 7), (center_x + 7, center_y - 7), 2)


def draw_coin_counter():
    x = HUD_X
    y = COIN_Y
    ...

    # Nền nhỏ sau tiền
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, 120, 42),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        DARK_BLUE,
        (x, y, 120, 42),
        2,
        border_radius=18
    )

    if coin_icon_image is not None:
        screen.blit(coin_icon_image, (x + 8, y + 4))
    else:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 140, 48), border_radius=18)
        pygame.draw.rect(screen, DARK_BLUE, (x, y, 140, 48), 2, border_radius=18)

    ui.draw_text(
        screen,
        f"x {coins}",
        x + 48,
        y + 9,
        BLACK
    )


def draw_shield_cooldown():
    x = HUD_X
    y = SHIELD_Y
    size = 44

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (x, y, 140, 50),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        DARK_BLUE,
        (x, y, 140, 50),
        2,
        border_radius=18
    )

    icon_x = x + 7
    icon_y = y + 7

    if shield_icon_image is not None:
        screen.blit(shield_icon_image, (icon_x, icon_y))
    else:
        pygame.draw.circle(screen, (120, 200, 255), (icon_x + 18, icon_y + 18), 18)
        pygame.draw.circle(screen, DARK_BLUE, (icon_x + 18, icon_y + 18), 18, 3)

    if player.shield_active:
        ui.draw_text(screen, "ON", x + 58, y + 12, GREEN)

    elif player.shield_cooldown <= 0:
        ui.draw_text(screen, "READY", x + 58, y + 12, GREEN)

    else:
        cooldown_second = player.shield_cooldown // FPS + 1
        ui.draw_text(screen, f"{cooldown_second}s", x + 65, y + 12, RED)

        bar_x = x + 55
        bar_y = y + 36
        bar_w = 70
        bar_h = 6

        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), border_radius=4)

        progress = 1 - player.shield_cooldown / player.shield_cooldown_max
        fill_w = int(bar_w * progress)

        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
def draw_hud():
    draw_hp_snowflakes()
    draw_coin_counter()
    draw_shield_cooldown()
    draw_energy_bar()
    draw_item_bar()

def draw_game_over():
    panel_w = 620
    panel_h = 280
    panel_x = WIDTH // 2 - panel_w // 2
    panel_y = HEIGHT // 2 - panel_h // 2 - 40

    if lose_panel_image is not None:
        scaled_panel = pygame.transform.smoothscale(
            lose_panel_image,
            (panel_w, panel_h)
        )
        screen.blit(scaled_panel, (panel_x, panel_y))
    else:
        pygame.draw.rect(
            screen,
            WHITE,
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=24
        )

        pygame.draw.rect(
            screen,
            RED,
            (panel_x, panel_y, panel_w, panel_h),
            5,
            border_radius=24
        )

    ui.draw_center_text(
        screen,
        "THẤT BẠI!",
        WIDTH // 2,
        panel_y + 45,
        RED,
        "big"
    )

    ui.draw_center_text(
        screen,
        "Piko đã va chạm quá nhiều!",
        WIDTH // 2,
        panel_y + 125,
        BLACK
    )

    ui.draw_center_text(
        screen,
        "Nhấn R để chơi lại",
        WIDTH // 2,
        panel_y + 180,
        BLACK
    )

    ui.draw_center_text(
        screen,
        "Nhấn ESC để về menu",
        WIDTH // 2,
        panel_y + 220,
        DARK_BLUE
    )

def draw_win():
    panel_w = 560
    panel_h = 260
    panel_x = WIDTH // 2 - panel_w // 2
    panel_y = HEIGHT // 2 - panel_h // 2 - 40

    if win_panel_image is not None:
        scaled_panel = pygame.transform.smoothscale(
            win_panel_image,
            (panel_w, panel_h)
        )
        screen.blit(scaled_panel, (panel_x, panel_y))
    else:
        pygame.draw.rect(
            screen,
            WHITE,
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=24
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (panel_x, panel_y, panel_w, panel_h),
            5,
            border_radius=24
        )

    ui.draw_center_text(
        screen,
        "CHIẾN THẮNG!",
        WIDTH // 2,
        panel_y + 45,
        GREEN,
        "big"
    )

    ui.draw_center_text(
        screen,
        "Piko đã vượt qua hành trình băng giá!",
        WIDTH // 2,
        panel_y + 125,
        BLACK
    )

    ui.draw_center_text(
        screen,
        "Nhấn R để chơi lại",
        WIDTH // 2,
        panel_y + 175,
        BLACK
    )

    ui.draw_center_text(
        screen,
        "Nhấn ESC để về menu",
        WIDTH // 2,
        panel_y + 210,
        DARK_BLUE
    )


def reset_game():
    global player, obstacle_manager, score, distance, obstacle_speed, game_state
    global track_effects, finish_line
    global projectile_manager, enemy_manager, coin_manager
    global boss, level3_timer
    global slow_timer, item_gesture_cooldown
    global level_hint_text, level_hint_timer
    global saved_health

    player = Player()
    player.health = saved_health
    player.max_health = MAX_PLAYER_HEALTH
    obstacle_manager = ObstacleManager(current_level)
    track_effects = TrackEffects()
    finish_line = FinishLine()

    projectile_manager = ProjectileManager()
    enemy_manager = EnemyManager()
    coin_manager = CoinManager()

    boss = PolarBearBoss()
    level3_timer = 0

    score = 0
    distance = 0
    obstacle_speed = 5
    slow_timer = 0
    item_gesture_cooldown = 0

    game_state = "playing"
    level_hint_text = ""
    level_hint_timer = 0

    if current_level == 2:
        level_hint_text = "MAN 2: Dung ky hieu sung hoac phim F de ban"
        level_hint_timer = FPS * 5

    elif current_level == 3:
        level_hint_text = "MAN 3: San sang doi dau boss gau Bac Cuc"
        level_hint_timer = FPS * 5
def draw_level_complete():
    panel_w = 620
    panel_h = 260
    panel_x = WIDTH // 2 - panel_w // 2
    panel_y = HEIGHT // 2 - panel_h // 2 - 40

    if level_complete_panel_image is not None:
        scaled_panel = pygame.transform.smoothscale(
            level_complete_panel_image,
            (panel_w, panel_h)
        )
        screen.blit(scaled_panel, (panel_x, panel_y))
    else:
        pygame.draw.rect(
            screen,
            WHITE,
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=24
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (panel_x, panel_y, panel_w, panel_h),
            5,
            border_radius=24
        )

    ui.draw_center_text(
        screen,
        "HOÀN THÀNH MÀN!",
        WIDTH // 2,
        panel_y + 45,
        GREEN,
        "big"
    )

    ui.draw_center_text(
        screen,
        "Piko đã chạm tới đích!",
        WIDTH // 2,
        panel_y + 125,
        BLACK
    )

    ui.draw_center_text(
        screen,
        "Nhấn N để vào cửa hàng",
        WIDTH // 2,
        panel_y + 175,
        DARK_BLUE
    )

    ui.draw_center_text(
        screen,
        "Nhấn ESC để về menu",
        WIDTH // 2,
        panel_y + 210,
        BLACK
    )

def quit_game():
    sound_manager.stop_music()
    camera_preview.release()
    hand_tracker.close()
    pygame.quit()
    sys.exit()

def load_ui_panel(path, size):
    if not os.path.exists(path):
        print(f"Khong tim thay anh UI: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image

def get_finish_distance():
    return LEVEL_FINISH_DISTANCE.get(current_level, 12000)

last_hand_gesture = "NONE"
gesture_hold_frames = 0

shield_gesture_cooldown = 0
shoot_gesture_cooldown = 0

# Sau khi nhận dạng GUN, khóa FIST một chút để tránh kích nhầm khiên
shield_after_gun_lock = 0

def buy_item(item_key):
    global coins, saved_health
    global shop_message, shop_message_timer

    item = SHOP_ITEMS[item_key]
    price = item["price"]

    if coins < price:
        sound_manager.play("not_enough_coin")
        shop_message = "Không đủ xu!"
        shop_message_timer = FPS * 2
        return False

    if item_key == "heal":
        if saved_health >= MAX_PLAYER_HEALTH:
            shop_message = "Máu đã đầy!"
            shop_message_timer = FPS * 2
            return False

        coins -= price
        saved_health += 1
        player.health = saved_health

        shop_message = "Đã hồi 1 máu!"
        shop_message_timer = FPS * 2
        return True

    coins -= price
    inventory[item_key] += 1

    if item_key == "energy":
        shop_message = "Đã mua năng lượng!"
    elif item_key == "slow":
        shop_message = "Đã mua thuốc làm chậm!"
    elif item_key == "bomb":
        shop_message = "Đã mua bom!"
    else:
        shop_message = "Đã mua vật phẩm!"

    shop_message_timer = FPS * 2
    return True

def use_item(item_key):
    global slow_timer

    if inventory[item_key] <= 0:
        return False

    if item_key == "energy":
        player.add_energy(10)
        inventory[item_key] -= 1
        return True

    if item_key == "slow":
        slow_timer = FPS * 10
        inventory[item_key] -= 1
        return True

    if item_key == "bomb":
        sound_manager.play("bomb")

        obstacle_manager.clear_visible_obstacles()

        if current_level == 3 and boss.active:
            boss.stun(FPS * 3)

        inventory[item_key] -= 1
        return True

    return False

def draw_shop():
    if runner_background is not None:
        screen.blit(runner_background, (0, 0))
    else:
        screen.fill((210, 240, 255))

    panel_w = 820
    panel_h = 600
    panel_x = WIDTH // 2 - panel_w // 2
    panel_y = HEIGHT // 2 - panel_h // 2

    pygame.draw.rect(
        screen,
        WHITE,
        (panel_x, panel_y, panel_w, panel_h),
        border_radius=28
    )

    pygame.draw.rect(
        screen,
        DARK_BLUE,
        (panel_x, panel_y, panel_w, panel_h),
        5,
        border_radius=28
    )

    ui.draw_center_text(
        screen,
        "CỬA HÀNG",
        WIDTH // 2,
        panel_y + 28,
        DARK_BLUE,
        "big"
    )

    ui.draw_center_text(
        screen,
        f"Xu hiện có: {coins}",
        WIDTH // 2,
        panel_y + 92,
        BLACK
    )

    lines = [
        ("1", "Hồi máu +1 HP", "5 xu", "Mua là hồi ngay", None),
        ("2", "Năng lượng +10", "5 xu", "Dùng trong trận", item_energy_icon),
        ("3", "Thuốc làm chậm 10 giây", "20 xu", "Giảm tốc độ game", item_slow_icon),
        ("4", "Bom phá vật cản", "50 xu", "Phá vật cản + choáng boss", item_bomb_icon),
    ]

    start_y = panel_y + 150
    row_gap = 82

    for key, name, price, note, icon in lines:
        row_y = start_y + (int(key) - 1) * row_gap

        pygame.draw.rect(
            screen,
            (235, 248, 255),
            (panel_x + 55, row_y - 8, panel_w - 110, 66),
            border_radius=16
        )

        pygame.draw.rect(
            screen,
            (180, 220, 240),
            (panel_x + 55, row_y - 8, panel_w - 110, 66),
            2,
            border_radius=16
        )

        # ô icon nhỏ bên trái
        icon_box_x = panel_x + 68
        icon_box_y = row_y + 3
        icon_box_size = 42

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (icon_box_x, icon_box_y, icon_box_size, icon_box_size),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (icon_box_x, icon_box_y, icon_box_size, icon_box_size),
            2,
            border_radius=10
        )

        if icon is not None:
            icon_draw = pygame.transform.smoothscale(icon, (30, 30))
            screen.blit(icon_draw, (icon_box_x + 6, icon_box_y + 6))
        else:
            ui.draw_center_text(
                screen,
                "HP",
                icon_box_x + icon_box_size // 2,
                icon_box_y + 8,
                RED,
                "small"
            )

        ui.draw_text(
            screen,
            f"{key}. {name}",
            panel_x + 125,
            row_y,
            BLACK
        )

        ui.draw_text(
            screen,
            price,
            panel_x + panel_w - 170,
            row_y,
            RED
        )

        ui.draw_text(
            screen,
            note,
            panel_x + 125,
            row_y + 30,
            DARK_BLUE,
            "small"
        )
    if shop_message_timer > 0 and shop_message != "":
        ui.draw_center_text(
            screen,
            shop_message,
            WIDTH // 2,
            panel_y + panel_h - 118,
            RED,
            "normal"
        )
    footer_y = panel_y + panel_h - 78

    ui.draw_center_text(
        screen,
        "Nhấn 1 / 2 / 3 / 4 để mua vật phẩm",
        WIDTH // 2,
        footer_y,
        BLACK
    )

    if next_level_after_shop is not None:
        continue_text = f"Nhấn N để vào màn {next_level_after_shop}"
    else:
        continue_text = "Nhấn N để tiếp tục"

    ui.draw_center_text(
        screen,
        continue_text,
        WIDTH // 2,
        footer_y + 36,
        GREEN
    )
def reset_player_progress():
    global coins, inventory, saved_health

    coins = 0
    saved_health = MAX_PLAYER_HEALTH

    inventory = {
        "energy": 0,
        "slow": 0,
        "bomb": 0
    }
def draw_center_hint():
    if level_hint_timer <= 0 or level_hint_text == "":
        return

    panel_w = 680
    panel_h = 70
    panel_x = WIDTH // 2 - panel_w // 2
    panel_y = 90

    hint_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    hint_surface.fill((255, 255, 255, 210))
    screen.blit(hint_surface, (panel_x, panel_y))

    pygame.draw.rect(
        screen,
        DARK_BLUE,
        (panel_x, panel_y, panel_w, panel_h),
        3,
        border_radius=18
    )

    ui.draw_center_text(
        screen,
        level_hint_text,
        WIDTH // 2,
        panel_y + 22,
        BLACK
    )
def draw_energy_bar():
    x = HUD_X
    y = ENERGY_Y
    w = 150
    h = 18

    pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), border_radius=8)
    pygame.draw.rect(screen, DARK_BLUE, (x, y, w, h), 2, border_radius=8)

    energy_ratio = player.energy / player.max_energy
    fill_w = int((w - 4) * energy_ratio)

    pygame.draw.rect(
        screen,
        (80, 190, 255),
        (x + 2, y + 2, fill_w, h - 4),
        border_radius=6
    )
def draw_item_bar():
    slot_count = 3
    slot_w = 78
    slot_h = 58
    gap = 14

    total_w = slot_count * slot_w + (slot_count - 1) * gap
    start_x = WIDTH // 2 - total_w // 2
    y = HEIGHT - 82

    items = [
        ("energy", item_energy_icon, inventory.get("energy", 0)),
        ("slow", item_slow_icon, inventory.get("slow", 0)),
        ("bomb", item_bomb_icon, inventory.get("bomb", 0)),
    ]

    for i, item_data in enumerate(items):
        item_key, icon, count = item_data

        x = start_x + i * (slot_w + gap)

        # nền ô
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (x, y, slot_w, slot_h),
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (x, y, slot_w, slot_h),
            3,
            border_radius=14
        )

        # vạch chéo trang trí
        pygame.draw.line(
            screen,
            (190, 225, 245),
            (x + 10, y + slot_h - 8),
            (x + slot_w - 10, y + 8),
            3
        )

        # icon item
        if icon is not None:
            icon_x = x + 8
            icon_y = y + 10
            screen.blit(icon, (icon_x, icon_y))
        else:
            # fallback nếu thiếu ảnh
            fallback_text = "E"
            if item_key == "slow":
                fallback_text = "S"
            elif item_key == "bomb":
                fallback_text = "B"

            ui.draw_center_text(
                screen,
                fallback_text,
                x + slot_w // 2,
                y + 16,
                DARK_BLUE
            )

        # số lượng item
        count_bg_size = 24
        count_bg_x = x + slot_w - count_bg_size - 6
        count_bg_y = y + 6

        pygame.draw.ellipse(
            screen,
            (255, 255, 255),
            (count_bg_x, count_bg_y, count_bg_size, count_bg_size)
        )

        pygame.draw.ellipse(
            screen,
            DARK_BLUE,
            (count_bg_x, count_bg_y, count_bg_size, count_bg_size),
            2
        )

        ui.draw_center_text(
            screen,
            str(count),
            count_bg_x + count_bg_size // 2,
            count_bg_y + 2,
            BLACK,
            "small"
        )
while True:
    # =====================
    # EVENT
    # =====================
    if shop_message_timer > 0:
        shop_message_timer -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:

            # =====================
            # INTRO
            # =====================
            if game_state == "intro":
                if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                    intro_cutscene.skip()
                    game_state = "start"

            # =====================
            # START MENU
            # =====================
            elif game_state == "start":
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    current_level = 1
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    quit_game()

            # =====================
            # SHOP
            # =====================
            elif game_state == "shop":
                if event.key == pygame.K_1:
                    buy_item("heal")

                elif event.key == pygame.K_2:
                    buy_item("energy")

                elif event.key == pygame.K_3:
                    buy_item("slow")

                elif event.key == pygame.K_4:
                    buy_item("bomb")

                elif event.key == pygame.K_n:
                    if next_level_after_shop is not None:
                        current_level = next_level_after_shop
                    else:
                        current_level += 1

                    reset_game()
                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    game_state = "start"

            # =====================
            # PLAYING
            # =====================
            elif game_state == "playing":
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    player.move_left()

                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.move_right()

                elif event.key == pygame.K_SPACE:
                    player.activate_shield()

                elif event.key == pygame.K_f and current_level >= 2:
                    if player.energy >= 1:
                        if projectile_manager.shoot(player.current_lane):
                            player.energy -= 1
                            sound_manager.play("shoot")

                elif event.key == pygame.K_e:
                    use_item("energy")

            # =====================
            # LEVEL COMPLETE
            # =====================
            elif game_state == "level_complete":
                if event.key == pygame.K_n:
                    game_state = "shop"

                elif event.key == pygame.K_ESCAPE:
                    game_state = "start"

                elif event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"

            # =====================
            # WIN / LOSE
            # =====================
            elif game_state in ["win", "lose"]:
                if event.key == pygame.K_r:
                    current_level = 1
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif event.key == pygame.K_ESCAPE:
                    game_state = "start"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state == "start":
                action = start_screen.handle_click(event.pos)

                if action == "start":
                    current_level = 1
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif action == "level_select":
                    start_screen.show_level_select = True
                    start_screen.show_tutorial = False

                elif action == "level_1":
                    current_level = 1
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif action == "level_2":
                    current_level = 2
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif action == "level_3":
                    current_level = 3
                    reset_player_progress()
                    reset_game()
                    game_state = "playing"

                elif action == "back":
                    start_screen.show_level_select = False

                elif action == "tutorial":
                    start_screen.show_tutorial = not start_screen.show_tutorial
                    start_screen.show_level_select = False

                elif action == "quit":
                    quit_game()
    if slow_timer > 0:
        slow_timer -= 1
        speed_multiplier = 0.75
    else:
        speed_multiplier = 1.0

    current_game_speed = obstacle_speed * speed_multiplier
    # =====================
    # UPDATE
    # =====================
    if game_state == "intro":
        intro_cutscene.update()

        if intro_cutscene.finished:
            game_state = "start"

    elif game_state == "playing":
        hand_command = "CENTER"
        hand_gesture = "NONE"
        if level_hint_timer > 0:
            level_hint_timer -= 1
        if camera_preview is not None:
            hand_command = camera_preview.get_command()
            hand_gesture = camera_preview.get_gesture()
        
            if camera_preview.is_hand_detected():
                if hand_command == "LEFT":
                    player.current_lane = 0
                elif hand_command == "CENTER":
                    player.current_lane = 1
                elif hand_command == "RIGHT":
                    player.current_lane = 2
                if item_gesture_cooldown > 0:
                    item_gesture_cooldown -= 1
                if item_gesture_cooldown <= 0:
                    # if hand_gesture == "ITEM_HEAL":
                    #     if use_item("heal"):
                    #         item_gesture_cooldown = 45

                    # elif hand_gesture == "ITEM_FAST_SHIELD":
                    #     if use_item("fast_shield"):
                    #         item_gesture_cooldown = 45
                    if hand_gesture == "ITEM_ENERGY":
                        if use_item("energy"):
                            item_gesture_cooldown = 45

                    elif hand_gesture == "ITEM_SLOW":
                        if use_item("slow"):
                            item_gesture_cooldown = 60

                    elif hand_gesture == "ITEM_BOMB":
                        if use_item("bomb"):
                            item_gesture_cooldown = 60
                                # Đếm gesture giữ ổn định bao lâu
                if hand_gesture == last_hand_gesture:
                    gesture_hold_frames += 1
                else:
                    last_hand_gesture = hand_gesture
                    gesture_hold_frames = 1

                if shield_gesture_cooldown > 0:
                    shield_gesture_cooldown -= 1

                if shoot_gesture_cooldown > 0:
                    shoot_gesture_cooldown -= 1

                if coin_sound_cooldown > 0:
                    coin_sound_cooldown -= 1

                if shield_after_gun_lock > 0:
                    shield_after_gun_lock -= 1
                if hand_gesture == "ITEM_HEAL":
                    use_item("heal")

                # elif hand_gesture == "ITEM_FAST_SHIELD":
                #     use_item("fast_shield")

                elif hand_gesture == "ITEM_SLOW":
                    use_item("slow")

                elif hand_gesture == "ITEM_BOMB":
                    use_item("bomb")
                # GUN được ưu tiên cao hơn FIST để tránh vừa làm súng vừa bật khiên
                if hand_gesture == "GUN":
                    shield_after_gun_lock = 20

                    if current_level >= 2 and gesture_hold_frames >= 3 and shoot_gesture_cooldown <= 0:
                        if player.energy >= 1:
                            if projectile_manager.shoot(player.current_lane):
                                player.energy -= 1
                                sound_manager.play("shoot")
                                shoot_gesture_cooldown = 18

                elif (
                    hand_gesture == "FIST"
                    and gesture_hold_frames >= 8
                    and shield_gesture_cooldown <= 0
                    and shield_after_gun_lock <= 0
                ):
                    player.activate_shield()
                    shield_gesture_cooldown = 40
        player.update()
        obstacle_manager.update(current_game_speed, distance, current_level)
        coin_manager.update(current_game_speed)
        track_effects.update(current_game_speed)
        finish_line.update(current_game_speed)
        effect_manager.update()

        if current_level == 3:
            level3_timer += 1

            if level3_timer >= FPS * 10 and not boss.active:
                boss.start()
                sound_manager.play("boss_roar")

            boss.update()
            player.camera_offset_y = boss.get_camera_pullback()
        else:
            player.camera_offset_y = 0

        collected_coins = coin_manager.check_collision(player)

        if collected_coins > 0:
            coins += collected_coins

            if coin_sound_cooldown <= 0:
                sound_manager.play("coin")
                score += collected_coins * 20
                coin_sound_cooldown = 8
        hit_count = obstacle_manager.check_collision(player)
        projectile_manager.update()

        if current_level >= 2:
            obstacle_manager.check_bullet_hits(projectile_manager)

        if current_level == 2:
            enemy_manager.update(current_game_speed)
            enemy_manager.check_bullet_hits(projectile_manager)

        if hit_count > 0:
            was_shielded = player.shield_active
            took_damage = player.take_hit()
            saved_health = player.health

            if was_shielded and not took_damage:
                effect_manager.spawn_shield_break(player.get_rect().center)
                sound_manager.play("shield_break")

            elif took_damage:
                effect_manager.spawn_damage_hit(player.get_rect().center)
                sound_manager.play("hit")

            if player.is_dead():
                if not result_sound_played:
                    sound_manager.play("lose")
                    result_sound_played = True

                game_state = "lose"

        if current_level == 2:
            arrow_hit_count = enemy_manager.check_arrow_hits_player(player)

            if arrow_hit_count > 0:
                was_shielded = player.shield_active
                took_damage = player.take_hit()

                if was_shielded and not took_damage:
                    effect_manager.spawn_shield_break(player.get_rect().center)
                    sound_manager.play("shield_break")

                elif took_damage:
                    effect_manager.spawn_damage_hit(player.get_rect().center)
                    sound_manager.play("hit")

                if player.is_dead():
                    if not result_sound_played:
                        sound_manager.play("lose")
                        result_sound_played = True

                    game_state = "lose"

        if current_level == 3 and boss.active:
            boss_hit_count = boss.check_hits_player(player)

            if boss_hit_count > 0:
                was_shielded = player.shield_active
                took_damage = player.take_hit()

                if was_shielded and not took_damage:
                    effect_manager.spawn_shield_break(player.get_rect().center)
                    sound_manager.play("shield_break")
                elif took_damage:
                    effect_manager.spawn_damage_hit(player.get_rect().center)
                    sound_manager.play("hit")

                if player.is_dead():
                    if not result_sound_played:
                        sound_manager.play("lose")
                        result_sound_played = True

                    game_state = "lose"

        score += 1
        distance += current_game_speed

        if distance % 500 < obstacle_speed:
            obstacle_speed += 0.3

        finish_line.update(obstacle_speed)

        if finish_line.reached:
            if not result_sound_played:
                sound_manager.play("win")
                result_sound_played = True

            player.start_celebration()

            if current_level < 3:
                game_state = "level_complete"
                next_level_after_shop = current_level + 1
            else:
                game_state = "win"
                        
        if distance >= get_finish_distance() - 1200:
            finish_line.start()
    elif game_state in ["level_complete", "win"]:
        player.update_celebration()
    if slow_timer > 0:
        slow_timer -= 1
        speed_multiplier = 0.75
    else:
        speed_multiplier = 1.0

    # =====================
    # DRAW
    # =====================

    if game_state == "intro":
        intro_cutscene.draw(screen)

        # Tạm comment dòng intro thật để test trước
        # intro_cutscene.draw(screen)

    elif game_state == "start":
        start_screen.draw(screen)

    elif game_state == "shop":
        draw_shop()

    else:
        draw_road()

        track_effects.draw_side_props(screen)
        track_effects.draw_snow_streaks(screen)

        finish_line.draw(screen)
        coin_manager.draw(screen)

        if current_level == 3:
            boss.draw(screen)

        if current_level >= 2:
            enemy_manager.draw(screen)

        projectile_manager.draw(screen)
        obstacle_manager.draw(screen)
        player.draw(screen)
        effect_manager.draw(screen)

        draw_hud()
        draw_center_hint()

        if camera_preview is not None:
            camera_preview.draw(screen, ui)

        if game_state == "level_complete":
            draw_level_complete()

        elif game_state == "win":
            draw_win()

        elif game_state == "lose":
            draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)