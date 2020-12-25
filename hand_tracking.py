import cv2 as cv
import mediapipe as mp
import numpy as np
import glob
import random
import math
import itertools


# parameters
HISTORY = 5
MOG2_THRESHOLD = 11
KNN_THRESHOLD = 500

MASK_NOISE_BLUR_RAD = 9

MICROBE_MIN_HEIGHT = 30
MICROBE_MAX_HEIGHT = 40
MICROBE_MIN_AMOUNT = 10
MICROBE_MAX_AMOUNT = 15

OPACITY_DECR = .05
OPACITY_DECR_ODD = .01

MOTION_MAX_DIST = 50
MOTION_MAX_RAND_OFFSET = 2

MIN_DETECTION_CONFIDENCE = .7
MIN_TRACKING_CONFIDENCE = .5

HAND_LABELS = ("Left", "Right")


def set_opacity(image, opacity):
    image[:, :, 3] = cv.multiply(image[:, :, 3], opacity)
    return image
    

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


def add_image_with_alpha(bottom_img, top_img, center_pos, opacity):
    # apply opacity
    if opacity < 1:
        top_img = set_opacity(top_img, opacity)

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



mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# initialize background subtractor
back_sub = cv.createBackgroundSubtractorMOG2(history=HISTORY, varThreshold=MOG2_THRESHOLD)
#back_sub = cv.createBackgroundSubtractorKNN(history=HISTORY, dist2Threshold=KNN_THRESHOLD)


# load microbe images
possible_locations = list(itertools.product(HAND_LABELS, mp_hands.HAND_CONNECTIONS))
microbe_files = list(glob.glob("res/microbes/*"))
microbes_n = random.randint(
    min(MICROBE_MIN_AMOUNT, len(possible_locations)), 
    min(MICROBE_MAX_AMOUNT, len(possible_locations))
)

microbe_imgs = [
    cv.imread(microbe_f, cv.IMREAD_UNCHANGED)
    for microbe_f in microbe_files
]

# initialization of a list of microbes with a defined position, angle and size
microbe_data = {
    hand: list()
    for hand in HAND_LABELS
}

for _ in range(microbes_n):
    loc_i = random.randrange(len(possible_locations))
    hand, conn_loc = possible_locations[loc_i]
    possible_locations.pop(loc_i)

    img_nr = random.randint(0, len(microbe_imgs) - 1)
    init_height, init_width = microbe_imgs[img_nr].shape[:2]
    height = MICROBE_MIN_HEIGHT + random.randint(0, MICROBE_MAX_HEIGHT - MICROBE_MIN_HEIGHT)
    width = int(height / init_height * init_width)

    microbe_data[hand].append(
        {
            "pos":
            {
                "connection": conn_loc,
                "distance_n": random.randint(100, 900) / 1000.0,
                "angle": random.randint(0, 359),

                "prev_x": None,
                "prev_y": None,
                "prev_angle": None,
            },
            "size": 
            {
                "width": width,
                "height": height,
            },
            "opacity": 1,
            "image_nr": random.randint(0, len(microbe_imgs) - 1),
        }
    )

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
    
    # detect landmakrs on hand
    results = hands.process(image)

    # convert image back to native opencv BGR, TODO: remove in production if displayed in Qt
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    # create motion mask with background substraction
    motion_mask = back_sub.apply(image)
    
    # if both hands not detected
    if (not results.multi_hand_landmarks) or (len(results.multi_hand_landmarks) < 2):
        # motion mask noise reduction with median blur
        motion_mask = cv.medianBlur(
            motion_mask,
            MASK_NOISE_BLUR_RAD
        )

        motion_pos = cv.findNonZero(motion_mask)

    for hand_name in HAND_LABELS:
        # try to get hand index
        if results.multi_hand_landmarks:
            try:
                hand_i = next(
                    i
                    for i, hand in enumerate(results.multi_handedness)
                    if hand.classification[0].label[:-1] == hand_name
                )
            except StopIteration:
                hand_i = None
        else: 
            hand_i = None

        # decrease opacity
        for i, microbe in enumerate(microbe_data[hand_name]):
            if microbe["opacity"] <= 0:
                microbe_data[hand_name].pop(i)
            elif (microbe["opacity"] < 1) or (random.random() <= OPACITY_DECR_ODD):
                microbe["opacity"] -= OPACITY_DECR

            # resize image
            microbe_img = microbe_imgs[microbe["image_nr"]]
            microbe_img = cv.resize(microbe_img, (microbe["size"]["width"], microbe["size"]["width"]))

            # if hand detected, use landmark connections
            if hand_i != None:
                landmark_result = results.multi_hand_landmarks[hand_i]
                image = draw_microbe_on_hand(image, microbe_img, landmark_result, microbe)

            # if hand not detected, use motion
            else:
                try:
                    image = draw_microbe_on_motion(image, microbe_img, motion_pos, microbe)
                # error when motion_pos None (no movement), likely no hands
                except TypeError:
                    pass

        

    # show image and close window with ESC
    cv.imshow('Microbes', image)
    if cv.waitKey(5) & 0xFF == 27:
        break

# exit gracefully
hands.close()
cap.release()