import numpy as np
import math
import random
from .constants import *
from .transformers import *


def draw_microbe_on_hand(image, microbe_img, landmark_result, microbe_data):
    img_rows, img_cols = image.shape[:2]

    # get coordinates on image axis
    landmark_ai = microbe_data["pos"]["connection"][0].value
    landmark_bi = microbe_data["pos"]["connection"][1].value
    
    landmark_an = landmark_result.landmark[landmark_ai]
    landmark_bn = landmark_result.landmark[landmark_bi]

    landmark_dx = landmark_bn.x - landmark_an.x
    landmark_dy = landmark_bn.y - landmark_an.y

    # rotate microbe
    angle = -1 * math.degrees(
        math.atan2(landmark_dy, landmark_dx)
    )
    angle = angle + microbe_data["pos"]["angle"]
    rot_microbe_img = rotate_img_uncropped(microbe_img, angle)

    # get microbe center on image
    center_x = landmark_dx * microbe_data["pos"]["distance_n"] + landmark_an.x
    center_y = landmark_dy * microbe_data["pos"]["distance_n"] + landmark_an.y

    center = (
        int(center_x * img_cols),
        int(center_y * img_rows),
    )

    #microbe["image"] = resize_img_hand_distance(microbe_img, results, MICROBE_BASE_HEIGHT, scale=1)

    # save position and angle in case needed in next iteration
    microbe_data["pos"]["prev_x"], microbe_data["pos"]["prev_y"] = center
    microbe_data["pos"]["prev_angle"] = angle
    
    # add microbe image to base image
    return add_image_with_alpha(image, rot_microbe_img, center, microbe_data["opacity"])


def draw_microbe_on_motion(image, microbe_img, motion_pos, microbe_data):
    prev_x = microbe_data["pos"]["prev_x"]
    prev_y = microbe_data["pos"]["prev_y"]

    # no previously saved positions or angles in hand
    if prev_x == None:
        return image

    # get closest pixel with motion
    dist = np.sqrt((motion_pos[:, :, 0] - prev_x) ** 2 + (motion_pos[:, :, 1] - prev_y) ** 2)
    min_idx = np.argmin(dist)
    if dist[min_idx] > MOTION_MAX_DIST:
        return image
    min_pos = motion_pos[min_idx][0]
    
    # add little offset to closest pixel
    min_pos[0] += random.randint(0, MOTION_MAX_RAND_OFFSET)
    min_pos[1] += random.randint(0, MOTION_MAX_RAND_OFFSET)

    # save position
    microbe_data["pos"]["prev_x"], microbe_data["pos"]["prev_y"] = min_pos
    
    # rotate microbe
    rot_microbe_img = rotate_img_uncropped(microbe_img, microbe_data["pos"]["prev_angle"])

    return add_image_with_alpha(image, rot_microbe_img, min_pos, microbe_data["opacity"])