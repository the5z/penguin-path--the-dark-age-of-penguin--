from settings import WIDTH, HEIGHT

FAR_Y = int(HEIGHT * 0.20)
NEAR_Y = int(HEIGHT * 0.84)

FAR_LANE_GAP = int(WIDTH * 0.065)
NEAR_LANE_GAP = int(WIDTH * 0.19)

FAR_SCALE = 0.35
NEAR_SCALE = 1.45


def get_perspective_position(lane, depth):
    depth = max(0, min(1, depth))
    t = 1 - depth

    center_x = WIDTH // 2

    y = FAR_Y + t * (NEAR_Y - FAR_Y)
    lane_gap = FAR_LANE_GAP + t * (NEAR_LANE_GAP - FAR_LANE_GAP)

    lane_offset = lane - 1
    x = center_x + lane_offset * lane_gap

    scale = FAR_SCALE + t * (NEAR_SCALE - FAR_SCALE)

    return x, y, scale