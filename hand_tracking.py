import cv2 as cv
import mediapipe as mp
import numpy as np
import glob
import random
import math


MICROBE_MIN_HEIGHT = 30
MICROBE_MAX_HEIGHT = 50
MICROBE_MIN_AMOUNT = 10
MICROBE_MAX_AMOUNT = 15

MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5


def rotate_img_uncropped(image, angle):
    # get rotation matrix
    rows, cols = image.shape[:2]
    center = (cols / 2.0, rows / 2.0)
    rot = cv.getRotationMatrix2D(center, angle, 1)
    
    # set max bounds of rotated image
    abs_cos = abs(rot[0, 0]) 
    abs_sin = abs(rot[0, 1])

    bound_cols = int(rows * abs_sin + cols * abs_cos)
    bound_rows = int(rows * abs_cos + cols * abs_sin)

    rot[0,2] += bound_cols / 2.0 - cols / 2.0
    rot[1,2] += bound_rows / 2.0 - rows / 2.0

    # return rotated image
    return cv.warpAffine(image, rot, (bound_cols, bound_rows))


def resize_img_hand_distance(image, landmark_result, base_height, scale=1):
    pass


def add_image_with_alpha(bottom_img, top_img, center_pos):

    # get image shapes and center coordinates
    t_c_x, t_c_y = center_pos
    b_rows, b_cols = bottom_img.shape[:2]
    t_rows, t_cols = top_img.shape[:2]

    # calculate top image coordinates on bottom image
    b_y1 = max(t_c_y - int(t_rows / 2), 0)
    b_y2 = max(min(t_c_y + t_rows - int(t_rows / 2), b_rows), 0)
    b_x1 = max(t_c_x - int(t_cols / 2), 0)
    b_x2 = max(min(t_c_x + t_cols - int(t_cols / 2), b_cols), 0)
    
    # calculate coordinates of bottom images to crop if necessary
    t_y1 = max(t_rows - b_y2, 0)
    t_y2 = max(min(b_rows - b_y1, t_rows), 0)
    t_x1 = max(t_cols - b_x2, 0)
    t_x2 = max(min(b_cols - b_x1, t_cols), 0)

    # calculate alpha value for top and bottom image of area in question
    t_a = top_img[t_y1:t_y2, t_x1:t_x2, 3] / 255.0
    b_a = 1.0 - t_a

    # scale each channel according to alpha and add bottom to top image
    for c in range(3):
        bottom_img[b_y1:b_y2, b_x1:b_x2, c] = bottom_img[b_y1:b_y2, b_x1:b_x2, c] * b_a + \
                                              top_img[t_y1:t_y2, t_x1:t_x2, c] * t_a

    return bottom_img


def draw_microbe_on_hand(image, microbe_img, landmark_result, microbe_data):
    img_rows, img_cols = image.shape[:2]

    # get hand index and return if hand not detected
    hand_name = microbe["pos"]["hand_name"]
    try:
        hand_i = next(
            i
            for i, hand in enumerate(landmark_result.multi_handedness)
            if hand.classification[0].label[:-1] == hand_name
        )
    except StopIteration:
        return image

    if (len(landmark_result.multi_handedness) == 1):
        hand_i = 0

    # get coordinates on image axis
    landmark_ai = microbe["pos"]["connection"][0].value
    landmark_bi = microbe["pos"]["connection"][1].value
    
    landmark_an = landmark_result.multi_hand_landmarks[hand_i].landmark[landmark_ai]
    landmark_bn = landmark_result.multi_hand_landmarks[hand_i].landmark[landmark_bi]

    landmark_dx = landmark_bn.x - landmark_an.x
    landmark_dy = landmark_bn.y - landmark_an.y

    # rotate microbe
    angle = -1 * math.degrees(
        math.atan2(landmark_dy, landmark_dx)
    )
    angle = angle + microbe["pos"]["angle"]
    rot_microbe_img = rotate_img_uncropped(microbe_img, angle)

    #if landmark.visibility < 0 or landmark.presence < 0:
    #    return image

    center_x = landmark_dx * microbe["pos"]["distance_n"] + landmark_an.x
    center_y = landmark_dy * microbe["pos"]["distance_n"] + landmark_an.y

    center = (
        int(center_x * img_cols),
        int(center_y * img_rows),
    )

    #microbe["image"] = resize_img_hand_distance(microbe_img, results, MICROBE_BASE_HEIGHT, scale=1)
    
    # add microbe image to base image
    return add_image_with_alpha(image, rot_microbe_img, center)


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# load microbe images
microbes = list(glob.glob("res/microbes/*"))
microbes_n = random.randint(MICROBE_MIN_AMOUNT, MICROBE_MAX_AMOUNT)

microbe_imgs = [
    cv.imread(microbe, cv.IMREAD_UNCHANGED)
    for microbe in microbes
]

# initialize of a set of microbes at set positions
microbe_data = [
    {
        "pos":
        {
            "connection": random.sample(mp_hands.HAND_CONNECTIONS, 1)[0],
            "distance_n": random.randint(100, 900) / 1000.0,
            "angle": random.randint(0, 359),
            "hand_name": random.choice(("Left", "Right")),
        },
        "size": dict(),
        "image_nr": random.randint(0, len(microbe_imgs) - 1)
    }
    for _ in range(microbes_n)
]

for microbe in microbe_data:
    init_height, init_width = microbe_imgs[microbe["image_nr"]].shape[:2]
    microbe["size"]["height"] = MICROBE_MIN_HEIGHT + random.randint(0, MICROBE_MAX_HEIGHT - MICROBE_MIN_HEIGHT)
    microbe["size"]["width"] = int(microbe["size"]["height"] / init_height * init_width)

# initialize model for hand detection
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
)


# read frames
cap = cv.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # convert flipped image to RGB 
    image = cv.cvtColor(
        cv.flip(image, 1),
        cv.COLOR_BGR2RGB
    )

    # detect nodes (joints and palm)
    results = hands.process(image)

    # convert image back to native opencv BGR
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    # resize and draw microbes on image
    if results.multi_hand_landmarks:
        for microbe in microbe_data:
            microbe_img = microbe_imgs[microbe["image_nr"]]
            microbe_img = cv.resize(microbe_img, (microbe["size"]["width"], microbe["size"]["width"]))
            image = draw_microbe_on_hand(image, microbe_img, results, microbe)

    # show image and close window with ESC
    cv.imshow('Microbes', image)
    if cv.waitKey(5) & 0xFF == 27:
        break

# exit gracefully
hands.close()
cap.release()