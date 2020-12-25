import cv2 as cv
import mediapipe as mp
import glob
import random
import itertools
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from .constants import *
from .drawers import *


mp_hands = mp.solutions.hands

class MicrobeARObj(QObject):
    newFrameAvail = pyqtSignal(QImage)


    def __init__(self, microbeRes, amount):
        super().__init__()

        # load microbe images
        possible_locations = list(itertools.product(HAND_LABELS, mp_hands.HAND_CONNECTIONS))
        microbe_files = list(glob.glob(f"{microbeRes}/*"))
        microbes_n = min(amount, len(possible_locations))

        microbe_imgs = [
            cv.imread(microbe_f, cv.IMREAD_UNCHANGED)
            for microbe_f in microbe_files
        ]

        # initialization of a list of microbes with a defined position, angle and size
        self.microbe_data = {
            hand: list()
            for hand in HAND_LABELS
        }

        for _ in range(microbes_n):
            loc_i = random.randrange(len(possible_locations))
            hand, conn_loc = possible_locations[loc_i]
            possible_locations.pop(loc_i)

            microbe_img = random.choice(microbe_imgs)
            init_height, init_width = microbe_img.shape[:2]
            height = MICROBE_MIN_HEIGHT + random.randint(0, MICROBE_MAX_HEIGHT - MICROBE_MIN_HEIGHT)
            width = int(height / init_height * init_width)
            res_microbe_img = cv.resize(microbe_img, (width, height))

            self.microbe_data[hand].append(
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
                    "opacity": 1,
                    "image": res_microbe_img,
                }
            )

    @pyqtSlot()
    def startRunning(self):
        # initialize background subtractor
        back_sub = cv.createBackgroundSubtractorMOG2(history=HISTORY, varThreshold=MOG2_THRESHOLD)
        #back_sub = cv.createBackgroundSubtractorKNN(history=HISTORY, dist2Threshold=KNN_THRESHOLD)

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
            
            # detect landmarks on hand
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

                print(results.multi_handedness)
                if results.multi_hand_landmarks:
                    try:
                        hand_i = next(
                            i
                            for i, hand in enumerate(results.multi_handedness)
                            if hand.classification[0].label == hand_name
                        )
                    except StopIteration:
                        hand_i = None
                else: 
                    hand_i = None

                # decrease opacity
                for i, microbe in enumerate(self.microbe_data[hand_name]):
                    if microbe["opacity"] <= 0:
                        self.microbe_data[hand_name].pop(i)
                    elif microbe["opacity"] < 1:
                        microbe["opacity"] -= OPACITY_DECR

                    # if hand detected, use landmark connections
                    if hand_i != None:
                        landmark_result = results.multi_hand_landmarks[hand_i]
                        image = draw_microbe_on_hand(image, microbe["image"], landmark_result, microbe)

                    # if hand not detected, use motion
                    else:
                        try:
                            image = draw_microbe_on_motion(image, microbe["image"], motion_pos, microbe)
                        # error when motion_pos None (no movement), likely no hands
                        except TypeError:
                            pass

            # convert opencv image to qt image
            rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            height, width, channels = rgb_image.shape
            q_image = QImage(rgb_image.data, width, height, width * channels, QImage.Format_RGB888)

            # emit image
            self.newFrameAvail.emit(q_image)

        # exit gracefully
        hands.close()
        cap.release()

    
    def delMicrobe(self):
        microbe = random.choice(self.microbe_data[HAND_LABELS[0]] + self.microbe_data[HAND_LABELS[1]])
        microbe["opacity"] -= OPACITY_DECR