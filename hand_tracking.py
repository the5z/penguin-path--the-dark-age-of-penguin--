# hand_tracking.py

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    def __init__(self, model_path="hand_landmarker.task"):
        self.base_options = python.BaseOptions(model_asset_path=model_path)

        self.options = vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.landmarker = vision.HandLandmarker.create_from_options(self.options)

        self.timestamp_ms = 0
        self.command = "CENTER"
        self.gesture = "NONE"
        self.hand_detected = False
        self.last_landmarks = None
    def is_finger_folded(self, hand_landmarks, tip_id, pip_id):
        """
        Kiểm tra ngón tay có đang gập xuống không.
        Với camera 2D: nếu đầu ngón thấp hơn khớp giữa thì xem như gập.
        """
        tip = hand_landmarks[tip_id]
        pip = hand_landmarks[pip_id]

        return tip.y > pip.y

    def detect_gesture(self, hand_landmarks):
        """
        Gesture:
        - GUN: bắn
        - FIST: khiên gốc
        - ITEM_HEAL: chỉ ngón út
        - ITEM_FAST_SHIELD: chỉ ngón cái
        - ITEM_SLOW: ngón cái + ngón út
        - ITEM_BOMB: 4 ngón trừ ngón cái
        """

        index_folded = self.is_finger_folded(hand_landmarks, 8, 6)
        middle_folded = self.is_finger_folded(hand_landmarks, 12, 10)
        ring_folded = self.is_finger_folded(hand_landmarks, 16, 14)
        pinky_folded = self.is_finger_folded(hand_landmarks, 20, 18)

        index_extended = not index_folded
        middle_extended = not middle_folded
        ring_extended = not ring_folded
        pinky_extended = not pinky_folded

        # Nhận diện ngón cái bằng khoảng cách từ đầu ngón cái tới cổ tay
        thumb_tip_dist = self.landmark_distance(hand_landmarks, 4, 0)
        thumb_ip_dist = self.landmark_distance(hand_landmarks, 3, 0)
        thumb_extended = thumb_tip_dist > thumb_ip_dist * 1.15

        folded_count = sum([
            index_folded,
            middle_folded,
            ring_folded,
            pinky_folded
        ])

        # =====================
        # ITEM GESTURES
        # =====================

        # Chỉ ngón út: hồi máu
        # if (
        #     pinky_extended
        #     and index_folded
        #     and middle_folded
        #     and ring_folded
        #     and not thumb_extended
        # ):
        #     return "ITEM_HEAL"

        # # Chỉ ngón cái: khiên cấp tốc
        # if (
        #     thumb_extended
        #     and index_folded
        #     and middle_folded
        #     and ring_folded
        #     and pinky_folded
        # ):
        #     return "ITEM_FAST_SHIELD"

        # Ngón cái + ngón út: giảm tốc
        if (
            thumb_extended
            and pinky_extended
            and index_folded
            and middle_folded
            and ring_folded
        ):
            return "ITEM_SLOW"

        # 4 ngón trừ ngón cái: bom
        if (
            not thumb_extended
            and index_extended
            and middle_extended
            and ring_extended
            and pinky_extended
        ):
            return "ITEM_BOMB"

        # =====================
        # GAME GESTURES CŨ
        # =====================

        # Ký hiệu súng: trỏ duỗi, giữa/áp út/út gập
        if index_extended and middle_folded and ring_folded and pinky_folded:
            return "GUN"

        if folded_count >= 4:
            return "FIST"

        if folded_count == 0:
            return "OPEN_HAND"

        return "UNKNOWN"
    
    def process_frame(self, frame):
        """
        Nhận frame từ camera_preview.py
        Trả về:
        - frame đã vẽ điểm tay
        - command: LEFT / CENTER / RIGHT
        - hand_detected: True / False
        """

        if frame is None:
            return frame, "CENTER", False

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.landmarker.detect_for_video(
            mp_image,
            self.timestamp_ms
        )

        self.timestamp_ms += 33

        self.hand_detected = False
        self.command = "CENTER"
        self.gesture = "NONE"
        self.last_landmarks = None

        h, w, _ = frame.shape

        if result.hand_landmarks:
            self.hand_detected = True

            hand_landmarks = result.hand_landmarks[0]
            self.last_landmarks = hand_landmarks
            self.gesture = self.detect_gesture(hand_landmarks)
            # Lấy cổ tay, landmark số 0
            wrist = hand_landmarks[0]

            wrist_x = int(wrist.x * w)
            wrist_y = int(wrist.y * h)

            # Chia khung camera thành 3 vùng trái / giữa / phải
            if wrist_x < w / 3:
                self.command = "LEFT"
            elif wrist_x > w * 2 / 3:
                self.command = "RIGHT"
            else:
                self.command = "CENTER"

            # Vẽ toàn bộ 21 điểm tay
            for landmark in hand_landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

            # Vẽ cổ tay to hơn
            cv2.circle(frame, (wrist_x, wrist_y), 9, (255, 0, 0), -1)

            # Vẽ 3 vùng điều khiển
            cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 255, 0), 2)
            cv2.line(frame, (w * 2 // 3, 0), (w * 2 // 3, h), (255, 255, 0), 2)

            cv2.putText(
            frame,
            f"{self.command} | {self.gesture}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        else:
            cv2.putText(
                frame,
                "NO HAND",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        return frame, self.command, self.gesture, self.hand_detected

    def close(self):
        self.landmarker.close()

    def landmark_distance(self, hand_landmarks, id1, id2):
        p1 = hand_landmarks[id1]
        p2 = hand_landmarks[id2]

        dx = p1.x - p2.x
        dy = p1.y - p2.y

        return (dx * dx + dy * dy) ** 0.5