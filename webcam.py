import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("error opening webcam")

backSub = cv.createBackgroundSubtractorMOG2()
#backSub = cv.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    frame = backSub.apply(
        cv.flip(frame, 1)
    )

    cv.imshow('webcam', frame)

    c = cv.waitKey(1)
    if c == 27:
        break

cap.release()
cv.destroyAllWindows()