import cv2 as cv
import numpy as np


# PARAMS
HISTORY = 2
MOG2_THRESHOLD = 11
KNN_THRESHOLD = 500

MASK_NOISE_BLUR_RAD = 9
MASK_SMOOTH_BLUR_RAD = 9
MASK_BLUR_STDEV = 2

DIRTY_COLOR_RGB = (41, 150, 23)
COLOR_FACTOR = 0.8


cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("error opening webcam")

# generate filled image from RGB
_, frame = cap.read()
dirty_frame = np.empty(frame.shape)

for i in range(3):
    dirty_frame[:, :, i].fill(DIRTY_COLOR_RGB[2 - i])

# initialize background subtractor
back_sub = cv.createBackgroundSubtractorMOG2(history=HISTORY, varThreshold=MOG2_THRESHOLD)
#back_sub = cv.createBackgroundSubtractorKNN(history=HISTORY, dist2Threshold=KNN_THRESHOLD)

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)

    # create mask with background substraction
    sub_mask = back_sub.apply(frame)

    # mask noise reduction with median blur
    sub_mask = cv.medianBlur(
        sub_mask,
        MASK_NOISE_BLUR_RAD
    )

    # mask smoothening with gaussian blur
    sub_mask = cv.GaussianBlur(
        sub_mask,
        (MASK_SMOOTH_BLUR_RAD,MASK_SMOOTH_BLUR_RAD),
        MASK_BLUR_STDEV
    )
    
    # make 3 channel alpha mask
    sub_mask = cv.cvtColor(sub_mask, cv.COLOR_GRAY2BGR)
    sub_alpha = sub_mask.astype(float) / (255 * (1/COLOR_FACTOR))

    # blend using alpha mask
    foreground = cv.multiply(sub_alpha, dirty_frame, dtype=0)
    background = cv.multiply(1.0 - sub_alpha, frame, dtype=0)
    out = cv.add(foreground, background)

    # show
    cv.imshow('dirty_motion', out)
    cv.imshow('motion_mask', sub_mask)

    c = cv.waitKey(1)
    if c == 27:
        break

cap.release()
cv.destroyAllWindows()