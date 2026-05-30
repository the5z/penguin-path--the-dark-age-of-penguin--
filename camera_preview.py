# camera_preview.py

import cv2
import pygame
from settings import BLACK, WHITE, RED, WIDTH, CAMERA_W, CAMERA_H, CAMERA_X, CAMERA_Y


class CameraPreview:
    def __init__(self, camera_index=0, hand_tracker=None):
        self.camera = cv2.VideoCapture(camera_index)
        self.hand_tracker = hand_tracker

        self.command = "CENTER"
        self.gesture = "NONE"
        self.hand_detected = False

        self.camera_available = self.camera.isOpened()

        self.preview_width = CAMERA_W
        self.preview_height = CAMERA_H

        self.x = CAMERA_X
        self.y = CAMERA_Y
        self.border_padding = 5

        if not self.camera_available:
            print("Khong mo duoc camera. Game se chay khong co camera.")

    def draw_camera_error(self, screen, ui):
        outer_rect = pygame.Rect(
            self.x,
            self.y,
            self.preview_width + self.border_padding * 2,
            self.preview_height + self.border_padding * 2
        )

        inner_rect = pygame.Rect(
            self.x + self.border_padding,
            self.y + self.border_padding,
            self.preview_width,
            self.preview_height
        )

        pygame.draw.rect(screen, BLACK, outer_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, inner_rect)

        ui.draw_text(
            screen,
            "NO CAMERA",
            self.x + 35,
            self.y + 70,
            RED
        )

    def draw(self, screen, ui):
        if not self.camera_available:
            self.draw_camera_error(screen, ui)
            return

        try:
            success, cam_frame = self.camera.read()
        except Exception as error:
            print(f"Loi doc camera: {error}")
            self.camera_available = False
            self.draw_camera_error(screen, ui)
            return

        if not success or cam_frame is None:
            print("Khong doc duoc frame tu camera.")
            self.camera_available = False
            self.draw_camera_error(screen, ui)
            return

        # Lật ảnh như gương
        cam_frame = cv2.flip(cam_frame, 1)

        # Nếu có hand_tracker thì xử lý nhận diện tay
        if self.hand_tracker is not None:
            try:
                cam_frame, self.command, self.gesture, self.hand_detected = (
                    self.hand_tracker.process_frame(cam_frame)
                )
            except Exception as error:
                print(f"Loi hand tracking: {error}")
                self.command = "CENTER"
                self.gesture = "NONE"
                self.hand_detected = False

        # Resize khung camera
        cam_frame = cv2.resize(
            cam_frame,
            (self.preview_width, self.preview_height)
        )

        # OpenCV dùng BGR, Pygame dùng RGB
        cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

        # Chuyển sang surface của Pygame
        cam_surface = pygame.surfarray.make_surface(cam_frame.swapaxes(0, 1))

        outer_rect = pygame.Rect(
            self.x,
            self.y,
            self.preview_width + self.border_padding * 2,
            self.preview_height + self.border_padding * 2
        )

        inner_rect = pygame.Rect(
            self.x + self.border_padding,
            self.y + self.border_padding,
            self.preview_width,
            self.preview_height
        )

        # Vẽ khung camera
        pygame.draw.rect(screen, BLACK, outer_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, inner_rect)

        screen.blit(
            cam_surface,
            (self.x + self.border_padding, self.y + self.border_padding)
        )

        # Nếu muốn bỏ chữ Camera thì comment dòng dưới
        ui.draw_text(
            screen,
            "Camera",
            self.x + self.preview_width // 2 - 45,
            self.y + self.preview_height + 15,
            BLACK
        )

    def get_command(self):
        return self.command

    def get_gesture(self):
        return self.gesture

    def is_hand_detected(self):
        return self.hand_detected

    def release(self):
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()