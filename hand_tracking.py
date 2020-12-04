import cv2 as cv
import mediapipe as mp
import numpy as np
import glob
import random


def add_image_with_alpha(bottom_img, top_img, center_pos):
    # get image shapes and center coordinates
    t_c_x, t_c_y = center_pos
    b_cols, b_rows, _ = bottom_img.shape
    t_cols, t_rows, _ = top_img.shape

    # calculate top image coordinates on bottom image
    b_y1 = max(t_c_y - int(t_cols / 2), 0)
    b_y2 = min(t_c_y + t_cols - int(t_cols / 2), b_cols)
    b_x1 = max(t_c_x - int(t_rows / 2), 0)
    b_x2 = min(t_c_x + t_rows - int(t_rows / 2), b_rows)
    
    # calculate coordinates of bottom images to crop if necessary
    t_y1 = max(t_cols - b_y2, 0)
    t_y2 = min(b_cols - b_y1, t_cols)
    t_x1 = max(t_rows - b_x2, 0)
    t_x2 = min(b_rows - b_x1, t_rows)

    # calculate alpha value for top and bottom image of area in question
    t_a = top_img[t_y1:t_y2, t_x1:t_x2, 3] / 255.0
    b_a = 1.0 - t_a

    # scale each channel according to alpha and add bottom to top image
    for c in range(3):
        bottom_img[b_y1:b_y2, b_x1:b_x2, c] = bottom_img[b_y1:b_y2, b_x1:b_x2, c] * b_a + \
                                              top_img[t_y1:t_y2, t_x1:t_x2, c] * t_a

    return bottom_img


def draw_microbes(image, landmark_result, microbes):
    img_rows, img_cols, _ = image.shape

    for microbe in microbes:
        # get hand index and continue if hand not detected
        hand_name = microbe["pos"]["hand_name"]
        try:
            hand_i = next(
                i
                for i, hand in enumerate(landmark_result.multi_handedness)
                if hand.classification[0].label[:-1] == hand_name
            )
        except StopIteration:
            continue

        if (len(landmark_result.multi_handedness) == 1):
            hand_i = 0

        # get coordinates on image axis
        landmark_i = microbe["pos"]["landmark"].value
        landmark = landmark_result.multi_hand_landmarks[hand_i].landmark[landmark_i]

        if landmark.visibility < 0 or landmark.presence < 0:
            continue

        landmark_px = mp_drawing._normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                                  img_cols, img_rows)
        
        # add microbe image to base image
        if landmark_px:
            image = add_image_with_alpha(image, microbe["image"], landmark_px)

    return image


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

microbes = list(glob.glob("res/microbes/*"))
random.shuffle(microbes)
microbes_l = len(microbes)
microbes_n = random.randint(min(3, microbes_l), microbes_l)
microbes = microbes[0:microbes_n]

positions = [
    {
        "landmark": landmark,
        "hand_name": hand,
    }
    for landmark in list(mp_hands.HandLandmark)
    for hand in ["Left", "Right"]
]

microbe_imgs = []

for microbe in microbes:
    microbe_img = cv.imread(microbe, cv.IMREAD_UNCHANGED)
    height = 50
    width = int(height / microbe_img.shape[0] * microbe_img.shape[1])
    dim = (width, height)
    microbe_imgs.append({
        "image": cv.resize(microbe_img, dim)    
    })


for microbe_img in microbe_imgs:
    pos = random.choice(positions)
    pos_i = positions.index(pos)
    microbe_img["pos"] = pos
    positions.pop(pos_i)

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

cap = cv.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv.cvtColor(
        cv.flip(image, 1),
        cv.COLOR_BGR2RGB
    )

    results = hands.process(image)

    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        image = draw_microbes(image, results, microbe_imgs)

    cv.imshow('Microbes', image)
    if cv.waitKey(5) & 0xFF == 27:
        break
hands.close()
cap.release()