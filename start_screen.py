# start_screen.py

import os
import pygame

from settings import WIDTH, HEIGHT, WHITE, BLACK, BLUE, DARK_BLUE


class Button:
    def __init__(self, text, x, y, w, h, font, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.action = action

        self.normal_color = (35, 125, 235)
        self.hover_color = (70, 160, 255)
        self.border_color = (230, 250, 255)
        self.text_color = WHITE

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen, mouse_pos):
        hovered = self.is_hovered(mouse_pos)

        color = self.hover_color if hovered else self.normal_color

        # Bóng nút
        shadow_rect = self.rect.copy()
        shadow_rect.y += 6
        pygame.draw.rect(
            screen,
            (20, 60, 130),
            shadow_rect,
            border_radius=22
        )

        # Thân nút
        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=22
        )

        # Viền nút
        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            width=4,
            border_radius=22
        )

        # Text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        screen.blit(text_surface, (text_x, text_y))


class StartScreen:
    def __init__(self):
        self.background = None

        image_path = "assets/ui/start_screen.png"
        if os.path.exists(image_path):
            self.background = pygame.image.load(image_path).convert()
            self.background = pygame.transform.scale(
                self.background,
                (WIDTH, HEIGHT)
            )
        else:
            print(f"Khong tim thay anh start screen: {image_path}")

        self.title_font = pygame.font.SysFont(None, 76)
        self.button_font = pygame.font.SysFont(None, 44)
        self.small_button_font = pygame.font.SysFont(None, 34)
        self.info_font = pygame.font.SysFont(None, 28)

        self.buttons = [
            Button(
                "START GAME",
                WIDTH // 2 - 190,
                330,
                380,
                65,
                self.button_font,
                "start"
            ),
            Button(
                "LEVEL SELECT",
                WIDTH // 2 - 190,
                410,
                380,
                60,
                self.small_button_font,
                "level_select"
            ),
            Button(
                "TUTORIAL",
                WIDTH // 2 - 190,
                490,
                175,
                55,
                self.small_button_font,
                "tutorial"
            ),
            Button(
                "QUIT",
                WIDTH // 2 + 15,
                490,
                175,
                55,
                self.small_button_font,
                "quit"
            ),
        ]

        self.level_buttons = [
            Button(
                "LEVEL 1",
                WIDTH // 2 - 170,
                240,
                340,
                60,
                self.small_button_font,
                "level_1"
            ),
            Button(
                "LEVEL 2",
                WIDTH // 2 - 170,
                320,
                340,
                60,
                self.small_button_font,
                "level_2"
            ),
            Button(
                "LEVEL 3",
                WIDTH // 2 - 170,
                400,
                340,
                60,
                self.small_button_font,
                "level_3"
            ),
            Button(
                "BACK",
                WIDTH // 2 - 170,
                480,
                340,
                55,
                self.small_button_font,
                "back"
            ),
        ]

        self.show_tutorial = False
        self.show_level_select = False

    def handle_click(self, mouse_pos):
        if self.show_level_select:
            for button in self.level_buttons:
                if button.is_hovered(mouse_pos):
                    return button.action

            return None

        for button in self.buttons:
            if button.is_hovered(mouse_pos):
                return button.action

        return None

    def draw_fallback_background(self, screen):
        screen.fill((210, 240, 255))

        title = self.title_font.render("PENGUIN PATH", True, DARK_BLUE)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 80)
        )

    def draw_tutorial_panel(self, screen):
        panel_rect = pygame.Rect(120, 120, WIDTH - 240, HEIGHT - 240)

        pygame.draw.rect(
            screen,
            (240, 250, 255),
            panel_rect,
            border_radius=24
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            panel_rect,
            width=4,
            border_radius=24
        )

        title = self.button_font.render("HUONG DAN", True, DARK_BLUE)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 155)
        )

        lines = [
            "A / D hoac mui ten trai/phai: doi lane",
            "Nam tay hoac SPACE: bat khien",
            "Dung khien de vuot qua tuong bang 3 lane",
            "Ne vat can va ve dich cung Piko",
            "",
            "Nhan ESC hoac click Tutorial de dong bang nay"
        ]

        y = 220
        for line in lines:
            text = self.info_font.render(line, True, BLACK)
            screen.blit(text, (160, y))
            y += 38

    def draw(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        else:
            self.draw_fallback_background(screen)

        mouse_pos = pygame.mouse.get_pos()

        # Vẽ nút lên trên ảnh nền
        for button in self.buttons:
            button.draw(screen, mouse_pos)

        # Dòng hướng dẫn nhỏ dưới cùng
        hint = self.info_font.render(
            "ENTER/SPACE: bat dau  |  Click nut de chon",
            True,
            DARK_BLUE
        )
        screen.blit(
            hint,
            (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 40)
        )

        if self.show_tutorial:
            self.draw_tutorial_panel(screen)

        if self.show_level_select:
            self.draw_level_select_panel(screen)

    def draw_level_select_panel(self, screen):
        panel_rect = pygame.Rect(110, 100, WIDTH - 220, HEIGHT - 160)

        pygame.draw.rect(
            screen,
            (240, 250, 255),
            panel_rect,
            border_radius=24
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            panel_rect,
            width=4,
            border_radius=24
        )

        title = self.button_font.render("CHON MAN CHOI", True, DARK_BLUE)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 145)
        )

        mouse_pos = pygame.mouse.get_pos()

        for button in self.level_buttons:
            button.draw(screen, mouse_pos)        