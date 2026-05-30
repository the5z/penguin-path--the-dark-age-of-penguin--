# intro_cutscene.py

import os
import pygame

from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, DARK_BLUE


def load_intro_image(path):
    if not os.path.exists(path):
        print(f"Không tìm thấy ảnh intro: {path}")
        return None

    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
    return image


class IntroCutscene:
    def __init__(self, ui, sound_manager=None):
        self.ui = ui
        self.sound_manager = sound_manager

        self.scenes = [
            {
                "image": load_intro_image("assets/cutscene/intro_1.png"),
                "text": "Trái Đất đang nóng lên từng ngày...",
                "duration": FPS * 4,
            },
            {
                "image": load_intro_image("assets/cutscene/intro_2.png"),
                "text": "Ngôi làng chim cánh cụt bắt đầu tan băng.",
                "duration": FPS * 4,
            },
            {
                "image": load_intro_image("assets/cutscene/intro_3.png"),
                "text": "Trưởng làng trao cho Piko chiếc balo và niềm hy vọng.",
                "duration": FPS * 4,
            },
            {
                "image": load_intro_image("assets/cutscene/intro_4.png"),
                "text": "Piko rời làng, bắt đầu hành trình băng giá.",
                "duration": FPS * 4,
            },
        ]

        self.start()

    def start(self):
        self.scene_index = 0
        self.timer = 0
        self.finished = False
        self.sound_played = False

    def skip(self):
        self.finished = True

    def update(self):
        if self.finished:
            return

        if not self.sound_played:
            if self.sound_manager is not None:
                self.sound_manager.play("intro")
            self.sound_played = True

        self.timer += 1

        current_scene = self.scenes[self.scene_index]

        if self.timer >= current_scene["duration"]:
            self.timer = 0
            self.scene_index += 1

            if self.scene_index >= len(self.scenes):
                self.finished = True

    def draw(self, screen):
        if self.finished:
            screen.fill((80, 180, 255))
            return

        current_scene = self.scenes[self.scene_index]
        image = current_scene["image"]
        text = current_scene["text"]

        if image is not None:
            screen.blit(image, (0, 0))
        else:
            screen.fill((80, 180, 255))

            self.ui.draw_center_text(
                screen,
                f"CẢNH {self.scene_index + 1}",
                WIDTH // 2,
                HEIGHT // 2 - 120,
                DARK_BLUE,
                "big"
            )

        # Hộp thoại
        box_w = int(WIDTH * 0.78)
        box_h = 120
        box_x = WIDTH // 2 - box_w // 2
        box_y = HEIGHT - box_h - 45

        dialogue_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        dialogue_surface.fill((255, 255, 255, 220))
        screen.blit(dialogue_surface, (box_x, box_y))

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (box_x, box_y, box_w, box_h),
            4,
            border_radius=22
        )

        self.ui.draw_center_text(
            screen,
            text,
            WIDTH // 2,
            box_y + 28,
            BLACK
        )

        self.ui.draw_center_text(
            screen,
            "Nhấn SPACE / ENTER / ESC để bỏ qua",
            WIDTH // 2,
            box_y + 75,
            DARK_BLUE,
            "small"
        )