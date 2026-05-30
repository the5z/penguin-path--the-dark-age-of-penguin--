# ui.py

import os
import pygame

from settings import BLACK


def get_vietnamese_font(size):
    font_candidates = [
        "assets/fonts/arial.ttf",
        "assets/fonts/Roboto-Regular.ttf",
        "assets/fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
    ]

    for font_path in font_candidates:
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)

    return pygame.font.SysFont("arial", size)


class UI:
    def __init__(self):
        self.font = get_vietnamese_font(30)
        self.small_font = get_vietnamese_font(24)
        self.big_font = get_vietnamese_font(56)

    def draw_text(self, screen, text, x, y, color=BLACK, size="normal"):
        if size == "big":
            used_font = self.big_font
        elif size == "small":
            used_font = self.small_font
        else:
            used_font = self.font

        img = used_font.render(text, True, color)
        screen.blit(img, (x, y))

    def draw_center_text(self, screen, text, center_x, y, color=BLACK, size="normal"):
        if size == "big":
            used_font = self.big_font
        elif size == "small":
            used_font = self.small_font
        else:
            used_font = self.font

        img = used_font.render(text, True, color)
        screen.blit(img, (center_x - img.get_width() // 2, y))